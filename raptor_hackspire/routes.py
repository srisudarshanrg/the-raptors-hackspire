from . import app, session, db
from flask_login import login_required, login_user, current_user, logout_user
from flask import render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date as dt
from .functions import roles_required, hash_password, check_hash_password, CreateStudent, LoginStudent, CreateTeacher, LoginTeacher, LoginCanteen
from .user_validations import password_equal_confirm_password, unique_username_student, unique_username_teacher
from .models import Student, Teacher, Canteen, Menu, Orders, Assignments

@app.route("/")
@login_required
def home():
    return render_template("home.html", role=current_user.get_role())

@app.route('/Assignments')
@login_required
@roles_required("student", "teacher")
def assignments():
    """
    format for assignment array(passed to "render_template"):
    array = [assignment, assignment, assignment], where:
        assignment = [Assignment name, Subject, Assignment link(if none, put an empty string), Deadline date]
        all the elements in the above array must be strings
    """
#    assignments = [["Math HW", "Math", "smthin.html", "2025-06-01"], ["English HW", "English", "", "2025-07-01"], ["Chemistry HW", "Chemistry", "another.html", "2025-07-03"]]
    assignment_obj = Assignments.query.all()
    assignments = []

    for a in assignment_obj:
        assignments.append([a.name, a.subject, a.links, a.deadline])

    current_date = datetime.now().date()
    for i in range(len(assignments)):
        if assignments[i][3] < current_date:
            assignments[i].append("red")
        elif assignments[i][3] == current_date:
            assignments[i].append("yellow")
        else:
            assignments[i].append("green")
        
    if current_user.get_role() == "student":
        return render_template('StudentAssignmentPage.html', assignments = assignments, role=current_user.get_role())
    elif current_user.get_role() == "teacher":
        return render_template('TeacherAssignmentPage.html', assignments = assignments, role=current_user.get_role())
    elif current_user.get_role() == "canteen":
        return "Canteen owner's account can't have assignments!"


@app.route('/Assignments/Edit', methods=["GET", "POST"])
@login_required
@roles_required("teacher")
def assignments_edit():
    """
    format for assignment array(passed to "render_template"):
    array = [assignment, assignment, assignment], where:
        assignment = [Assignment name, Subject, Assignment link(if none, put an empty string), Deadline date]
        all the elements in the above array must be strings
    """
    assignment_obj = Assignments.query.all()
    assignments = []

    for a in assignment_obj:
        assignments.append([a.name, a.subject, a.links, a.deadline])

    current_date = datetime.now().date()
    for i in range(len(assignments)):
        if assignments[i][3] < current_date:
            assignments[i].append("red")
        elif assignments[i][3] == current_date:
            assignments[i].append("yellow")
        else:
            assignments[i].append("green")

    return render_template('EditableAssignmentPage.html', empty = "", assignments = assignments, role=current_user.get_role())

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
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        teacher = LoginTeacher(username, password)
        if teacher != False:
            login_user(teacher)
            session["user_type"] = "teacher"            
            flash("Logged in sucessfully", "success")
            return redirect(url_for("home"))
        else:
            flash("Incorrect login credentials", "danger")

    return render_template("login.html", href="{{urlFor('teacher_register')}}", title="Teacher Login")

@app.route("/canteen-login", methods=["GET", "POST"])
def canteen_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        canteen = LoginCanteen(username, password)
        if canteen != False:
            login_user(canteen)
            session["user_type"] = "canteen"            
            flash("Logged in sucessfully", "success")
            return redirect(url_for("home"))
        else:
            flash("Incorrect login credentials", "danger")

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
        username_validation = unique_username_student(username)

        results = [username_validation, password_validation]
        if results[0] == True and results[1] == True:
            hashed = hash_password(password)
            message, category = CreateStudent(username, section, hashed)
            flash(f"{message}", category)
            if category == "success":
                redirect(url_for('home'))
            else:
                redirect(url_for("student_register"))
        else:
            for i in results:
                if i != True:
                    flash(f"{i}", category="danger")           

    return render_template("register.html", section=True, subject=False, title="Student Register ")

@app.route("/teacher-register", methods=["GET", "POST"])
def teacher_register():
    if request.method == "POST":
        username = request.form.get("username")
        subject = request.form.get("subject")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        password_validation = password_equal_confirm_password(password, confirm_password)
        username_validation = unique_username_teacher(username)

        results = [username_validation, password_validation]

        if results[0] == True and results[1] == True:
            hashed = hash_password(password)
            message, category = CreateTeacher(username, subject, hashed)
            flash(f"{message}", category)
            if category == "success":
                redirect(url_for("home"))
            else:
                redirect(url_for("teacher_register"))
        else:
            for i in results:
                if i != True:
                    flash(f"{i}", category="danger")

    return render_template("register.html", section=False, subject=True, title="Teacher Register")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("student_login"))