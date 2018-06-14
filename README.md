# Insight DevOps Engineering Systems Puzzle

## Table of Contents
1. [Understanding the puzzle](README.md#understanding-the-puzzle)
2. [Bugs and Fix](README.md#bugs-and-fix)
3. [Refactoring](README.md#refactoring)
4. [Summary of thoughts](README.md#summary-of-thoughts)

## Understanding the puzzle

## Bugs and Fix

### Bugs1

Based on the docker command, first I try to run the puzzle: 

    docker-compose up


Starting systems-puzzle_db_1 ... done
Starting systems-puzzle_flaskapp_1 ... done
Starting systems-puzzle_nginx_1    ... error

ERROR: for systems-puzzle_nginx_1  Cannot start service nginx: driver failed programming external connectivity on endpoint systems-puzzle_nginx_1 (95a4aa1c0f4b1fa48f6c58752c1a7323301aefc433d98188eb0590b1c5809d7f): Error starting userland proxy: Bind for 0.0.0.0:80: unexpected error (Failure EADDRINUSE)

ERROR: for nginx  Cannot start service nginx: driver failed programming external connectivity on endpoint systems-puzzle_nginx_1 (95a4aa1c0f4b1fa48f6c58752c1a7323301aefc433d98188eb0590b1c5809d7f): Error starting userland proxy: Bind for 0.0.0.0:80: unexpected error (Failure EADDRINUSE)

ERROR: Encountered errors while bringing up the project.

#### Analyze Bug1:







#### Fix1: turn off firewall (fail)




-->port 80 on host is used

#### Fix2: change ports: 80:8080 to 8080:80 (work)


----------------------------------------
### Bugs2

    docker-compose up
        
access localhost:8080 returns bad gateway error

#### Analyze the Bug2:
    
"Containers connected to the same user-defined bridge network automatically expose all ports to each other, and no ports to the outside world. "

#### Fix: add "expose: 80" (work)

But return the other error:

---> can access but not configured correctly

----------------------------------------

### Bugs3

    docker-compose up

502 Bad Gateway

nginx/1.13.5

#### Analyze of Bug3: 

This is a port error in app.py
#### Fix: change port 5000 to 5001 app.run(host='0.0.0.0',port=5001)

-------------------------------------------------------------
### Bugs4

    docker-compose up

    Welcome!
    Please enter items that you would like to sell?
    name  quantity  description  

After enter the name, quantity, description and click enter button, I got the fourth bug:

    Internal Server Error
    The server encountered an internal error and was unable to complete your request. Either the server is overloaded or    there is an error in the application.

#### Analyze Bug4:


#### Fix1. enable debug 

    if __name__ == '__main__':
    app.debug = True


sqlalchemy.exc.ProgrammingError
sqlalchemy.exc.ProgrammingError: (psycopg2.ProgrammingError) relation "items" does not exist
LINE 1: INSERT INTO items (name, quantity, description, date_added) ...
                    ^
 [SQL: 'INSERT INTO items (name, quantity, description, date_added) VALUES (%(name)s, %(quantity)s, %(description)s, %(date_added)s) RETURNING items.id'] [parameters: {'name': 'anyu zhang', 'quantity': '1', 'description': 's', 'date_added': datetime.datetime(2018, 6, 12, 2, 13, 17, 707688)}] (Background on this error at: http://sqlalche.me/e/f405)


#### Fix2. reread the details in the system puzzle readme file

I found the codes:

    docker-compose up -d db
    docker-compose run --rm flaskapp /bin/bash -c "cd /opt/services/flaskapp/src && python -c  'import database; database.init_db()'"

This "bootstraps" the PostgreSQL database with the correct tables. I can run the whole system with:
docker-compose up -d only after that.


-----------------------------------------------------------------
### Bugs5

    docker-compose up -d

insert items but get return results like this  [, , , ], no data show on the page.

Then I check the files like app.py , forms.py, models.py.
I found there is no representative in models.py for class Items, so when try to return str(results), nothing showed on the page.

http://docs.sqlalchemy.org/en/latest/orm/tutorial.html

    Analyze Bug5:
    

#### Fix: 
Add

    def __repr__(self):
    	return "(id='%d',name='%s',quantity='%d',description='%s',date_added='%s')" % (
    		self.id, self.name, self.quantity, self.description, self.date_added)
to Models.py Class Items

to make data visiable on the page.

![alt text](https://github.com/anyuz/anyuzhangpuzzle/blob/master/Screen%20Shot%202018-06-13%20at%2011.48.25%20AM.png)
![alt text](https://github.com/anyuz/anyuzhangpuzzle/blob/master/Screen%20Shot%202018-06-13%20at%2011.48.32%20AM.png)




# Refactoring
From the details of this project, I know this is a simple system to buy and sell product.
Now, the basic functionality is done. 
Then add more ways to read and write data.
## Read all items in database

    Add route "/allitems " with methods=('GET') in app.py. Type: 'localhost:8080/allitems' can return all items in database.
![alt text](https://github.com/anyuz/anyuzhangpuzzle/blob/master/Screen%20Shot%202018-06-13%20at%2011.48.47%20AM.png)


## Find a specific item by name

 ### Method 1. 
        1. Add route "/query" with methods=('GET', 'POST') in app.py 
        2. Create query html page file same like index.html file to get item name.

![alt text](https://github.com/anyuz/anyuzhangpuzzle/blob/master/Screen%20Shot%202018-06-13%20at%2011.52.37%20PM.png)

### Method 2.
Add route "/items/<item name> " with methods=('GET') in app.py. Type: 'localhost:8080/items/<item name>' can return all items in database.

![alt text](https://github.com/anyuz/anyuzhangpuzzle/blob/master/Screen%20Shot%202018-06-13%20at%2011.51.47%20AM.png)


## Delete some items in database

1. Add route "/delete " with methods=('GET','POST') in app.py. 
delete items by given name: db_session.query(Items).filter_by(name = form.name.data).delete(synchronize_session=False)

2. Create delete html page file same like index.html file.

But here, we only need to enter the name of items that want to delete. Type: 'localhost:8080/delete' then enter the items name you want to delete, it will return all items in database after deleting given items.

![alt text](https://github.com/anyuz/anyuzhangpuzzle/blob/master/Screen%20Shot%202018-06-13%20at%2011.49.10%20AM.png)

![alt text](https://github.com/anyuz/anyuzhangpuzzle/blob/master/Screen%20Shot%202018-06-13%20at%2011.49.19%20AM.png)



## Summary of thoughts
comming soon...
