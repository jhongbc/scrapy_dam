#!/home/ubuntu/.env/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import MySQLdb.cursors
import sys
import os
import time
import json
#path = os.path.abspath("dbhelper.py").replace("dbhelper.py","")
#sys.path.append(path)

# C9 has some problem with dbhelper.py path so later you can use codes above!
sys.path.append("/home/ubuntu/workspace/scrapy_dam/")
from dbhelper import dbuser_connect

#Setting
path = os.path.abspath("dir.txt").replace("dir.txt","") # To find the path

def run_scrapy():
    delet()
    os.system("scrapy crawl ReservoirState")
    print("Please wait.....")
    for i in range(1,6,1):
        time.sleep(1)
        print(i)
    os.system("scrapy crawl ReservoirState")

def delet():
    if(os.path.isfile('ReservoirState_items1.json')):
        os.remove('ReservoirState_items1.json')
        
    if(os.path.isfile('ReservoirState_items2.json')):
        os.remove('ReservoirState_items2.json')
        
    if(os.path.isfile('check_item1.txt')):
        os.remove('check_item1.txt')
        
    if(os.path.isfile('check_item1.txt')):
        os.remove('check_item2.txt')
#Compare two json file
def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

def convert2list(string):
    s = open(string,"r")
    s_list = s.read().splitlines()
    l = len(s_list)
    object_list = []
    for i in range(0,l,1):
        object_list.append(json.loads(s_list[i]))
    return(object_list)
    
#Link to DB by dbhelper.py
conn = dbuser_connect()
cursor = conn.cursor() 

#run crawl and compare the file then insert into DB
run_scrapy()

for t in range(1,5,1):
    dict_item1 = convert2list(path+"ReservoirState_items1.json")
    dict_item2 = convert2list(path+"ReservoirState_items2.json")
    
    if(ordered(dict_item1) == ordered(dict_item2)):
        l = len(dict_item1)
        #print(l)
        #print(dict_item1)
        for i in range(0,l,1):
            myDict = dict_item1[i]
            # Insert object to mysql 
            a =  list(myDict.values())
            values = '\"' + '\",\"'.join(map(str, a)) + '\"'
            column_name = ', '.join(myDict.keys())
            sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % ("ReservoirState", column_name, values)
            print(i+1,". ",values)
            print(sql)
            cursor.execute(sql)
            conn.commit()
            delet()
        print("Comparison pass and file has been insert into DB table ReservoirState!")
        break
    else:
        print("comparison is fail. Try ",t," times")
        time.sleep(5)
        run_scrapy()

# Close DB link
cursor.close()
conn.close()
