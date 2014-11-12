#!/usr/bin/python
import psycopg2 as pg
import sys

def log(msg):
        print msg


def normalize_grade(grade_srt):
    try:
        grade = float(grade_srt)
        if grade < 0.5:
            return 2.0
        if grade < 0.6:
            return 3.0
        if grade < 0.7:
            return 3.5
        if grade < 0.8:
            return 4.0
        if grade < 0.9:
            return 4.5
        if grade >= 0.0 and grade < 1.0:
            return 5.0
        return 2.0
    except:
        return 2.0


def fill_grade_normalized(cursor):
    log("Filling grade_normalized...")
    cursor.execute("select id, grade from users_on_courses")
    for row in cursor.fetchall():
        id = row[0]
        grade = row[1]
        new_grade = normalize_grade(grade)
        cursor.execute("UPDATE users_on_courses SET grade_normalized = %s where id = %s", (new_grade, id))
    log("Filling grade_normalized....[OK]")

connection = None
try:
    log("Connectiong to db..")
    connection = pg.connect(dbname="ed", user="postgres", password="postgres", host="localhost", port=5432)
    log("Connected")

    cursor = connection.cursor()

    fill_grade_normalized(cursor)

    connection.commit()
finally:
    if connection:
        connection.close()