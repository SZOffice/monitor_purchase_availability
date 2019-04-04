# -*- coding: utf-8 -*-  
import os, sys, time
import json

def read_file_all(path):
    context = ""
    try:
        file_object = open(path)
        context = file_object.read()
        #print(persons)
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
    
def read_file_json(path):
    json_object = {}
    try:
        with open(path, 'r') as f:
            json_object = json.load(f)
    except:
        print("read_file_json error:" + path)
    return json_object

def save_file_json(path, context):
    try:
        with open(path, 'w') as json_file:
            json.dump(context, json_file, ensure_ascii=False)
    except:
        print("save_file_json error:" + path)