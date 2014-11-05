#!/usr/bin/python
import psycopg2 as pg
import sys
import model
import db_actions

def log(msg):
        print msg


connection = None
try:
    log("Connectiong to db..")
    connection = pg.connect(dbname="ed", user="postgres", password="postgres", host="localhost", port=5432)
    cursor = connection.cursor()
    model.load_cache_region(cursor)

    cursor.execute("select id, course_id, userid_di, registered, viewed, explored, certified, final_cc_cname_di, loe_di, yob, gender, grade, start_time_di, last_event_di, nevents, ndays_act, nplay_video, nchapters, nforum_posts, roles, incomplete_flag from raw_data")

    users_cache = {}
    courses_cache = {}
    users_on_courses_cache = {}

    log("Fetching from raw_data")
    for row in cursor.fetchall():
        course_old_id = row[1]
        course = None
        if course_old_id in courses_cache:
            course = courses_cache[course_old_id]
        else:
            name = model.course_names[course_old_id.split("/")[1].strip()]
            year = course_old_id.split("/")[2].split("_")[0].strip()
            period = model.get_from_cache(model.cache_Period, course_old_id.split("_")[1]) if len(course_old_id.split("_")) > 1 else model.cache_Period['Fall']
            university = model.get_from_cache(model.cache_University, course_old_id[0])
            course = model.Course(name, year, course_old_id, period, university)
            courses_cache[course_old_id] = course

        user_old_id = row[2]
        user = None
        if user_old_id in users_cache:
            user = users_cache[user_old_id]
        else:
            gender = model.get_from_cache(model.cache_Genders, row[10])
            education_level = model.get_from_cache(model.cache_EducationLevel, row[8])
            year_of_birth = row[9]
            user = model.User(user_old_id, gender, education_level, year_of_birth)
            users_cache[user_old_id] = user


        raw_data_old_id = row[0]
        region = model.get_from_cache(model.cache_Region, row[7])
        viewed = row[4]
        explored = row[5]
        certified = row[6]
        grade = row[11]
        registration_date = row[12]
        last_activity_date = row[13]
        number_of_interactions = row[14]
        number_of_activity_days = row[15]
        number_of_played_videos = row[16]
        number_of_chapters_interacted = row[17]
        number_of_post_in_forum = row[18]

        user_on_course = model.UserOnCourse(raw_data_old_id, region, viewed, explored, certified, grade, registration_date, last_activity_date, number_of_interactions, number_of_activity_days, number_of_played_videos, number_of_chapters_interacted, number_of_post_in_forum, user, course)

        users_on_courses_cache[raw_data_old_id] = user_on_course

    log("Saving to db...")
    db_actions.dump_cache(model.cache_Genders, cursor)
    db_actions.dump_cache(model.cache_EducationLevel, cursor)
    db_actions.dump_cache(model.cache_Region, cursor)
    db_actions.dump_cache(model.cache_University, cursor)
    db_actions.dump_cache(model.cache_Period, cursor)


    db_actions.dump_cache(users_cache, cursor)
    db_actions.dump_cache(courses_cache, cursor)
    db_actions.dump_cache(users_on_courses_cache, cursor)

    connection.commit()

finally:
    if connection:
        connection.close()