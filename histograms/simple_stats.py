#!/usr/bin/python
import psycopg2 as pg
import sys

def log(msg):
    print msg

def all_records(cursor):
    cursor.execute("select count(*) from raw_data")
    return cursor.fetchone()[0]

def null_statistics(cursor):
    print "#### Null statistics ####"
    all_num = all_records(cursor)
    columns = ['gender', 'final_cc_cname_di', 'loe_di', 'yob', 'grade', 'roles']
    for col in columns:
        query = "SELECT count(*) from raw_data where " + col + " is null OR " + col + " = 'NA'"
        cursor.execute(query)
        null_count = cursor.fetchone()[0]  
        print "{:30s} {:7s}%".format(col, str( round((float(null_count)*100.0/float(all_num)), 3)))
    print "############"


connection = None
try:
    log("Connectiong to db..")
    connection = pg.connect(dbname="ed", user="postgres", password="postgres", host="localhost", port=5432)
    log("Connected")

    cursor = connection.cursor()
    null_statistics(cursor)




    connection.commit()

finally:
    if connection:
        connection.close()