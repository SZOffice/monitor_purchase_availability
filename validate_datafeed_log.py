# -*- coding: utf-8 -*-  
import os, sys, time
import urllib
from datetime import datetime
import helpers.file_helper as file_helper
import helpers.send_email as send_email
import helpers.send_slack as send_slack
import helpers.sql_helper as sql_helper
import helpers.log_helper as log_helper
import helpers.logger_helper as logger_helper
import config

now = datetime.now()
now_str = now.strftime("%Y-%m-%d %H:%M:%S")
now_id = now.strftime("%Y%m%d%H%M%S")
logger = logger_helper.mylog('validate_datafeed_log').getlog()
  
def string_toDatetime(string):
    return datetime.strptime(string, "%d/%b/%Y:%H:%M:%S")

def validate_log_db(env, country, purchase_order_ref):
    logger.info("country: %s, purchase_order_ref: %s" % (country, purchase_order_ref))
    db_info = config.jobsdb_mssql[env][country]
    ms_Conn = sql_helper.MSSQL(host=db_info["host"], user=db_info["user"], pwd=db_info["pwd"], db=db_info["db"])    
    sql = "SELECT IsNull(JobAdId, 0) as JobAdId FROM EmpEPaymentLog With(Nolock) Where PurchaseOrderRef=N'%s'" % purchase_order_ref
    result_list =  ms_Conn.ExecQuery(sql)
    log_type = 0    #0:no record  1:normal purchase  2:post jobad purchase
    if len(result_list) == 0:
        logger.info("not found purchase ref %s in database-EmpEPaymentLog." % purchase_order_ref)
    else:
        if result_list[0][0] == 0:
            log_type = 3
            logger.info("online - normal purchase")
        else:
            log_type = 9
            logger.info("online - post jobad purchase")
    return log_type

#read txt
def validate_log(server, env, country, last_log_time='', is_send_slack=False, is_send_email=False):
    list_error_log = []
    list_error_type = []
    filePath = config.path_nginx_paymentgateway_log.format(server)
    totalLogs = 0

    logger.info("log filePath: %s" % filePath)
    lines = file_helper.read_file_lines(filePath)
    totalLogs = len(lines)
    for line in lines:
        log_time = line.split(' ')[0]
        if last_log_time == '' or string_toDatetime(last_log_time) < string_toDatetime(log_time):
            last_log_time = log_time
            
            if "|200|" not in line:
                url_query = line.split('|')[16]
                query_ref = urllib.parse.parse_qs(url_query)["Ref"]
                isOnline = False
                for ref in query_ref:
                    if ref.startswith('PPL'):
                        list_error_type.append(validate_log_db(env, country, ref.split('_')[0]))
                        isOnline = True
                if isOnline:
                    list_error_log.append(line)
                        
    if len(list_error_log) > 0:
        logger.info("exists error log: %s" % str(list_error_log))
        if is_send_email:
            subject = "Monitor: Payment gateway exists error in %s at %s" % (server, now.strftime('%Y%m%d'))
            body_html = [
                """
                <p>Total Logs: %s<br/>
                Total Errors: %s<br/><br/>
                Error list: </p>
                <p>%s</p>
                """ % (str(totalLogs), str(len(list_error_log)), '<br/>'.join(list_error_log))
            ]
            body_text = """ Total Logs: %s \t\n Total errors: %s \t\n\t\n Error list: \t\n\t\n %s
                """ % (str(totalLogs), str(len(list_error_log)), '\t\n'.join(list_error_log))
        
            logger.info('start send email...')
            try:
                from_addr = config.email["from_addr"]
                send_email.send_email(from_addr, config.email["receivers"], subject, body_text)
                #send_email.send_email(from_addr, email_receivers, subject, body_html, True)
            except Exception as e:
                logger.error('send email error:' + e)
            finally:
                logger.info('end send email...')
            
        if is_send_slack:
            try:
                title = '<!here>, this is Online Payment Failed Notification'
                attachments = [
                    {
                        "pretext": "--------------",
                        "title": "total:%s | error:%s" % (str(totalLogs), str(len(list_error_log))), 
                        "text": '\n'.join(list_error_log), 
                        "color":"#7CD197",
                        "ts": int(time.time())
                    }
                ]
                send_slack.send_slack(config.slack["token"], config.slack["channel"], title, attachments)
            except Exception as e:
                logger.error('send slack error:' + str(e))
    else:
        logger.info("validated pass")
    return (last_log_time, list_error_log, list_error_type)
    
def validate_payment_log(env, country, validate_info, sql_insert_data_list=[]):    
    error_log = ""
    log_path = config.validate_nginx_paymentgateway_log
    log_data = file_helper.read_file_json(log_path)
    error_type = []
    for server in config.nginx_server[env][country]:
        logger.info(server)
    
        helper = log_helper.LogFileHelper()
        last_log_time = helper.get_payment_lastlogtime(log_data, server)
        #helper = log_helper.LogDBHelper(config.local_sqlite3)
        #last_log_time = helper.get_payment_lastlogtime(server)
        (last_log_time, list_error_log, list_error_type) = validate_log(server, env, country, last_log_time, True, True)    
        logger.info(last_log_time)
        log_data = helper.update_payment_lastlogtime(log_data, server, last_log_time)
        #helper.update_payment_lastlogtime(server, last_log_time)
        if len(list_error_log) > 0:
            error_log = error_log + str(list_error_log)    
            error_type.extend(list_error_type)
    logger.info(log_data)
    file_helper.save_file_json(log_path, log_data)

    logger.info("error_type:" + str(error_type))
    for info in validate_info:
        cur_type = info["type"]
        if info["is_skip"]:
            sql_insert_data_list.append((now_id, country, cur_type, 3, 2, '', now_str))
        else:
            if cur_type in error_type:
                sql_insert_data_list.append((now_id, country, cur_type, 3, (0 if error_log!='' else 1), error_log, now_str))
            else:
                sql_insert_data_list.append((now_id, country, cur_type, 3, 1, '', now_str))

    return sql_insert_data_list

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        logger.info("not args")
    
    t = time.time()
    
    #list_server = ["hknginx3", "hknginx4", "hknginx5", "idnginx3", "idnginx4", "thnginx3", "thnginx4"]
    list_server = ["hknginx3", "hknginx4", "hknginx5"]
    for server in list_server:
        validate_log(server, 'Production', 'HK')

    logger.info("total run time:")
    e = time.time()
    logger.info(e-t)
