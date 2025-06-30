from . import app
from flask_login import login_required
from flask import render_template, redirect, url_for
from datetime import datetime, date as dt
from .functions import roles_required

@app.route('/<role>/<username>/Assignments')
@login_required
@roles_required("student", "teacher")
def assignments(username):
    """
    format for assignment array(passed to "render_template"):
    array = [assignment, assignment, assignment], where:
        assignment = [Assignment name, Subject, Assignment link(if none, put an empty string), Deadline date]
        all the elements in the above array must be strings
    """
    assignments = [["Math HW", "Math", "smthin.html", "1/6/2025"], ["English HW", "English", "", "30/6/2025"], ["Chemistry HW", "Chemistry", "another.html", "3/7/2025"]]

    current_date = datetime.now().date()
    for num in range(len(assignments)):
        given_date = assignments[num][2].split("/")
        date = dt(day = int(given_date[0]), month = int(given_date[1]), year = int(given_date[2]))

        if date < current_date:
            assignments[num].append("green")
        elif date == current_date:
            assignments[num].append("yellow")
        else:
            assignments[num].append("red")

    return render_template('StudentAssignmentPage.html', empty = "", assignments = assignments)

@app.route("/student-login", methods=["GET", "POST"])
def student_login():
    return render_template("login.html", href="url_for('student_register')")

@app.route("/teacher-login", methods=["GET", "POST"])
def teacher_login():
    return render_template("login.html", href="url_for('teacher_register')")

@app.route("/canteen-login", methods=["GET", "POST"])
def canteen_login():
    return render_template("login.html")

@app.route("/student-register")
def student_register():
    render_template("register.html", section=True, subject=False)

@app.route("/teacher-register")
def teacher_register():
    render_template("register.html", section=False, subject=True, href="url_for('teacher_login')")