# -*- coding: utf-8 -*-  
import os, sys, time
import json, csv

def read_file_all(path):
    context = ""
    try:
        file_object = open(path)
        context = file_object.read()
    except:
        print("read_file_all error:" + path)
    finally:
        file_object.close()
    return context
    
def read_file_lines(path):
    lines = []
    try:
        file_object = open(path)
        lines = file_object.readlines()
        #print(persons)
    except:
        print("read_file_lines error:" + path)
    finally:
        file_object.close()
    return lines
    
def save_file(path, context):
    try:
        file_object = open(path, 'w')
        file_object.write(context)
    except:
        print("save_file error:" + path)
    finally:
        file_object.close()

def read_file_json(path):
    json_object = {}
    try:
        with open(path, 'r') as f:
            json_object = json.load(f)
    except Exception as e:
        print("read_file_json %s error: %s" % (path, str(e)))
    return json_object

def save_file_json(path, context):
    try:
        with open(path, 'w') as json_file:
            json.dump(context, json_file, ensure_ascii=False)
    except:
        print("save_file_json error:" + path)

def read_file_csv(path):
    csv_object = []
    try:
        with open(path, 'r') as f:
            readCSV = csv.reader(f, delimiter=',')
            for row in readCSV:
                csv_object.append(row)
    except Exception as e:
        print("read_file_csv %s error: %s" % (path, str(e)))
    return csv_object
