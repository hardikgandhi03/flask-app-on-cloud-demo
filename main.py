from flask import Flask, redirect, url_for, render_template, request, session, flash
# from datetime import timedelta

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


app = Flask(__name__)
app.secret_key = "qwerty@#$uiop"
# app.permanent_session_lifetime =  timedelta(minutes=10)
# we can define just as we have defined minutes (days=2)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        # session.permanent = True
        user = request.form["name"]
        city = request.form["city"]
        # print(user)
        # print(city)
        db.collection('Users').add({'name': user, 'city': city})
        session["user"] = user
        session["city"] = city
        flash("Login successful !!")
        return redirect(url_for("userPage"))
    else:
        if "user" in session:
            flash("Already logged in!!")
            return redirect(url_for("userPage"))
        return render_template("login.html")

@app.route("/user")
def userPage():
    if "user" in session:
        user = session["user"]
        city = session["city"]
        return render_template("user.html", user=user)
    else:
        flash("You are not logged in !!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    flash("You have been logged out!!","info")
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)