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


    # NORMALIZATION
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='users_on_courses' and column_name='grade_normalized'" )
    exists = len(cursor.fetchall()) > 0
    if not exists:
        log("Adding grade_normalized")
        cursor.execute("ALTER TABLE users_on_courses ADD COLUMN grade_normalized real NULL")


    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='users_on_courses' and column_name='number_of_played_videos_normalized'" )
    exists = len(cursor.fetchall()) > 0
    if not exists:
        cursor.execute("ALTER TABLE users_on_courses ADD COLUMN number_of_played_videos_normalized integer NULL")


    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='users_on_courses' and column_name='number_of_interactions_normalized'" )
    exists = len(cursor.fetchall()) > 0
    if not exists:
        log("Adding number_of_interactions_normalized")
        cursor.execute("ALTER TABLE users_on_courses ADD COLUMN number_of_interactions_normalized real NULL")


    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='users_on_courses' and column_name='number_of_activity_days_normalized'" )
    exists = len(cursor.fetchall()) > 0
    if not exists:
        log("Adding number_of_activity_days_normalized")
        cursor.execute("ALTER TABLE users_on_courses ADD COLUMN number_of_activity_days_normalized real NULL")


    #CATEGORIZATION
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='users_on_courses' and column_name='number_of_played_videos_categorized'" )
    exists = len(cursor.fetchall()) > 0
    if not exists:
        log("Adding number_of_played_videos_categorized")
        cursor.execute("ALTER TABLE users_on_courses ADD COLUMN number_of_played_videos_categorized character varying(20) NULL")


    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='users_on_courses' and column_name='number_of_interactions_categorized'" )
    exists = len(cursor.fetchall()) > 0
    if not exists:
        log("Adding number_of_interactions_categorized")
        cursor.execute("ALTER TABLE users_on_courses ADD COLUMN number_of_interactions_categorized character varying(20) NULL")


    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='users_on_courses' and column_name='number_of_activity_days_categorized'" )
    exists = len(cursor.fetchall()) > 0
    if not exists:
        log("Adding number_of_activity_days_categorized")
        cursor.execute("ALTER TABLE users_on_courses ADD COLUMN number_of_activity_days_categorized character varying(20) NULL")



    connection.commit()

except Exception  as e:
    if connection:
        connection.rollback()
    print "Unexpected error:", e
    
finally:
    if connection:
        connection.close()