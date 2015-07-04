import flask
from flask import Flask

app=Flask(__name__)

@app.route("/<filename>")
def static (filename):
    pass

