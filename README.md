# Insight DevOps Engineering Systems Puzzle

## Table of Contents
1. [Understanding the puzzle](README.md#understanding-the-puzzle)
2. [Bugs and Fix](README.md#bugs-and-fix)
3. [Refactoring](README.md#refactoring)
4. [Summary of thoughts](README.md#summary-of-thoughts)


## Understanding the puzzle

We highly recommend that you take a few dedicated minutes to read this README in its entirety before starting to think about potential solutions. You'll probably find it useful to review the codebase and understand the system at a high-level before attempting to find specific bugs.

## Bugs and Fix

### Bugs1
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
### Bugs2

>> docker-compose up
access localhost:8080 returns bad gateway error

"Containers connected to the same user-defined bridge network automatically expose all ports to each other, and no ports to the outside world. "
add "expose: 80"
---> can access but not configured correctly

----------------------------------------

### Bugs3



>> docker-compose up

502 Bad Gateway

nginx/1.13.5

This is a port error in app.py
change port 5000 to 5001 app.run(host='0.0.0.0',port=5001)

-------------------------------------------------------------
### Bugs4

>> docker-compose up

Welcome!
Please enter items that you would like to sell?
name  quantity  description  

problem found: 

Internal Server Error
The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.

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


-----------------------------------------------------------------
### Bugs5

>> docker-compose up

insert items but get return results like this  [, , , ], no data show on the page.

process  tried to fix:
  
http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
Add:
def __repr__(self):
    	return "(id='%d',name='%s',quantity='%d',description='%s',date_added='%s')" % (
    		self.id, self.name, self.quantity, self.description, self.date_added)
to Models.py Class Items
to make data visiable on the page.




## Refactoring
add check item functions


## Summary of thoughts

1.
2.
3

