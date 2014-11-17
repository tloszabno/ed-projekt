#!/usr/bin/python
import psycopg2 as pg
import sys

def log(msg):
        print msg


########
###
### GRADE
###
########
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


########
###
### VIDEOS
###
########


def get_max_played_videos_foreach_course(cursor):
    query_1 = """ select id from courses """
    cursor.execute(query_1)
    courses_ids = [x[0] for x in cursor.fetchall()]
    maxes = {}
    for cid in courses_ids:
        cursor.execute("select max(number_of_played_videos) from users_on_courses where course_id = %s", (cid,))
        maxc = cursor.fetchone()[0]
        maxes[cid] = maxc
    return maxes





def fill_number_of_played_videos_normalized(cursor):
    def normalize(course_id, num_of_playes, courses_max):
        if not num_of_playes: return 0
        max_for_course = courses_max[course_id]
        normalized = int((num_of_playes * 10.0 )/ max_for_course) if max_for_course else 0
        return normalized if normalized > 0 else 1 if max_for_course else 0

    log("Filling number_of_played_videos_normalized...")

    courses_max = get_max_played_videos_foreach_course(cursor)
    cursor.execute("select id,course_id, number_of_played_videos from users_on_courses")
    for row in cursor.fetchall():
        id = row[0]
        course_id = row[1]
        num = row[2]
        normalized = normalize(course_id, num, courses_max)
        cursor.execute("UPDATE users_on_courses SET number_of_played_videos_normalized = %s where id = %s", (normalized, id))

    log("Filling number_of_played_videos_normalized....[OK]")


connection = None
try:
    log("Connectiong to db..")
    connection = pg.connect(dbname="ed", user="postgres", password="postgres", host="localhost", port=5432)
    log("Connected")

    cursor = connection.cursor()

    #fill_grade_normalized(cursor)
    fill_number_of_played_videos_normalized(cursor)

    connection.commit()
finally:
    if connection:
        connection.close()