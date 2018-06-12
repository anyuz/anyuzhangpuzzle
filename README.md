# Insight DevOps Engineering Systems Puzzle

## Table of Contents
1. [Understanding the puzzle](README.md#understanding-the-puzzle)
2. [Bugs and Fix](README.md#bugs-and-fix)
3. [Refactoring](README.md#refactoring)
4. [Summary of thoughts](README.md#summary-of-thoughts)


## Understanding the puzzle

We highly recommend that you take a few dedicated minutes to read this README in its entirety before starting to think about potential solutions. You'll probably find it useful to review the codebase and understand the system at a high-level before attempting to find specific bugs.

## Bugs and Fix

>> docker-compose up

Starting systems-puzzle_db_1 ... done
Starting systems-puzzle_flaskapp_1 ... done
Starting systems-puzzle_nginx_1    ... error

ERROR: for systems-puzzle_nginx_1  Cannot start service nginx: driver failed programming external connectivity on endpoint systems-puzzle_nginx_1 (95a4aa1c0f4b1fa48f6c58752c1a7323301aefc433d98188eb0590b1c5809d7f): Error starting userland proxy: Bind for 0.0.0.0:80: unexpected error (Failure EADDRINUSE)

ERROR: for nginx  Cannot start service nginx: driver failed programming external connectivity on endpoint systems-puzzle_nginx_1 (95a4aa1c0f4b1fa48f6c58752c1a7323301aefc433d98188eb0590b1c5809d7f): Error starting userland proxy: Bind for 0.0.0.0:80: unexpected error (Failure EADDRINUSE)
ERROR: Encountered errors while bringing up the project.

Trial: turn off firewall (fail)
-->port 80 on host is used

Fix1: change ports: 80:8080 to 8080:80

----------------------------------------

>> docker-compose up
access localhost:8080 returns bad gateway error

"Containers connected to the same user-defined bridge network automatically expose all ports to each other, and no ports to the outside world. "
add "expose: 80"
---> can access but not configured correctly

----------------------------------------

1. bug:  port error in docker-compose file

process  tried to fix: 






problem found:

502 Bad Gateway

nginx/1.13.5


2. bug:  port error in app.py

process  tried to fix:  change port 5000 to 5001 app.run(host='0.0.0.0',port=5001)




Welcome!
Please enter items that you would like to sell?
name  quantity  description  




problem found: 

Internal Server Error
The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.

3. bug:  

process  tried to fix:

1. enable debug 

if __name__ == '__main__':
    app.debug = True

sqlalchemy.exc.ProgrammingError
sqlalchemy.exc.ProgrammingError: (psycopg2.ProgrammingError) relation "items" does not exist
LINE 1: INSERT INTO items (name, quantity, description, date_added) ...
                    ^
 [SQL: 'INSERT INTO items (name, quantity, description, date_added) VALUES (%(name)s, %(quantity)s, %(description)s, %(date_added)s) RETURNING items.id'] [parameters: {'name': 'anyu zhang', 'quantity': '1', 'description': 's', 'date_added': datetime.datetime(2018, 6, 12, 2, 13, 17, 707688)}] (Background on this error at: http://sqlalche.me/e/f405)


2. docker-compose up -d db
docker-compose run --rm flaskapp /bin/bash -c "cd /opt/services/flaskapp/src && python -c  'import database; database.init_db()'"

This "bootstraps" the PostgreSQL database with the correct tables. After that you can run the whole system with:
docker-compose up -d



4. bug:   insert items but get return results like this  [, , , ]

process  tried to fix:


  
http://docs.sqlalchemy.org/en/latest/orm/tutorial.html







## Refactoring
* Don't schedule your interview until you've worked on the puzzle 
* To submit your entry please use the link you received in your systems puzzle invitation
* You will only be able to submit through the link one time
* For security, we will not open solutions submitted via files
* Use the submission box to enter the link to your GitHub repo or Bitbucket ONLY
* Link to the specific repo for this project, not your general profile
* Put any comments in the README inside your project repo

## Summary of thoughts



