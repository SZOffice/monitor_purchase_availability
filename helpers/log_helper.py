# -*- coding: utf-8 -*-
import os, sys, time, datetime,json
from .sql_helper import Sqlite3

class LogDBHelper:
    def __init__(self, db_path):
        self.now_str = datetime.datetime.now().strftime("%Y-%m-%d")
        is_local_sqlite3 = False
        if os.path.exists(db_path) and os.path.isfile(db_path):
            is_local_sqlite3 = True
        self.sqlite3_conn = Sqlite3(db_path)
        if not is_local_sqlite3:
            create_table_sql = '''CREATE TABLE `validate_nginx_datafeed_log` (
                `id` varchar(50) NOT NULL,
                `server` varchar(20) NOT NULL,
                `last_log_time` varchar(50) DEFAULT NULL,
                `validate_time` varchar(50) DEFAULT NULL,
                PRIMARY KEY (`id`)
            )'''
            self.sqlite3_conn.ExecQuery(create_table_sql)
        #print(self.sqlite3_conn)

    def get_payment_lastlogtime(self, server, log_date=None):
        if log_date == None:
            log_date = self.now_str
        last_log_time = ""
        id = log_date + "-" + server
        sql = "Select `last_log_time` From `validate_nginx_datafeed_log` Where `id`='%s'" % id        
        result = self.sqlite3_conn.ExecQuery(sql)
        print("last_log_time:" + str(result))
        if len(result) == 0:
            self.is_exist_log = False
        else:
            self.is_exist_log = True
            last_log_time = result[0][0]
        print(last_log_time)
        return last_log_time

    def update_payment_lastlogtime(self, server, last_log_time, log_date=None):
        if log_date == None:
            log_date = self.now_str
        id = log_date + "-" + server
        if self.is_exist_log:
            sql = "Update `validate_nginx_datafeed_log` Set `last_log_time`='%s', `validate_time`=datetime('now') Where `id`='%s'" % (last_log_time, id)
        else:
            sql = "Insert into `validate_nginx_datafeed_log` Values ('%s', '%s', '%s', datetime('now'))" % (id, server, last_log_time)
        print(sql)
        self.sqlite3_conn.ExecNonQuery(sql)

class LogFileHelper:
    def __init__(self):
        print('init LogFileHelper')

    def get_payment_lastlogtime(self, log_json, server, log_date=None):
        if log_date == None:
            log_date=datetime.datetime.now().strftime("%Y-%m-%d")
        last_log_time = ""
        if log_date in log_json:
            date_log = log_json[log_date]
            if "payment" in date_log:
                payment_log = date_log["payment"]
                if server in payment_log:
                    server_log = payment_log[server]
                    if "last_log_time" in server_log:
                        last_log_time = server_log["last_log_time"]
        return last_log_time

    def update_payment_lastlogtime(self, log_json, server, last_log_time, log_date=None):
        if log_date == None:
            log_date=datetime.datetime.now().strftime("%Y-%m-%d")
        if log_date in log_json:
            date_log = log_json[log_date]
            if "payment" in date_log:
                payment_log = date_log["payment"]
                if server in payment_log:
                    payment_log[server]["last_log_time"] = last_log_time
                else:
                    payment_log[server] = {"last_log_time": last_log_time}
            else:
                date_log["payment"] = {server: {"last_log_time": last_log_time}}
        else:
            log_json[str(log_date)] = {"payment": {server: {"last_log_time": last_log_time}}}
        return log_json

if __name__ == "__main__":
    helper = LogDBHelper(r"D:\SZOffice\monitor_purchase_availability\logs\local_sqlite3.db")
    helper.get_payment_lastlogtime("hknginx3")
    helper.update_payment_lastlogtime("hknginx3", "02/Apr/2019:12:08:08")