from flask_app import app
from flask import Flask, render_template, redirect,request,session,flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt= Bcrypt(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    if User.validate(request.form):
        data= {
        "email" : request.form["email"]
    }
        user_in_db= User.check_email(data)
        if user_in_db:
            pw_hash = bcrypt.generate_password_hash(request.form["password"])
            data= {
                "firstname" : request.form["fname"],
                "lastname" : request.form["lname"],
                "email" : request.form["email"],
                "password" : pw_hash
            }
            user_id= User.create(data)
            session["user_id"] = user_id
            session["user_name"] = request.form["fname"]
            return redirect("/dashboard")
    return redirect("/")
        

@app.route("/login", methods=["POST"])
def login():
    data= {
        "email" : request.form["email"]
    }
    user_in_db= User.get_email(data)

    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password,request.form["password"]):
        flash("Invalid Email/Password")
        return redirect("/")
    session["user_id"]= user_in_db.id
    session["user_name"] = user_in_db.first_name
    return redirect("/dashboard")
    
