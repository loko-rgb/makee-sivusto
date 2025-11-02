from flask import Blueprint, render_template, session, url_for, redirect, request, make_response, current_app
import pandas as pd
import os



main = Blueprint("main", __name__)

db = pd.read_csv("app/logins.csv")

@main.route("/", methods=("GET", "POST"))
def home():
    if request.method == "GET":
        if not session.get("loggedin", False):
            return render_template("login.html")
        return render_template("index.html")

    if request.method == "POST":
        pasw = request.form["psw"]
        usrname = request.form["usrname"]
        if "," in usrname or "," in pasw:
            return render_template("login.html", message="You can not have camas in your username or password")
        global db
        row = db.loc[db["username"]==usrname]

        if row.empty:
            db.loc[len(db)] = {"#":len(db)+1,"username":usrname,"pasw":pasw,"highscore":0}
            db.to_csv('app/logins.csv', index=False)
            session["loggedin"] = True
            return render_template("index.html", message="You created an account")
        
        elif str(pasw) == str(row["pasw"].iloc[0]):
            session["loggedin"] = True
            return render_template("index.html", massage="You are now logged in")
        
        else:
            return render_template("login.html", message="wrong")
        
@main.route("/hilow")
def hilow():
    if not session.get("loggedin", False):
        return render_template("login.html")
    return render_template("hilow.html")

@main.route("/logout", methods=("GET", "POST"))
def logout():
    return redirect(url_for("main.home"))