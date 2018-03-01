#! /usr/bin/env python

import psycopg2


# Defining function to connect to database and return error if connection fails
def connect(database_name="news"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("I am sorry Dave, I'm afraid I can't do that.")


# The next thre 'def' create the sql views for the 3 data queries
# I am choosing to have the python program create the views
# so the user does not have to. However these can be commented
# out if the user wants to build his own views in sql
def articles_by_popularity_view():
    try:
        db, cursor = connect()
        query = "create or replace view articles_by_popularity_view as\
        select title,count(title) as views from articles,log\
        where log.path = concat('/article/',articles.slug)\
        group by title order by views desc"
        cursor.execute(query)
        db.commit()
        db.close()
    except:
        print("Error in creating view articles_by_popularity_view")


def authors_by_popularity_view():
    try:
        db, cursor = connect()
        query = "create or replace view authors_by_popularity_view as select authors.name,\
        count(articles.author) as views from articles, log, authors where\
        log.path = concat('/article/',articles.slug) and\
        articles.author = authors.id group by authors.name order by views desc"
        cursor.execute(query)
        db.commit()
        db.close()
    except:
        print("Error in creating view authors_by_popularity_view")


def log_status_error_view():
    try:
        db, cursor = connect()
        query = "create or replace view log_status_error_view as select Date,Total,Error,\
        (Error::float*100)/Total::float as Percent from\
        (select time::timestamp::date as Date, count(status) as Total,\
        sum(case when status = '404 NOT FOUND' then 1 else 0 end) as Error\
        from log group by time::timestamp::date) as result\
        where (Error::float*100)/Total::float > 1.0 order by Percent desc;"
        cursor.execute(query)
        db.commit()
        db.close()
    except:
        print("Error in creating view log_status_error_view")


# (1) This function will print the three most popular articles.
def articles_by_popularity():
    db, cursor = connect()
    query = "SELECT * from articles_by_popularity_view LIMIT 3;"
    cursor.execute(query)
    data = cursor.fetchall()
    print "\nThe three most popular articles of all time:\n"
    for row in data:
        print row[0], "-", row[1], "views"
    db.close


# (2) This function will print the most popular authors from our database.
def authors_by_popularity():
    db, cursor = connect()
    query = "select * from authors_by_popularity_view limit 3"
    cursor.execute(query)
    data = cursor.fetchall()
    print "\nThe most popular article authors of all time:\n"
    for row in data:
        print row[0], "-", row[1], "views"
    db.close


# This section determines the percent
def log_status_error():
    db, cursor = connect()
    query = "select * from log_status_error_view"
    cursor.execute(query)
    data = cursor.fetchall()
    print "\nDays where more than 1% of requests lead to errors:\n"
    for row in range(0, len(data), 1):
        print str(data[row][0]) + " - "+str(round(data[row][3], 2))+"% errors"
    db.close

# The code below builds the sql views as well as prints the data queries
if __name__ == "__main__":
    # Build the views - these can be commented out- see lines 15-18
    articles_by_popularity_view()
    authors_by_popularity_view()
    log_status_error_view()
    # The following code calls the query functions
    print "\nYour data is being collected:\n"
    articles_by_popularity()
    authors_by_popularity()
    log_status_error()
    print "\nYour data query is now complete.\n"
