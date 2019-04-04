# -*- coding: utf-8 -*-
import os, sys, time, datetime,json

def get_payment_lastlogtime(log_json, server, log_date=None):
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

def update_payment_lastlogtime(log_json, server, last_log_time, log_date=None):
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
