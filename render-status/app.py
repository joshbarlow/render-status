import os

import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
#connection = sqlite3.connect("renders.db")
#cursor = connection.cursor()
# db = SQL("sqlite:///birthdays.db")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        return "post aaa"

    else:
        connection = sqlite3.connect("renders.db")
        connection.row_factory = sqlite3.Row
        c = connection.cursor()
        c.execute('select * from jobs ORDER BY startTime DESC')
        jobs = []
        for r in c.fetchall():

            jodDict = dict(r)

            firstFrame = int(jodDict['firstFrame'])
            lastFrame = int(jodDict['lastFrame'])
            latestFrame = int(jodDict['latestFrame'])

            print("firstFrame: " + str(firstFrame) + " lastFrame: " + str(lastFrame) + " latestFrame: " + str(latestFrame))

            percent = (100.0 / (lastFrame - firstFrame + 1)) * (latestFrame - firstFrame + 1);

            jodDict['progress'] = int(percent)

            jobs.append(jodDict)

        print(jobs)

        return render_template("index.html", jobs = jobs)

@app.route("/update", methods=["POST"])

def update():

    jobName = request.form.get("name")
    firstFrame = request.form.get("firstFrame")
    lastFrame = request.form.get("lastFrame")
    latestFrame = request.form.get("latestFrame")
    length = int(lastFrame) - int(firstFrame) + 1

    # print("submited data - jobName: {}, firstFrame: {}, lastframe: {}, latestFrame: {}, length: {}".format(jobName,firstFrame,lastFrame,latestFrame,length))

    connection = sqlite3.connect("renders.db")
    connection.row_factory = sqlite3.Row
    c = connection.cursor()
    params = (str(jobName))
    c.execute("SELECT * FROM jobs WHERE name = '" + str(jobName) + "'")

    returnVal = "Existing Job Updated"

    if (c.fetchone() == None):
        c.execute("INSERT INTO jobs (name, firstFrame, lastFrame, latestFrame, length) VALUES(?,?,?,?,?)", (jobName,firstFrame,lastFrame,latestFrame, length))
        connection.commit()
        connection.close()
        returnVal = "New Job Created"
    else:
        c.execute("UPDATE jobs SET firstFrame = ?, lastFrame = ?, latestFrame = ?, length = ? WHERE name = ?", (firstFrame,lastFrame,latestFrame,length,jobName))
        connection.commit()
        connection.close()

    return returnVal

@app.route("/submit", methods=["GET"])

def submit():

    return render_template("submit.html")

@app.route("/delete", methods=["POST"])

def delete():

    jobName = request.form.get("name")

    print(jobName)

    connection = sqlite3.connect("renders.db")
    connection.row_factory = sqlite3.Row
    c = connection.cursor()
    params = (str(jobName),)
    c.execute("DELETE FROM jobs WHERE name = ?", params)

    connection.commit()
    connection.close()

    return redirect('/')
