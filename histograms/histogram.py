#!/usr/bin/python
import psycopg2 as pg
import sys
def log(msg):
        print msg

def plot_hist(histogram):
    import numpy as np
    import matplotlib.pyplot as plt
    n = len(histogram.keys())
    ind = np.arange(n)  # the x locations for the groups
    width = 0.35       # the width of the bars

    values = [ histogram[k]  if k in histogram else 0 for k in xrange(n) ]
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, values, width, color='r')
    ax.set_xticklabels( tuple([ str(x) for x in xrange(n)]) )


    plt.show()

connection = None
try:

    if len(sys.argv) != 2:
        print "Put column name in users_on_courses table to print histogram, Usage %s column_name" % sys.argv[0]
        exit()


    log("Connectiong to db..")
    connection = pg.connect(dbname="ed", user="postgres", password="postgres", host="localhost", port=5432)
    log("Connected")

    cursor = connection.cursor()


    column_name = sys.argv[1]
    cursor.execute("SELECT " + column_name + " from users_on_courses")

    histogram = {}
    for row in cursor.fetchall():
        histogram[ row[0] ] = histogram[ row[0] ] + 1 if row[0] in histogram else 1
    #values = [ row[0] for row in cursor.fetchall() ]

    plot_hist(histogram)
    for k in histogram:
        print "%d\t->%d" % (k, histogram[k])


finally:
    if connection:
        connection.close()