#!/usr/bin/python
import psycopg2 as pg
import sys

class IdSeq(object):
    def __init__(self):
        self.id_sequence=0
    def next(self):
        new_id = self.id_sequence
        self.id_sequence+=1
        return new_id

dict_seq = IdSeq()
user_seq = IdSeq()

course_seq = IdSeq()
users_on_courses_seq = IdSeq()

class Gender(object):
    __tablename__ = "genders"
    def __init__(self, name):
        self.name = name
        self.id = dict_seq.next()

class EducationLevel(object):
    __tablename__ = "education_levels"
    def __init__(self,name):
        self.name = name
        self.id = dict_seq.next()

class Region(object):
    __tablename__ = "regions"
    def __init__(self, name):
        self.name = name
        self.id = dict_seq.next()

class University(object):
    __tablename__ = "universities"
    def __init__(self, name):
        self.name = name
        self.id = dict_seq.next()

class Period(object):
    __tablename__ = "periods"
    def __init__(self, name):
        self.name = name
        self.id = dict_seq.next()       


cache_Genders = {
    "m": Gender("Male"),
    "f": Gender("Female"),
    "o": Gender("Other")
}

cache_Period = {
    "Fall": Period("Fall"),
    "Spring": Period("Spring"),
    "Summer": Period("Summer")
}

cache_EducationLevel={
    "Master's" : EducationLevel("Master's"),
    "Bachelor's": EducationLevel("Bachelor's"),
    "Less than Secondary": EducationLevel("Less than Secondary"),
    "Secondary": EducationLevel("Secondary"),
    "Doctorate": EducationLevel("Doctorate")
}

cache_Region = {}

cache_University = {
    'H': University('Harvard'),
    'M': University('MIT')
}

course_names = {
    '8.02x': 'Electricity and Magnetism',
    'PH278x': 'Human Health and Global Environmental Change',
    '8.MReV': 'Mechanics Review' ,
    'CB22x': 'The Ancient Greek Hero' ,
    'ER22x': 'Justice' ,
    '7.00x': 'Introduction to Biology - The Secret of Life' ,
    '6.00x': 'Introduction to Computer Science and Programming' ,
    '2.01x': 'Elements of Structure',
    '3.091x': 'Introduction to Solid State Chemistry' ,
    'PH207x': 'Health in Numbers: Quantitative Methods in Clinical & Public Health ' ,
    '6.002x': 'Circuits and Electronics' ,
    '14.73x': 'The Challenges of Global Poverty' ,
    'CS50x': 'Introduction to Computer Science I' ,
}



class User(object):
    __tablename__= "users"
    def __init__(self, user_old_id, gender, education_level, year_of_birth):
        self.id = user_seq.next()
        self.user_old_id = user_old_id
        self.gender_id = gender.id if gender else None
        self.education_level_id = education_level.id if education_level else None
        self.year_of_birth = year_of_birth

class Course(object):
    __tablename__="courses"
    def __init__(self, name, year, course_old_id, period, university):
        self.id = course_seq.next()
        self.name = name
        self.course_old_id = course_old_id
        self.period_id = period.id if period else None
        self.university_id = university.id if university else None
        self.year = year

class UserOnCourse(object):
    __tablename__="users_on_courses"
    def __init__(self, raw_data_old_id, region, viewed, explored, certified, grade, registration_date, last_activity_date,number_of_interactions,number_of_activity_days,number_of_played_videos,number_of_chapters_interacted,number_of_post_in_forum, user, course):
        self.id = users_on_courses_seq.next()
        self.raw_data_old_id = raw_data_old_id
        self.region_id = region.id if region else None
        self.viewed = viewed
        self.explored = explored
        self.certified = certified
        self.grade = grade
        self.registration_date = registration_date
        self.last_activity_date = last_activity_date
        self.number_of_interactions = number_of_interactions
        self.number_of_activity_days = number_of_activity_days
        self.number_of_played_videos = number_of_played_videos
        self.number_of_chapters_interacted = number_of_chapters_interacted
        self.number_of_post_in_forum = number_of_post_in_forum
        self.user_id = user.id
        self.course_id = course.id


def load_cache_region(cursor):
    global cache_Region
    cursor.execute("select distinct final_cc_cname_di from raw_data")
    for region in cursor.fetchall():
        region_name = region[0]
        if region_name != None and region_name != 'NA':
            cache_Region[region_name] = Region(region_name)

def get_from_cache(cache, key):
    try: 
        return cache[key]
    except KeyError:
        return None

def test():
    assert(cache_EducationLevel["Less than Secondary"].name == "Less than Secondary")
    connection = pg.connect(dbname="ed", user="postgres", password="postgres", host="localhost", port=5432)
    load_cache_region(connection.cursor())
    for reg in cache_Region:
        print reg, cache_Region[reg].name, cache_Region[reg].id
    uc = UserOnCourse("1", cache_Region["Japan"], True, True, True, 0.1, "aaa", "a", 1, 1, 1, 1, 2)


if __name__ == '__main__':
    test()


