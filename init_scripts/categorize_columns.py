#!/usr/bin/python
import psycopg2 as pg
import sys

def log(msg):
        print msg


column_map = {
    'number_of_played_videos_normalized'    : 'number_of_played_videos_categorized',
    'number_of_interactions_normalized'     : 'number_of_interactions_categorized',
    'number_of_activity_days_normalized'    : 'number_of_activity_days_categorized'
}

categorize_values = [ 'few', 'normal', 'many' ]

# indexes from - to  ( included )
catagorize_boundaries = {
    'number_of_played_videos_categorized':
        {
            'few'       : (0, 1),
            'normal'    : (2, 25),
            'many'      : (26, 100)
        },
    'number_of_interactions_categorized':
        {
            'few'       : (0, 2),
            'normal'    : (2, 50),
            'many'      : (50, 100)
        },
    'number_of_activity_days_categorized':
        {
            'few'       : (0,5),
            'normal'    : (6,61),
            'many'      : (62,100)
        }
}

def categorize(old_value, boundaries):
    for categorized_val in categorize_values:
        boundary = boundaries[categorized_val]
        if old_value >= boundary[0] and old_value <= boundary[1]:
            return categorized_val


connection = None
try:
    log("Connectiong to db...")
    connection = pg.connect(dbname="ed", user="postgres", password="postgres", host="localhost", port=5432)
    log("Connected")

    cursor = connection.cursor()

    for old_column in column_map.keys():
        new_column = column_map[old_column]

        log("Processing " + new_column)

        boundaries = catagorize_boundaries[new_column]
        cursor.execute("SELECT id," + old_column + " from users_on_courses")
        for row in cursor.fetchall():
            old_value = row[1]
            cursor.execute("UPDATE users_on_courses SET " + new_column + " = %s where id = %s", (categorize(old_value, boundaries), row[0]))

        log(" -> [DONE]")

    connection.commit()

finally:
    if connection:
        connection.close()