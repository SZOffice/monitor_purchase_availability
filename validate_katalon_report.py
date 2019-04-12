# -*- coding: utf-8 -*-
import os, sys, time, datetime, json
import csv
import helpers.file_helper as file_helper
import helpers.log_helper as log_helper
import helpers.sql_helper as sql_helper
import helpers.send_slack as send_slack
import config

now = datetime.datetime.now()
now_str = now.strftime("%Y-%m-%d %H:%M:%S")
now_id = now.strftime("%Y%m%d%H%M%S")

def validate_purchase_ui(env, country, reportId, sql_insert_data_list=[]):
    with open(config.path_katalon_report.format(env, reportId)) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        for (flow, step_info) in config.autotest_category.items():
            step_go = True
            for (step, item) in step_info.items():
                if step_go:
                    is_success = False
                    for row in readCSV:
                        if row[0] == item[1] and row[6] == 'PASSED':
                            is_success = True
                            break
                    if is_success:
                        print('katalon passed: country=%s, step=%s, case=%s' % (country, step, item[1]))
                        sql_insert_data_list.append((now_id, country, step, item[0], 1, '', now_str))
                    else:
                        print('katalon failed: country=%s, step=%s, case=%s' % (country, step, item[1]))
                        if config.slack != None:
                            try:
                                title = '<!here>, this is Katalon failed notification with purchase availability'
                                attachments = [
                                    {
                                        "pretext": "--------------",
                                        "title": "Country=%s, Step=%s, Case=%s" %  (country, step, item[1]), 
                                        "text": "Report file path: %s" % config.path_katalon_report.format(env, reportId), 
                                        "color":"#7CD197",
                                        "ts": int(time.time())
                                    }
                                ]
                                send_slack.send_slack(config.slack["token"], config.slack["channel"], title, attachments)
                            except Exception as e:
                                print('send slack error:' + str(e))
                        sql_insert_data_list.append((now_id, country, step, item[0], 0, '', now_str))
                        step_go = False
                else:
                    print('Skip: country=%s, step=%s, case=%s' % (country, step, item[1]))
                    sql_insert_data_list.append((now_id, country, step, item[0], 2, '', now_str))
    return sql_insert_data_list

if __name__ == "__main__":
    #init data what need (format data&time, env, country)
    args = sys.argv[1:]
    if not args:
        print("not args")
        env='Preview'
        country='HK'
        report_id='7'
    else:
        env = args[0]
        country = args[1]
        report_id = args[2]
    print("env:{0}, country:{1}, report_id:{2}".format(env, country, report_id))

    sql_insert_data_list = []

    is_success_purchase_ui = validate_purchase_ui(env, country, report_id, sql_insert_data_list)
    print("sql_insert_data_list: %s" % sql_insert_data_list)
    