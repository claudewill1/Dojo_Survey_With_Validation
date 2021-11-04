from flask import render_template, redirect, request, session, flash
from flask_app.models import survey
from flask_app import app

@app.route("/")
def index():
    return render_template("index.html")

# add survey
@app.route("/create/survey",methods=["POST"])
def addSurvey():
    newSurvey = {
        "name": request.form["name"],
        "location": request.form["location"],
        "languages": request.form["languages"],
        "comment": request.form["comment"]
    }
    if not survey.Survey.validateSurvey(newSurvey):
        return redirect("/")
    
    id = survey.Survey.addNewSurvey(newSurvey)
    if not id:
        flash("Something went wrong")
        return redirect("/")
    session["dojo_id"] = id
    return redirect("/result")
    

# show result of most recent survey
@app.route("/result")
def show_results():
    return render_template("result.html",result = survey.Survey.getMostRecentSurvey())
    
