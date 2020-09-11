#!/usr/bin/python3
import os
import pymysql
import random
from datetime import date
from dotenv import load_dotenv
load_dotenv()

today = date.today()
resultList = []
batch_ids = ""
def DBOption(Action):
    connection = pymysql.connect(host=os.getenv("MONITORING_HOST"),
                                 user="root",
                                 password=os.getenv("MONITORING_PWD"),
                                 port=3306,
                                 db="monitor",
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            if Action == "update":
                print('--------------Update data--------------')
                if len(batch_ids)>0:
                    update_table_sql = "UPDATE jobsdb_purchase SET response_status=1 WHERE id in (%s)" % batch_ids
                    print('updating data id(s):' +batch_ids)
                    cursor.execute(update_table_sql)
                    connection.commit()
                    print('--------------Update Done--------------')
                else:
                    print('option has been refused,no data has been selected for updates.')
            else:
                print('--------------Query Data--------------')
                query_table_sql = "SELECT id FROM jobsdb_purchase WHERE response_status=0 AND DATE(monitor_time) = '%s'" % today
                cursor.execute(query_table_sql)
                results = cursor.fetchall()
                global resultList
                if len(results) > 0:
                    for result in results:
                        resultList += result.values()
                    print('failed id list : '+str(resultList))
                    GetRandomList(resultList)
                else:
                    print("Congratulation! No failed test case in today.")
                 # for row in results:
                 #     print(row[0])
    except Exception as e:
        connection.rollback()
        print(e)
    finally:
        cursor.close()
        connection.close()


def GetRandomList(resultList):
    resultLength = round(len(resultList)*0.8)
    slice = random.sample(resultList, resultLength)
    global batch_ids
    batch_ids = ','.join(str(e) for e in slice)
    print('select in randomly:'+batch_ids+'; total:' + str(resultLength))
    if len(batch_ids)>0:
        # update data
        DBOption("update")
    else:
        print('no data has been selected')


DBOption("Q")

