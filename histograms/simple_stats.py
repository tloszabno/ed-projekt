#!/usr/bin/python
# -*- coding: utf-8 -*-
import psycopg2 as pg
import sys

def log(msg):
    print msg

def list_as_csv(__list):
    s = ""
    for item in __list:
        s += str(item) + ","
    return s[:-1]

def all_records(cursor):
    cursor.execute("select count(*) from raw_data")
    return cursor.fetchone()[0]

def null_statistics(cursor):
    print "#### Statytyki występownia nulli ####"
    all_num = all_records(cursor)
    columns = ['gender', 'final_cc_cname_di', 'loe_di', 'yob', 'grade', 'roles']
    for col in columns:
        query = "SELECT count(*) from raw_data where " + col + " is null OR " + col + " = 'NA'"
        cursor.execute(query)
        null_count = cursor.fetchone()[0]  
        print "{:30s} {:7s}%".format(col, str( round((float(null_count)*100.0/float(all_num)), 3)))
    print "############\n"


def how_many_users_was_in_all_courses(cursor):
    query = """select count(id) from users where id in (
    select user_id from users_on_courses 
        group by user_id
        having count(user_id) = 16
    )"""
    cursor.execute(query)
    return cursor.fetchone()[0]

def how_many_users_not_finished_any_course(cursor):
    query = """
    select count(u.id) from users as u left outer join users_on_courses as uc on uc.user_id = u.id and uc.certified = 0
    where uc.user_id is null
    """
    cursor.execute(query)
    return cursor.fetchone()[0]

def get_users_not_finished_any_course(cursor):
    query = """
    select u.id from users as u left outer join users_on_courses as uc on uc.user_id = u.id and uc.certified = 0
    where uc.user_id is null
    """
    cursor.execute(query)
    return [x[0] for x in cursor.fetchall()]


def get_users_signuped_in_all_courses(cursor):
    query = """
    select user_id from users_on_courses 
        group by user_id
        having count(user_id) = 16
    """
    cursor.execute(query)
    users = [ x[0] for x in cursor.fetchall()]
    return users


def how_many_users_passed_all_courses(cursor):
    query = """
    select count(id) from users where id in (
    select user_id  from users_on_courses 
        where certified = 1
        group by user_id
        having count(user_id) = 16
)
    """
    cursor.execute(query)
    return cursor.fetchone()[0]



def what_is_the_max_in_passed_courses_per_user(cursor):
    query = """
        select user_id, count(user_id) as num from users_on_courses 
        where certified = 1
        group by user_id
        order by num desc
    """
    cursor.execute(query)
    maxc = cursor.fetchall()[0][1]
    return maxc

def get_users_which_passed_max_courses(cursor, max_courses):
    query = """
        select user_id, count(user_id) as num from users_on_courses 
        where certified = 1
        group by user_id
        having count(user_id) = %d 
        order by num desc
    """ % max_courses
    cursor.execute(query)
    users = [x[0] for x in cursor.fetchall()]
    return users

def get_users_with_not_passed_any_course(cursor):
    query = """
        select user_id, count(user_id) as num from users_on_courses 
        where certified = 0
        group by user_id
        having count(user_id) = %d 
        order by num desc
    """ % max_courses
    cursor.execute(query)
    users = [x[0] for x in cursor.fetchall()]
    return users



def how_many_courses_passed_user_avg(cursor):
    query = """select user_id, count(user_id) as num from users_on_courses 
        where certified = 1
        group by user_id
        order by num desc"""
    cursor.execute(query)
    l = [x[1] for x in cursor.fetchall()]
    return float(reduce(lambda x,y: x+y, l)) / len(l)

def how_many_courses_signedup_user_avg(cursor):
    query = """select user_id, count(user_id) as num from users_on_courses 
        group by user_id
        order by num desc"""
    cursor.execute(query)
    l = [x[1] for x in cursor.fetchall()]
    return float(reduce(lambda x,y: x+y, l))/len(l)

def get_users_education_level_stats(cursor, users_id_list):
    query = """
    select el.name, count(el.name) as num from users as u 
    join education_levels as el on u.education_level_id = el.id
    where u.id in (%s)
    group by el.name
    order by num desc
    """ % list_as_csv(users_id_list)
    cursor.execute(query)
    return cursor.fetchall()

def get_users_gender_stats(cursor, users_id_list):
    query = """
    select g.name, count(g.name) as num from users as u 
    join genders as g on u.gender_id = g.id
    where u.id in (%s)
    group by g.name
    order by num desc
    """ % list_as_csv(users_id_list)
    cursor.execute(query)
    return cursor.fetchall()

def get_users_gender_stats(cursor, users_id_list):
    query = """
    select g.name, count(g.name) as num from users as u 
    join genders as g on u.gender_id = g.id
    where u.id in (%s)
    group by g.name
    order by num desc
    """ % list_as_csv(users_id_list)
    cursor.execute(query)
    return cursor.fetchall()

def get_users_years_of_birth_stats(cursor, users_id_list, top=None):
    query = """
    select u.year_of_birth, count(u.year_of_birth) as num from users as u 
    where u.id in (%s) and u.year_of_birth <> 'NA'
    group by u.year_of_birth
    order by num desc
    """ % list_as_csv(users_id_list)
    cursor.execute(query)
    results = cursor.fetchall()
    return results[:top] if top  and top <= len(results) else result

def get_users_finished_at_least_one_course(cursor):
    query = """
    select distinct(u.id) from users as u join users_on_courses as uc on uc.user_id = u.id and uc.certified = 1 order by u.id
    """
    cursor.execute(query)
    return [ x[0] for x in cursor.fetchall() ]


def how_many_users_are_in_given_gender(cursor, gender_name):
    query = """
    select count(u.id) from users as u join genders as g on g.id = u.gender_id where g.name = '%s';
    """ % gender_name
    cursor.execute(query)
    return cursor.fetchone()[0]

def get_education_level_stats_dict(cursor):
    query = """
    select el.name, count(el.name) from education_levels as el join users as u on u.education_level_id = el.id join users_on_courses as uc on uc.user_id = u.id
    group by el.name
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return dict(result)

def get_users_with_grade_over(cursor, grade):
    query = """
    select distinct user_id from users_on_courses
    where grade_normalized >= %f 
    """ % (grade-0.01)
    cursor.execute(query)
    return [x[0] for x in cursor.fetchall()]

def get_users_with_grade(cursor, grade_from, grade_to):
    query = """
    select distinct user_id from users_on_courses
    where grade_normalized <= %f and grade_normalized >= %f 
    """ % ((grade_to+0.01), (grade_from-0.01))
    cursor.execute(query)
    return [x[0] for x in cursor.fetchall()]

def print_relation_between_played_videos_and_grade(cursor):
    users_with_grade_5 = get_users_with_grade(cursor, 5.0, 5.0)
    sum_of_played_videos = 0
    for user_id in users_with_grade_5[:10]:
        cursor.execute("select avg(number_of_played_videos_normalized) from users_on_courses where user_id = %s", (user_id,))
        sum_of_played_videos += cursor.fetchone()[0]
    avg_of_played_videos = sum_of_played_videos / len(users_with_grade_5)   
    print "\n\n* Użytkownikownicy, którzy mieli ocenę 5.0 choć z jednego z kursów, średnio odworzyli %f %% możliwych" % (avg_of_played_videos*10)

    users_with_grade_2 = get_users_with_grade(cursor, 2.0, 2.0)
    sum_of_played_videos = 0
    for user_id in users_with_grade_2:
        cursor.execute("select avg(number_of_played_videos_normalized) from users_on_courses where user_id = %s", (user_id,))
        sum_of_played_videos += cursor.fetchone()[0]

    avg_of_played_videos = sum_of_played_videos / len(users_with_grade_2)   
    print "\n\n* Użytkownikownicy, którzy mieli ocenę 2.0 choć z jednego z kursów, średnio odworzyli %d %% możliwych" % (avg_of_played_videos*10)





def print_user_characteristic(cursor, user_list):
    males_in_courses = how_many_users_are_in_given_gender(cursor, "Male")
    females_in_courses = how_many_users_are_in_given_gender(cursor, "Female")

    education_levels_stats = get_education_level_stats_dict(cursor)

    print ""
    for ed_stat in get_users_education_level_stats(cursor, user_list):
        print "\t|| %s  ||  %d osób ||\t %f%% wszystkich ||" % (ed_stat[0], ed_stat[1],( ed_stat[1]*100.0 / education_levels_stats[ed_stat[0]]) )
    print ""
    for ed_stat in get_users_gender_stats(cursor, user_list):
        print "\t|| %s  ||  %d osób ||\t %f%% wszystkich ||" % (ed_stat[0], ed_stat[1], (ed_stat[1]*100.0 / males_in_courses if ed_stat[0] == "Male" else ed_stat[1]*100.0 / females_in_courses ))

#    print " # Rok urodzenia użytkowników: (Top5)"

#   for ed_stat in get_users_years_of_birth_stats(cursor, user_list, top=5):
#        print "\t %s  ->  %d osób" % (ed_stat[0], ed_stat[1])


connection = None
try:
    i = 0
    log("Connectiong to db..")
    connection = pg.connect(dbname="ed", user="postgres", password="postgres", host="localhost", port=5432)
    log("Connected")

    cursor = connection.cursor()
    
    null_statistics(cursor)

    males_in_courses = how_many_users_are_in_given_gender(cursor, "Male")
    females_in_courses = how_many_users_are_in_given_gender(cursor, "Female")

    print "\n=== W ilu kursach brali udział użytkownicy ===\n"
    print "|| Kobiet  ||  %d " % females_in_courses
    print "|| Meżczyzn ||  %d"  % males_in_courses

    print ""
    print "* %d użytkowników zapisało się na wszystkie(16) kursy" % how_many_users_was_in_all_courses(cursor)
    print "* %d użytkowników skończyło 16cie kursów" %  how_many_users_passed_all_courses(cursor)
    print "* %d użytkowników nie skończyło żadnego kursu, na który się zapisało" % how_many_users_not_finished_any_course(cursor)

    max_passed_courses = what_is_the_max_in_passed_courses_per_user(cursor)
    print "* %d kursów było maksimum ukończonym przez jedną osobę" % max_passed_courses

    users_signedup_to_all_courses = get_users_signuped_in_all_courses(cursor)
    print "* użytkownicy, który zapisali się na wszystkie(16) kursy " + str(users_signedup_to_all_courses)

    users_passed_max_courses = get_users_which_passed_max_courses(cursor, max_passed_courses)
    print ("* użytkownicy, którzy skończyli %d kursów " % max_passed_courses )+ str(users_passed_max_courses)

    users_signed_up_for_all_courses_and_in_max_passed = [ u for u in users_signedup_to_all_courses if u in users_passed_max_courses ]
    print "* użytkonicy wspólni dla powyższych dwóch zbiorów " + str(users_signed_up_for_all_courses_and_in_max_passed)

    avg_passed_courses = how_many_courses_passed_user_avg(cursor)
    print "* %f średnio kursów kończyli użytkownicy " % avg_passed_courses

    avg_signedup_courses = how_many_courses_signedup_user_avg(cursor)
    print "* Na %f średnio kursów byli zapisani użytkownicy " % avg_signedup_courses

    print "* Stosunek powyższych %f%%" % (avg_passed_courses*100.0/avg_signedup_courses)


    print "\n=== Charakterystyki użytkowników ===\n"
    print "\n* Charakterytyka użytkowników, którzy skończyli najwięcej (%d) kursów:" % max_passed_courses
    print_user_characteristic(cursor, users_passed_max_courses)

    print "\n* Charakterytyka użytkowników, którzy nie skończyli żadnego kursu: " 
    users_with_not_passed_any_course = get_users_not_finished_any_course(cursor)
    print_user_characteristic(cursor, users_with_not_passed_any_course)
    
    print "\n* Charakterytyka użytkowników, którzy skończyli choć jeden kurs: " 
    print_user_characteristic(cursor, get_users_finished_at_least_one_course(cursor))
    

    users_with_5 = get_users_with_grade_over(cursor, 5.0)

    print "\n* Charakterytyka użytkowników, którzy mają 5.0 z przynajmniej jednego kursu: " 
    print_user_characteristic(cursor, users_with_5)

    print "\n* Charakterytyka użytkowników, którzy mają 3.0 z przynajmniej jednego kursu: " 
    print_user_characteristic(cursor, get_users_with_grade(cursor, 3.0, 3.0))

    print "\n\n=== Zależność od oglądniętych materiałów wideo==="
    print_relation_between_played_videos_and_grade(cursor)  

    print ""
    connection.commit()
finally:
    if connection:
        connection.close()