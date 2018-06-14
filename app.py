import datetime
import os
from flask import Flask, render_template, redirect, url_for
from forms import ItemForm, QueryForm
from models import Items
from database import db_session


app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/", methods=('GET', 'POST'))
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Items(name=form.name.data, quantity=form.quantity.data, description=form.description.data, date_added=datetime.datetime.now())
        db_session.add(item)
        db_session.commit()
        return redirect(url_for('success'))
    return render_template('index.html', form=form)

@app.route("/success")
def success():
    results = []
 
    qry = db_session.query(Items) 
    #print(qry)
    results = qry.all()

    return str(results)
@app.route("/delete", methods=('GET', 'POST'))
def delete_item():
    form = QueryForm()
    if form.validate_on_submit():
        db_session.query(Items).filter_by(name = form.name.data).delete(synchronize_session=False)
        db_session.commit()
        return redirect(url_for('success'))
    return render_template('delete.html', form=form)

@app.route("/query", methods=('GET', 'POST'))
def query_item():
    form = QueryForm()
    if form.validate_on_submit():
        results = db_session.query(Items).filter_by(name = form.name.data).all()
        return str(results)
    return render_template('query.html',form=form)

@app.route("/items/<item>",methods=('GET',))
def disp_item(item):
    results = db_session.query(Items).filter_by(name=item).all()
    if results:
        return str(results)
    else:
        return "404 page not found"

@app.route("/allitems",methods=('GET',))
def disp_all():
    qry = db_session.query(Items)
    results = qry.all()
    return str(results)

if __name__ == '__main__':
    #app.run(host='0.0.0.0')
    app.debug = True
    app.run(host='0.0.0.0',port=5001)
