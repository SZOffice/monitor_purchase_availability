# -*- coding: utf-8 -*-
import os, sys, time, datetime, json
import csv
import helpers.file_helper as file_helper
import helpers.log_helper as log_helper
import helpers.sql_helper as sql_helper
import config, validate_log

now = datetime.datetime.now()
now_str = now.strftime("%Y-%m-%d %H:%M:%S")
now_id = now.strftime("%Y%m%d%H%M%S")

def validate_purchase_ui(config, reportId, sql_insert_data_list=[]):
    with open(r"logs/TS_CFS_SmokeTest/{0}/{0}.csv".format(reportId)) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        for (flow, step_info) in config.autotest_category.items():
            step_go = True
            for (step, item) in step_info.items():
                if step_go:
                    is_success = False
                    for row in readCSV:
                        if row[0] == item[1] and row[6] != 'PASSED':
                            is_success = True
                            break
                    if is_success:
                        sql_insert_data_list.append((now_id, country, step, item[0], 1, '', now_str))
                    else:
                        sql_insert_data_list.append((now_id, country, step, item[0], 0, '', now_str))
                        step_go = False
                else:
                    sql_insert_data_list.append((now_id, country, step, item[0], 2, '', now_str))
    return sql_insert_data_list
            
def validate_payment_log(config, sql_insert_data_list=[], is_skip=False):    
    error_log = ""
    if is_skip == False:
        log_data = file_helper.read_file_json('log_data.json')
        for server in config.nginx_server[country]:
            print(server)
        
            last_log_time = log_helper.get_payment_lastlogtime(log_data, server)
            (last_log_time, list_error_log) = validate_log.validate_log(server, last_log_time, slack=config.slack, email_receivers=config.email_receiver)    
            print(last_log_time)
            log_data = log_helper.update_payment_lastlogtime(log_data, server, last_log_time)
            if len(list_error_log) > 0:
                error_log = error_log + str(list_error_log)    
        print(log_data)
        file_helper.save_file_json('log_data.json', log_data)

        sql_insert_data_list.append((now_id, country, 3, 3, (0 if error_log!='' else 1), error_log, now_str))
    else:
        sql_insert_data_list.append((now_id, country, 3, 3, 2, '', now_str))

    return sql_insert_data_list

if __name__ == "__main__":
    #init data what need (format data&time, env, country)
    args = sys.argv[1:]
    if not args:
        print("not args")
        env='preview'
        country='HK'
        report_id='20190402_111239'
    else:
        env = args[0]
        country = args[1]
        report_id = args[2]
    print("env:{0}, country:{1}, report_id:{2}".format(env, country, report_id))

    sql_insert_data_list = []

    is_success_purchase_ui = validate_purchase_ui(config, report_id, sql_insert_data_list)
    #sql_insert_data_list = validate_payment_log(config, sql_insert_data_list, (not is_success_purchase_ui))
    
    ms_Conn = sql_helper.MYSQL(host=config.aws_mysql["host"], user=config.aws_mysql["user"], pwd=config.aws_mysql["pwd"], db=config.aws_mysql["db"])    
    insert_sql = """
        Insert into jobsdb_payment(batch_id, country_code, user_journey, category, response_status, remark, monitor_time, created_time, last_updated_time) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, now(), now())
        """
    print(sql_insert_data_list)
    #ms_Conn.ExecManyQuery(insert_sql, sql_insert_data_list)
    
    sql = "SELECT * FROM jobsdb_payment"
    #reslist = ms_Conn.ExecQuery(sql)
    