## Summary

This repository corrects the manually added bugs in code provided by [system-puzzle](https://github.com/InsightDataScience/systems-puzzle) and adds **query**, **delete** features to the web service. 

## Usage
*	Port 8080 is required to run the service
*	Download the repository and run the following commands 
	```
	docker-compose up -d db
	docker-compose run --rm flaskapp /bin/bash -c "cd /opt/services/flaskapp/src && python -c  'import database; database.init_db()'"
	```
*	After PostgreSQL database is initialized, run the system with
	```
	docker-compose up -d
	```
*	Web service is accessed with `localhost:8080` in any browser
## Web API
* `localhost:8080` adds your items for sell into the data base. When submitted successfully, it redirects to `localhost:8080/success` and displays all items added so far.  
*	`localhost:8080/allitems` displays all items added so far.
*	`localhost:8080/query` provides query for items based on the name in the database.
*	`localhost:8080/items/<name>` provides a list of all items with name matched in the database.
*	`localhost:8080/delete` deletes items with name matched in the database.
## Debug Log
Following the commands above, database is initialized without error message and nginx service is starting. However, access to localhost:8080 gives 
> This site can't be reached
>
That leads me to check docker-compose.yml 

I nginx is not deployed correction on 8080 port. 
>ports:
      - "80:8080"
since checking the syntax manual of docker-compose tells me that the first port is for host and second is for container. 

This is typo and the order should be flipped. Correcting the typo gives me 
> 502 Bad Gateway
> nginx/1.13.5
>
That's a good sign, meaning I have connected to nginx service but something went wrong to bring me the content. Reading the error log on the shell
>connect() failed (111: Connection refused) while connecting to upstream, client: 172.19.0.1, server: localhost, request: "GET / HTTP/1.1", upstream: "http://172.19.0.2:5001/", host: "localhost:8080"
>
I first tried to turn off the firewall on mac but that doesn't help solve the problem. Then I tried a test nginx with empty content. 
```
docker run --name test-nginx -p 8080:80 nginx
```

![alt text](https://github.com/anyuz/anyuzhangpuzzle/blob/master/Screen%20Shot%202018-06-14%20at%203.35.44%20PM.png)

This returns a welcome page on `localhost:8080`, which means that docker is installed correctly and the error must come from the nginx configuration. I found that nginx depends_on: flaskapp. then I checked the `conf.d/flaskapp.conf`
```
proxy_pass http://flaskapp:5001;
```
However, the docker service log reads 
```
flaskapp_1  | * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```
Bad gateway error is a proxy error and flaskapp should be serviced through port 5001 instead of 5000. 
There are python files running in flaskapp container. After checking all of them, I found in app.py:

	if __name__ == '__main__':
		app.run(host='0.0.0.0')
    	
Changing `app.py` 
	
	if __name__ == '__main__':
		app.run(host='0.0.0.0',port=5001)

and I get the correct index.html page. The app.py send proxy setting to the right flaskapp port:

	app.secret_key = os.environ['APP_SECRET_KEY'] 
	
the problem of proxy solved.


![alt text](https://github.com/anyuz/anyuzhangpuzzle/blob/master/Screen%20Shot%202018-06-13%20at%2011.48.25%20AM.png)


After entering one test entry and click submit, the browser redirects me to success page with `[]` as output. After the second entry, it returns `[,]`. Nothing is printed out. Checking the `app.py`, 
```
@app.route("/success")
def success():
    results = []
 
    qry = db_session.query(Items)
    results = qry.all()

    return str(results)
```
Output is returned by a `str` conversion from a list of `Items` object. Checking `models.py` and `database.py`,
```
class Items(Base):
    """
    Items table
    """
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    quantity = Column(Integer)
    description = Column(String(256))
    date_added = Column(DateTime())
```
```
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
```
Class `Items` inherits from `Base`. Both of them have no representations to convert to a string object. Adding the class member function `__repr__()`  solves the problem. 
Reading the flask tutorial and mimic the codes in `app.py`. I added several other features to improve the system.


# Web API Examples

From the details of this project, I know this is a simple system to buy and sell product.
Now, the basic functionality is done. 
Then add more ways to read and write data.
## Read all items in database

    Add route "/allitems " with methods=('GET') in app.py. Type: 'localhost:8080/allitems' can return all items in database.
![alt text](https://github.com/anyuz/anyuzhangpuzzle/blob/master/Screen%20Shot%202018-06-13%20at%2011.48.47%20AM.png)


## Find a specific item by name

### Method 1. 
#### 1. Add route "/query" with methods=('GET', 'POST') in app.py 
#### 2. Create query html page file same like index.html file to get item name.

![alt text](https://github.com/anyuz/anyuzhangpuzzle/blob/master/Screen%20Shot%202018-06-13%20at%2011.52.37%20PM.png)

### Method 2.
Add route "/items/<item name> " with methods=('GET') in app.py. Type: 'localhost:8080/items/<item name>' can return all items in database.

![alt text](https://github.com/anyuz/anyuzhangpuzzle/blob/master/Screen%20Shot%202018-06-13%20at%2011.51.47%20AM.png)

If the item you want to find is not in the database, It will return an error page.

![alt text](https://github.com/anyuz/anyuzhangpuzzle/blob/master/Screen%20Shot%202018-06-13%20at%2011.49.52%20AM.png)



## Delete some items in database

#### 1. Add route "/delete " with methods=('GET','POST') in app.py. delete items by given name:
	db_session.query(Items).filter_by(name = form.name.data).delete(synchronize_session=False)

#### 2. Create delete html page file same like index.html file.

But here, we only need to enter the name of items that want to delete. Type: 'localhost:8080/delete' then enter the items name you want to delete, it will return all items in database after deleting given items.

![alt text](https://github.com/anyuz/anyuzhangpuzzle/blob/master/Screen%20Shot%202018-06-13%20at%2011.49.10%20AM.png)

![alt text](https://github.com/anyuz/anyuzhangpuzzle/blob/master/Screen%20Shot%202018-06-13%20at%2011.49.19%20AM.png)


