from flask import Flask,request,session,render_template,Request
import flask
import sqlite3

app=Flask(__name__)

@app.route("/")
def hello():
    app_ctx=app.app_context()
    print(app_ctx.app.name)
    return "hello world",400

@app.route("/send",methods=["POST"])
def post():
    if request.method == "POST":
        print("i get POST")
        dat=request.get_data()
        print(dat.decode())
    else:
        pass
    return "hello"



if __name__=='__main__':
    app.run(debug=True)


