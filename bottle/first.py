#import gevent.monkey
#gevent.monkey.patch_all()
from bottle import route,run,template
import sqlite3
@route('/')
def index():
    db=sqlite3.connect('test.db')
    cur=db.execute('select * from pimark')
    rows=cur.fetchall()
    return  template("first",rows=rows)

@route('/:name')
def hello(name):
    print('called nmmr')
    return 'hello bottle'+name

run(host='0.0.0.0')
#run(host='0.0.0.0',server="paste")


