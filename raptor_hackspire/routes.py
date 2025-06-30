from . import app, session
from flask_login import login_required, login_user, current_user
from flask import render_template, redirect, url_for, request, flash
from datetime import datetime, date as dt
from .functions import roles_required, hash_password, check_hash_password, CreateStudent, LoginStudent
from .user_validations import password_equal_confirm_password, unique_username

@app.route("/")
@login_required
def home():
    return render_template("home.html", role=current_user.get_role)

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
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        student = LoginStudent(username, password)
        if student != False:
            login_user(student)
            session["user_type"] = "student"
            flash("Logged in sucessfully", "success")
            return redirect(url_for("home"))
        else:
            flash("Incorrect login credentials", "danger")

    return render_template("login.html", href="{{urlFor('student_register')}}", title="Student Login")

@app.route("/teacher-login", methods=["GET", "POST"])
def teacher_login():
    return render_template("login.html", href="{{urlFor('teacher_register')}}", title="Teacher Login")

@app.route("/canteen-login", methods=["GET", "POST"])
def canteen_login():
    return render_template("login.html", title="Canteen Login")

@app.route("/student-register", methods=["GET", "POST"])
def student_register():
    if request.method == "POST":
        username = request.form.get("username")
        section = request.form.get("section")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        print(password)

        # validations
        password_validation = password_equal_confirm_password(password, confirm_password)
        username_validation = unique_username(username)

        results = [username_validation, password_validation]
        if results[0] == True and results[1] == True:
            hashed = hash_password(password)
            message, category = CreateStudent(username, section, hashed)
            flash(f"{message}", category)
        else:
            for i in results:
                if i != True:
                    flash(f"{i}", category="danger")           

    return render_template("register.html", section=True, subject=False, title="Student Register")

@app.route("/teacher-register")
def teacher_register():
    return render_template("register.html", section=False, subject=True, title="Teacher Register")