# -*- coding: utf-8 -*-
import os, sys, time, datetime,json
import urllib
import helpers.file_helper as file_helper
import helpers.log_helper as log_helper
import helpers.sql_helper as sql_helper
import config, validate_log

now = datetime.datetime.now()
now_str = now.strftime("%Y-%m-%d %H:%M:%S")
now_id = now.strftime("%Y%m%d%H%M%S")

def validate_payment_log(config, sql_insert_data_list=[], is_skip=False):    
    error_log = ""
    if is_skip == False:
        log_data = file_helper.read_file_json('log_data.json')
        for server in config.nginx_server[country]:
            print(server)
        
            last_log_time = log_helper.get_payment_lastlogtime(log_data, server)
            (last_log_time, list_error_log) = validate_log.validate_log(server, last_log_time, slack_channel=config.slack_channel, email_receivers=config.email_receiver)    
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
    else:
        env = args[0]
        country = args[1]
    print("env:{0}, country:{1}".format(env, country))

    sql_insert_data_list = []
    
    is_success_purchase_ui = False
    sql_insert_data_list = validate_payment_log(config, sql_insert_data_list, (not is_success_purchase_ui))
    
    ms_Conn = sql_helper.MYSQL(host=config.aws_mysql["host"], user=config.aws_mysql["user"], pwd=config.aws_mysql["pwd"], db=config.aws_mysql["db"])    
    insert_sql = """
        Insert into jobsdb_payment(batch_id, country_code, user_journey, category, status, remark, monitor_time, created_time, last_updated_time) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, now(), now())
        """
    print(sql_insert_data_list)
    #ms_Conn.ExecManyQuery(insert_sql, sql_insert_data_list)
    
    sql = "SELECT * FROM jobsdb_payment"
    #reslist = ms_Conn.ExecQuery(sql)
    