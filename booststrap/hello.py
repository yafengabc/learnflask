from flask.ext.bootstrap import Bootstrap
from flask import Flask,render_template,request,Request,session,redirect,url_for
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import Required

class NameForm(Form):
    name=StringField("what is your name",validators=[Required()])
    passwd=PasswordField("what is your passwd",validators=[Required()])
    submit=SubmitField("submit")


app=Flask(__name__)
bootstrap=Bootstrap(app)
app.config['SECRET_KEY']="you need help"

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/user",methods=['GET','POST'])
def user():
    form=NameForm()
    if form.validate_on_submit():
        name=form.name.data
        form.name.data=''
        session['name']=name
        return redirect(url_for('user'))
    return render_template("user.html",name=session['name'],form=form)
@app.route("/<name>.html")
def test(name):
    return app.send_static_file("{0}.html".format(name))
@app.route("/send",methods=['GET','POST'])
def post(): 
    print(request.form["wd"])
    return "Post OK"

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"),404

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)
