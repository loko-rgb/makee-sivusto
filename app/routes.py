from flask import Blueprint, render_template, session, url_for, redirect, request, make_response, current_app
import pandas as pd
import os
import time
from functools import wraps

def update_sesion(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ans = func(*args, **kwargs)
        session["last_use"] = time.time()
        return ans
    return wrapper

main = Blueprint("main", __name__)

db = pd.read_csv("app/logins.csv")

@main.route("/", methods=("GET", "POST"))
@update_sesion
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
@update_sesion
def hilow():
    if not session.get("loggedin", False):
        return render_template("login.html")
    return render_template("hilow.html")

@main.route("/logout", methods=("GET", "POST"))
@update_sesion
def logout():
    session["loggedin"] = False
    return redirect(url_for("main.home"))