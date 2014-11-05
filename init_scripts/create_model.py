#!/usr/bin/python
import psycopg2 as pg
import sys

def log(msg):
        print msg

RAW_DATA_TABLE_NAME = "raw_data"

drop_tables = '''
DROP TABLE IF EXISTS users_on_courses;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS genders;
DROP TABLE IF EXISTS education_levels;
DROP TABLE IF EXISTS regions;
DROP TABLE IF EXISTS periods;
DROP TABLE IF EXISTS universities;
'''

create_genders_table = '''
CREATE TABLE genders
(
    id serial NOT NULL,
    name character varying(40) NOT NULL,
    CONSTRAINT genders_id_pkey PRIMARY KEY (id)
)
WITH (
    OIDS=FALSE
);
ALTER TABLE genders
    OWNER TO postgres;

'''

create_education_levels_table = '''
CREATE TABLE education_levels
(
    id serial NOT NULL,
    name character varying(40) NOT NULL,
    CONSTRAINT education_levels_id_pkey PRIMARY KEY (id)
)
WITH (
    OIDS=FALSE
);
ALTER TABLE education_levels
    OWNER TO postgres;

'''

create_regions_table = '''
CREATE TABLE regions
(
    id serial NOT NULL,
    name character varying(40) NOT NULL,
    CONSTRAINT regions_id_pkey PRIMARY KEY (id)
)
WITH (
    OIDS=FALSE
);
ALTER TABLE regions
    OWNER TO postgres;

'''

create_periods_table = '''
CREATE TABLE periods
(
    id serial NOT NULL,
    name character varying(40) NOT NULL,
    CONSTRAINT periods_id_pkey PRIMARY KEY (id)
)
WITH (
    OIDS=FALSE
);
ALTER TABLE periods
    OWNER TO postgres;

'''


create_universities_table = '''
CREATE TABLE universities
(
    id serial NOT NULL,
    name character varying(40) NOT NULL,
    CONSTRAINT universities_id_pkey PRIMARY KEY (id)
)
WITH (
    OIDS=FALSE
);
ALTER TABLE universities
    OWNER TO postgres;

'''


create_courses_table = '''
CREATE TABLE courses
(
    id serial NOT NULL,
    course_old_id character varying(40) NOT NULL,
    name character varying(200) NOT NULL,
    period_id integer REFERENCES periods(id),
    university_id integer REFERENCES universities(id),
    year character varying(20) NOT NULL,
    CONSTRAINT courses_id_pkey PRIMARY KEY (id)
)
WITH (
    OIDS=FALSE
);
ALTER TABLE courses
    OWNER TO postgres;

'''
create_users_table = '''


CREATE TABLE users
(
    id serial NOT NULL,
    user_old_id character varying(40),
    education_level_id integer REFERENCES education_levels(id),
    gender_id integer REFERENCES genders(id),
    year_of_birth character varying(20),
    CONSTRAINT users_id_pkey PRIMARY KEY (id)
)
WITH (
    OIDS=FALSE
);
ALTER TABLE users
    OWNER TO postgres;
'''

create_users_on_courses_table = '''
CREATE TABLE users_on_courses
(
    id serial NOT NULL,
    course_id integer REFERENCES courses(id),
    user_id integer REFERENCES users(id),
    raw_data_old_id integer REFERENCES raw_data(id),
    region_id integer REFERENCES regions(id),
    viewed integer,
    explored integer,
    certified integer,
    grade character varying(5),
    registration_date date,
    last_activity_date date,
    number_of_interactions bigint,
    number_of_activity_days integer,
    number_of_played_videos integer,
    number_of_chapters_interacted real,
    number_of_post_in_forum integer,
    CONSTRAINT users_on_courses_pkey PRIMARY KEY (id)
)
WITH (
    OIDS=FALSE
);
ALTER TABLE users_on_courses
    OWNER TO postgres;

'''

connection = None
try:
    log("Connectiong to db..")
    connection = pg.connect(dbname="ed", user="postgres", password="postgres", host="localhost", port=5432)
    log("Connected")

    cursor = connection.cursor()
    log("Dropping tables ")
    cursor.execute(drop_tables)

    log("Creating tables")
    cursor.execute(create_genders_table)
    cursor.execute(create_education_levels_table)
    cursor.execute(create_regions_table)
    cursor.execute(create_universities_table)
    cursor.execute(create_periods_table)

    cursor.execute(create_courses_table)
    cursor.execute(create_users_table)
    cursor.execute(create_users_on_courses_table)

    connection.commit()

finally:
        if connection:
                connection.close()