#!/usr/bin/python
import psycopg2 as pg
import sys

def log(msg):
        print msg



connection = None
try:
    log("Connectiong to db..")
    connection = pg.connect(dbname="ed", user="postgres", password="postgres", host="localhost", port=5432)
    log("Connected")

    cursor = connection.cursor()

    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='users_on_courses' and column_name='grade_normalized'" )
    exists = len(cursor.fetchall()) > 0
    if not exists:
        cursor.execute("ALTER TABLE users_on_courses ADD COLUMN grade_normalized real NULL")

    # next additions ...


    connection.commit()

except Exception  as e:
    if connection:
        connection.rollback()
    print "Unexpected error:", e
    
finally:
    if connection:
        connection.close()