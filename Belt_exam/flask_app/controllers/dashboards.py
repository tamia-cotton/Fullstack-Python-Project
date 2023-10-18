from flask_app import app
from flask import Flask, render_template, redirect,request,session,flash
from flask_app.models.dashboard import Car
from flask_app.models.user import User

@app.route("/dashboard")
def welcome():
    if "user_id" not in session:
        flash("Must be logged in!!!")
        return redirect("/")
    car = Car.get_all()
    id = session['user_id']
    return render_template("dashboard.html", cars= car, id=id)

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id")
    return redirect("/")

@app.route("/edit/<int:carid>")
def edit_one(carid):
    data={
        "car_id" : carid
    }
    car = Car.get_one(data)
    return render_template("editone.html", car = car)


@app.route("/view/<int:carid>",)
def view_one(carid):
    data={
        "car_id" : carid
    }
    car = Car.get_one(data)
    return render_template("viewone.html", car = car)



@app.route("/newcar")
def new():
    return render_template("newcar.html")

@app.route("/create/<int:num>",  methods= ["POST"])
def create(num):
    data= {
        "make" : request.form["make"],
        "model" : request.form["model"],
        "year" : request.form["year"],
        "desc" : request.form["desc"],
        "price" : request.form["price"],
        "user_id" : num
        }
    Car.create(data)
    return redirect("/dashboard")



@app.route("/edit", methods= ["POST"])
def edit():
    data= {
        "make" : request.form["make"],
        "model" : request.form["model"],
        "year" : request.form["year"],
        "desc" : request.form["desc"],
        "price" : request.form["price"],
            "user_id" : session['user_id']
        }
    Car.update_one(data)
    return redirect("/dashboard")

@app.route("/delete/<int:num>")
def delete(num):
    data= {
        "car_id" : num
    }
    Car.delete(data)
    return redirect("/dashboard")


