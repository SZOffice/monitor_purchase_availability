# -*- coding: utf-8 -*-
import os, sys, time, datetime, json
import csv
import helpers.file_helper as file_helper
import helpers.log_helper as log_helper
import helpers.sql_helper as sql_helper
import helpers.send_slack as send_slack
import helpers.logger_helper as logger_helper
import config
from enums import status

now = datetime.datetime.now()
now_str = now.strftime("%Y-%m-%d %H:%M:%S")
now_id = now.strftime("%Y%m%d%H%M%S")
logger = logger_helper.mylog('validate_katalon_report').getlog()

def validate_purchase_ui(steps, country, report_path, sql_insert_data_list=[], is_send_slack=False):
    with open(report_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        step_go = True
        for (step, item) in steps.items():
            if step_go:
                is_success = False
                for row in readCSV:
                    if row[0] == item[1] and row[6] == 'PASSED':
                        is_success = True
                        break
                if is_success:
                    logger.info('katalon passed: country=%s, step=%s, case=%s' % (country, step, item[1]))
                    sql_insert_data_list.append((now_id, country, step, item[0], status.Success, '', now_str))
                else:
                    logger.info('katalon failed: country=%s, step=%s, case=%s' % (country, step, item[1]))
                    if is_send_slack:
                        try:
                            title = '<!here>, this is Katalon failed notification with purchase availability'
                            attachments = [
                                {
                                    "pretext": "--------------",
                                    "title": "Country=%s, Step=%s, Case=%s" %  (country, step, item[1]), 
                                    "text": "Report file path: %s" % report_path, 
                                    "color":"#7CD197",
                                    "ts": int(time.time())
                                }
                            ]
                            send_slack.send_slack(config.slack["token"], config.slack["channel"], title, attachments)
                        except Exception as e:
                            logger.error('send slack error:' + str(e))
                        finally:
                            logger.info('end send slack...')
                    sql_insert_data_list.append((now_id, country, step, item[0], status.Failed, '', now_str))
                    step_go = False
            else:
                logger.info('Skip: country=%s, step=%s, case=%s' % (country, step, item[1]))
                sql_insert_data_list.append((now_id, country, step, item[0], status.NotValid, '', now_str))
    return sql_insert_data_list

if __name__ == "__main__":
    #init data what need (format data&time, env, country)
    args = sys.argv[1:]
    if not args:
        logger.info("not args")
        env='Preview'
        country='HK'
        report_id='7'
    else:
        env = args[0]
        country = args[1]
        report_id = args[2]
    logger.info("env:{0}, country:{1}, report_id:{2}".format(env, country, report_id))

    sql_insert_data_list = []

    is_success_purchase_ui = validate_purchase_ui(env, country, report_id, sql_insert_data_list)
    logger.info("sql_insert_data_list: %s" % sql_insert_data_list)
    