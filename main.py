# -*- coding: utf-8 -*-
import os, sys, time, datetime, json
import csv
import helpers.file_helper as file_helper
import helpers.log_helper as log_helper
import helpers.sql_helper as sql_helper
import helpers.send_slack as send_slack
import config, validate_katalon_report, validate_datafeed_log

now = datetime.datetime.now()
now_str = now.strftime("%Y-%m-%d %H:%M:%S")
now_id = now.strftime("%Y%m%d%H%M%S")

if __name__ == "__main__":
    #init data what need (format data&time, env, country)
    args = sys.argv[1:]
    if not args:
        print("not args")
        env='Production'
        country='HK'
        report_id='7'
    else:
        env = args[0]
        country = args[1]
        report_id = args[2]
    print("env:{0}, country:{1}, report_id:{2}".format(env, country, report_id))

    sql_insert_data_list = []

    is_success_purchase_ui = validate_katalon_report.validate_purchase_ui(env, country, report_id, sql_insert_data_list)    
    sql_insert_data_list = validate_datafeed_log.validate_payment_log(env, country, sql_insert_data_list, (not is_success_purchase_ui))
    print("sql_insert_data_list: %s" % sql_insert_data_list)
    
    '''
    my_Conn = sql_helper.MYSQL(host=config.aws_sycee_monitor_mysql["host"], user=config.aws_sycee_monitor_mysql["user"], pwd=config.aws_sycee_monitor_mysql["pwd"], db=config.aws_sycee_monitor_mysql["db"])    
    insert_sql = """
        Insert into jobsdb_payment(batch_id, country_code, user_journey, category, response_status, remark, monitor_time, created_time, last_updated_time) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, now(), now())
        """
    my_Conn.ExecManyQuery(insert_sql, sql_insert_data_list)
    '''
    sql = "SELECT * FROM jobsdb_payment"
    #reslist = my_Conn.ExecQuery(sql)
    