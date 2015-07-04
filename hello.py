import flask
from flask import Flask

app=Flask(__name__)

@app.route("/<filename>")
def static (filename):
    pass

if __name__=='__main__'
    app.run()
