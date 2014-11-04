#!/usr/bin/python
import psycopg2 as pg
import sys

def log(msg):
    print msg

RAW_DATA_TABLE_NAME = "raw_data"

create_sql = '''
CREATE TABLE raw_data
(
  id serial NOT NULL,
  course_id character varying(40),
  userid_di character varying(40),
  registered integer,
  viewed integer,
  explored integer,
  certified integer,
  final_cc_cname_di character varying(100),
  loe_di character varying(20),
  yob character varying(20),
  gender character varying(20),
  grade character varying(5),
  start_time_di date,
  last_event_di date,
  nevents bigint,
  ndays_act integer,
  nplay_video integer,
  nchapters real,
  nforum_posts integer,
  roles character varying(20),
  incomplete_flag integer,
  CONSTRAINT raw_data_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE raw_data
  OWNER TO postgres;
'''

copy_sql = '''COPY raw_data(course_id, userid_di, registered, viewed, explored, certified, final_cc_cname_di, loe_di, yob, gender, grade, start_time_di, last_event_di, nevents, ndays_act, nplay_video, nchapters, nforum_posts, roles, incomplete_flag) FROM '/home/tomek/ed/data-raw.csv' DELIMITER ',' CSV HEADER'''


connection = None
try:
    log("Connectiong to db..")
    connection = pg.connect(dbname="ed", user="postgres", password="postgres", host="localhost", port=5432)
    log("Connected")

    cursor = connection.cursor()

    log("Droping table %s" % RAW_DATA_TABLE_NAME)
    cursor.execute("DROP TABLE IF EXISTS " + RAW_DATA_TABLE_NAME)

    log("Creating %s table" % RAW_DATA_TABLE_NAME)
    cursor.execute(create_sql)

    log("Inserting date from file to %s" % (RAW_DATA_TABLE_NAME))
    cursor.execute(copy_sql)

    log("Counting inserted rows...")
    cursor.execute("select count(*) from " + RAW_DATA_TABLE_NAME)
    log(cursor.fetchone()[0])


    connection.commit()

except Exception  as e:
    if connection:
        connection.rollback()
    print "Unexpected error:", e
    
finally:
    if connection:
        connection.close()