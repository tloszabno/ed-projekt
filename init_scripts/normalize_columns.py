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
def normalize_grade(grade_srt, certified):
    try:
        grade = float(grade_srt)
        if grade < 0.5 and certified:
            return 3.0 # fix for inconsistent data
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
        return 5.0
        
    except:
        return 2.0

def fill_grade_normalized(cursor):
    log("Filling grade_normalized...")
    cursor.execute("select id, grade, certified from users_on_courses")
    for row in cursor.fetchall():
        id = row[0]
        grade = row[1]
        certified =  row[2]
        new_grade = normalize_grade(grade,certified)
        cursor.execute("UPDATE users_on_courses SET grade_normalized = %s where id = %s", (new_grade, id))
    log("Filling grade_normalized....[OK]")


########
###
### VIDEOS
###
########

def get_max_value_foreach_course(cursor, column_name):
    query_1 = """ select id from courses """
    cursor.execute(query_1)
    courses_ids = [x[0] for x in cursor.fetchall()]
    maxes = {}
    for cid in courses_ids:
        cursor.execute("select max({}) from users_on_courses where course_id = {}".format(column_name, cid))
        maxc = cursor.fetchone()[0]
        maxes[cid] = maxc
    return maxes

def get_max_played_videos_foreach_course(cursor):
    return get_max_value_foreach_course(cursor, "number_of_played_videos")

def get_max_interactions_foreach_course(cursor):
    return get_max_value_foreach_course(cursor, "number_of_interactions")

def get_max_number_of_activity_days_foreach_course(cursor):    
    return get_max_value_foreach_course(cursor, "number_of_activity_days")

def normalize_value(value, max_):
    if not value: return 0
    normalized = int((value * 100.0 )/ max_) if max_ else 0
    return normalized if normalized > 0 else 1 if max_ else 0

def fill_column_with_normalized_data(old_column, new_column, cursor):
    log("Filling {}".format(new_column))

    courses_max = get_max_value_foreach_course(cursor, old_column)
    cursor.execute("select id,course_id, {} from users_on_courses".format(old_column))
    for row in cursor.fetchall():
        id = row[0]
        course_id = row[1]
        num = row[2]
        normalized = normalize_value(num, courses_max[course_id])
        cursor.execute("UPDATE users_on_courses SET {} = {} where id = {}".format(new_column, normalized, id))

    log(" -> [DONE]")

def fill_number_of_interactions_normalized(cursor):
    fill_column_with_normalized_data("number_of_interactions" ,"number_of_interactions_normalized", cursor)
    
def fill_number_of_activity_days_normalized(cursor):    
    fill_column_with_normalized_data("number_of_activity_days", "number_of_activity_days_normalized", cursor)

def fill_number_of_played_videos_normalized(cursor):
    def normalize(course_id, num_of_playes, courses_max):
        if not num_of_playes: return 0
        max_for_course = courses_max[course_id]
        normalized = int((num_of_playes * 100.0 )/ max_for_course) if max_for_course else 0
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

    log(" -> [DONE]")


connection = None
try:
    log("Connectiong to db..")
    connection = pg.connect(dbname="ed", user="postgres", password="postgres", host="localhost", port=5432)
    log("Connected")

    cursor = connection.cursor()

    fill_grade_normalized(cursor)
    #fill_number_of_played_videos_normalized(cursor)
    #fill_number_of_interactions_normalized(cursor)
    #fill_number_of_activity_days_normalized(cursor)

    connection.commit()
finally:
    if connection:
        connection.close()