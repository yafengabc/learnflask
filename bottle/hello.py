import gevent.monkey
gevent.monkey.patch_all()
from bottle import route,run,template
import sqlite3
@route('/')
def index():
    return 'hello bottle'
@route('/:name')
def hello(name):
    print('called nmmr')
    return 'hello bottle'+name

run(host='0.0.0.0',server="gevent")


