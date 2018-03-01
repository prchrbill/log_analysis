# log_analysis
Log analysis project for Udacity FSND
## Introduction
This is a python module that uses information of large database of a web server and draw business conclusions from that information. The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. The database includes three tables:
* The **authors** table includes information about the authors of articles.
* The **articles** table includes the articles themselves.
* The **log** table includes one entry for each time a user has accessed the site.

#### The program produces the following data queries:
* Most popular three articles of all time.
* Most popular article authors of all time.
* Days on which more than 1% of requests lead to errors.

### Functions in newsdb.py:
* **connect():** Connects to the PostgreSQL database and returns a database connection.
* **articles_by_popularity_view():** Creates SQL view articles_by_popularity_view.
* **authors_by_popularity_view():** Creates SQL view authors_by_popularity_view.
* **log_satus_error_view():** Creates SQL view log_satus_error_view.
* **articles_by_popularity():** Prints most popular three articles of all time.
* **authors_by_popularity():** Prints most popular article authors of all time.
* **log_satus_error():** Print days on which more than 1% of requests lead to errors.

### Views Made:
* <h4>articles_by_popularity_view</h4>
```sql
create or replace view articles_by_popularity_view as
select title, count(title) as views from articles,log
where log.path = concat('/article/',articles.slug)
group by title order by views desc
```
* <h4>authors_by_popularity_view</h4>
```sql
create or replace view authors_by_popularity_view as
select authors.name, count(articles.author) as views from articles, log, authors
where log.path = concat('/article/',articles.slug) and articles.author = authors.id
group by authors.name order by views desc
```
* <h4>log_status</h4>
```sql
create or replace view log_satus_error_view as
select Date,Total,Error, (Error::float*100)/Total::float as Percent from
(select time::timestamp::date as Date, count(status) as Total,
sum(case when status = '404 NOT FOUND' then 1 else 0 end) as Error from log
group by time::timestamp::date) as result
where (Error::float*100)/Total::float > 1.0 order by Percent desc;
```

## Instructions
* <h4>Install <a href="https://www.vagrantup.com/">Vagrant</a> and <a href="https://www.virtualbox.org/wiki/Downloads">VirtualBox.</a></h4>
* <h4>Clone the repository to your local machine:</h4>
  <pre>git clone https://github.com/prchrbill/log_analysis</pre>
* <h4>Start the virtual machine</h4>
  From your terminal, inside the project directory, run the command `vagrant up`. This will cause Vagrant to download the Linux           operating   system and install it.
  When vagrant up is finished running, you will get your shell prompt back. At this point, you can run `vagrant ssh` to log in to your     newly installed Linux VM!
* <h4>Download the <a href="https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip">data</a></h4>
  You will need to unzip this file after downloading it. The file inside is called newsdata.sql. Put this file into the vagrant           directory, which is shared with your virtual machine.
* <h4>Setup Database</h4>
  To load the database use the following command:
  <pre>psql -d news -f newsdata.sql;</pre>
* <h4>Run Module</h4>
  <pre>python newsdb.py</pre>
* <h4>The Views<h4>
  Views can be entered manually by enertering 'psql' in your terminal but I have the program do it for you.
  You can comment them out, edit them, etc, just be sure use the view names I have in the program or edit the file
  to match your view name choices.
  
  Have fun!
