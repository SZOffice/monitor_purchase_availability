# -*- coding: utf-8 -*-  
import os, sys, time
import urllib
from datetime import datetime
import helpers.file_helper as file_helper
import helpers.send_email as send_email
import helpers.send_slack as send_slack
import helpers.sql_helper as sql_helper
import config

now = datetime.now()
  
def string_toDatetime(string):
    return datetime.strptime(string, "%d/%b/%Y:%H:%M:%S")

def validate_log_db(env, country, purchase_order_ref):
    print("country: %s, purchase_order_ref: %s" % (country, purchase_order_ref))
    db_info = config.jobsdb_mssql[env][country]
    ms_Conn = sql_helper.MSSQL(host=db_info["host"], user=db_info["user"], pwd=db_info["pwd"], db=db_info["db"])    
    sql = "SELECT IsNull(JobAdId, 0) as JobAdId FROM EmpEPaymentLog Where PurchaseOrderRef=N'%s'" % purchase_order_ref
    result_list =  ms_Conn.ExecQuery(sql)
    log_type = 0    #0:no record  1:normal purchase  2:post jobad purchase
    if len(result_list) == 0:
        print("not found purchase ref %s in database-EmpEPaymentLog." % purchase_order_ref)
    else:
        if result_list[0][0] == 0:
            log_type = 1
            print("online - normal purchase")
        else:
            log_type = 2
            print("online - post jobad purchase")
    return log_type

#read txt
def validate_log(server, env, country, last_log_time='', slack=None, email_receivers=None):
    list_error_log = []
    filePath = config.path_nginx_paymentgateway_log.format(server)
    totalLogs = 0

    print("log filePath: %s" % filePath)
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
                        #log_type = validate_log_db(env, country, ref.split('_')[0])
                        isOnline = True
                if isOnline:
                    list_error_log.append(line)
                        
    if len(list_error_log) > 0:
        print("exists error log: %s" % str(list_error_log))
        if email_receivers != None:
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
        
            print('receivers:' + str(email_receivers))
            print('start send email...')
            try:
                from_addr = "ifelse01@126.com"
                send_email.send_email(from_addr, email_receivers, subject, body_text)
                #send_email.send_email(from_addr, email_receivers, subject, body_html, True)
            except Exception as e:
                print('send email error:' + e)
            
        if slack != None:
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
                send_slack.send_slack(slack["token"], slack["channel"], title, attachments)
            except Exception as e:
                print('send slack error:' + str(e))
    else:
        print("validated pass")
    return (last_log_time, list_error_log)
    
if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("not args")
    
    t = time.time()
    
    #list_server = ["hknginx3", "hknginx4", "hknginx5", "idnginx3", "idnginx4", "thnginx3", "thnginx4"]
    list_server = ["hknginx3", "hknginx4", "hknginx5"]
    for server in list_server:
        validate_log(server, 'Production', 'HK')

    print("total run time:")
    e = time.time()
    print(e-t)
