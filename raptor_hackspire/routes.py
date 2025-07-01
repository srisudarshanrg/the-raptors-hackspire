from . import app, session, db
from flask_login import login_required, login_user, current_user, logout_user
from flask import render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date as dt
from .functions import roles_required, hash_password, check_hash_password, CreateStudent, LoginStudent, CreateTeacher, LoginTeacher, LoginCanteen
from .user_validations import password_equal_confirm_password, unique_username_student, unique_username_teacher
from .models import Student, Teacher, Canteen, Menu, Orders, Assignments
from datetime import datetime

@app.route("/home")
@login_required
def home():
    loggedIn = False
    if current_user.is_authenticated:
        loggedIn = True
    return render_template("home.html", role=current_user.get_role(), loggedIn=loggedIn, user=current_user)

@app.route("/assignment-student")
@login_required
@roles_required("student")
def assignments_student():
    assignments = []

    assignment_obj = Assignments.query.all()
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
    
    return render_template('StudentAssignmentPage.html', assignments = assignments, role=current_user.get_role())

@app.route('/assignment-teacher', methods=["GET", "POST"])
@login_required
@roles_required("teacher")
def assignments_teacher():
    assignments = []

    if request.method == "POST":
        if "create_assignment" in request.form:
            format_date = "%Y-%m-%d"

            name = request.form.get("name")
            deadline = datetime.strptime(request.form.get("deadline"), format_date)
            links = request.form.get("links")

            new_assignment = Assignments(
                name=name,
                subject=current_user.subject,
                deadline=deadline,
                links=links,
                teacher_id=current_user.id,
            )

            db.session.add(new_assignment)
            db.session.commit()

            return redirect(url_for('assignments_teacher'))

    assignment_obj = Assignments.query.filter_by(teacher_id=current_user.id).all()
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
    
    return render_template('TeacherAssignmentPage.html', assignments = assignments, role=current_user.get_role())

@app.route('/assignments/edit', methods=["GET", "POST"])
@login_required
@roles_required("teacher")
def assignments_edit():
    assignment_obj = Assignments.query.filter_by(teacher_id=current_user.id).all()
    assignments = []

    if request.method == "POST":
        if "edit_assignment_id" in request.form:            
            format_date = "%Y-%m-%d"
            id = request.form.get("edit_assignment_id")
            name = request.form.get("assignment_name")
            assignment_link = request.form.get("assignment_link")
            deadline = datetime.strptime(request.form.get("assignment_deadline"), format_date)

            updated = Assignments.query.filter_by(id=id).first()
            updated.name = name
            updated.assignment_link = assignment_link
            updated.deadline = deadline

            db.session.commit()

            return redirect(url_for("assignments_edit"))
            

    for a in assignment_obj:
        print(a.name)
        assignments.append([a.name, a.subject, a.links, a.deadline, a.id])

    current_date = datetime.now().date()
    for i in range(len(assignments)):
        if assignments[i][3] < current_date:
            assignments[i].append("red")
        elif assignments[i][3] == current_date:
            assignments[i].append("yellow")
        else:
            assignments[i].append("green")

    return render_template('EditableAssignmentPage.html', empty = "", assignments=assignments, role=current_user.get_role())

# student view of canteenMore actions
@app.route("/canteen-buddy", methods=["GET", "POST"])
@login_required
@roles_required("student")
def canteen_buddy():
    menu_items = Menu.query.all()

    menu_names = []
    for m in menu_items:
        if m.availability == True:
            menu_item_dict = {
                "id": m.id,
                "name": m.item_name,
            }
            menu_names.append(menu_item_dict)

    if request.method == "POST":
        if "menu_order_item" in request.form:
            menu_id = int(request.form.get("menu_order_item"))
            new_order = Orders(
                student_id=current_user.id,
                menu_id=menu_id,
                section=current_user.section,
            )
            db.session.add(new_order)
            db.session.commit()
            flash("Your order has been submitted", "success")
            return redirect(url_for("canteen_buddy"))

    return render_template("canteen_buddy.html", role=current_user.get_role(), menu_items=menu_items, menu_order_items=menu_names)

# canteen admin view of canteen buddy
@app.route("/canteen-admin", methods=["GET", "POST"])
@login_required
@roles_required("canteen")
def canteen_admin():
    menu = Menu.query.all()
    orders = Orders.query.all()

    sections = db.session.query(Orders.section).distinct().all()

    order_section_items = []
    for section_tuple in sections:
        section = section_tuple[0]
        section_menu_orders = db.session.query(Orders.menu_id).filter_by(section=section).distinct().all()
        for menu_id_tuple in section_menu_orders:
            menu_id = menu_id_tuple[0]
            menu_item = Menu.query.filter_by(id=menu_id).first()    # for getting menu item name        
            menu_item_count_list = Orders.query.filter_by(section=section, menu_id=menu_id).all() # to get count of menu items in that section
            menu_item_count = len(menu_item_count_list)
            dict_section_menu = {
                "section": section,
                "menu_item": menu_item.item_name,
                "count": menu_item_count,
            }
            order_section_items.append(dict_section_menu)  


    order_items = []
    for order in orders:
        student_details = Student.query.filter_by(id=order.student_id).first()
        menu_details = Menu.query.filter_by(id=order.menu_id).first()
        order_element = {
            "id": order.id,
            "student_name": student_details.username,
            "section": order.section,
            "menu_item": menu_details.item_name,
        }
        order_items.append(order_element)

    if request.method == "POST":
        if "menu_id" in request.form:
            menu_id = request.form.get("menu_id")
            category = request.form.get("category")
            item_name = request.form.get("item_name")
            price = int(request.form.get("price"))
            availability = request.form.get("availability")
            m = Menu.query.filter_by(id=menu_id).first()
            m.category = category
            m.item_name = item_name
            m.price = price
            m.availability = bool(availability)
            db.session.commit()
        if "add_item" in request.form:
            category = request.form.get("category")
            item_name = request.form.get("item_name")
            price = request.form.get("price")
            availability = bool(request.form.get("availability"))

            new_menu_item = Menu(
                category=category,
                item_name=item_name,
                price=price,
                availability=availability,
            )

            db.session.add(new_menu_item)
            db.session.commit()
            return redirect(url_for("canteen_admin"))

        if "menu_id_delete" in request.form:
            item = Menu.query.filter_by(id=int(request.form.get("menu_id_delete"))).first()
            db.session.delete(item)
            db.session.commit()
            return redirect(url_for("canteen_admin"))

        if "order_id_delete" in request.form:
            order = Orders.query.filter_by(id=int(request.form.get("order_id_delete"))).first()
            db.session.delete(order)
            db.session.commit()
            return redirect(url_for("canteen_admin"))

    return render_template("canteen_admin.html", role=current_user.get_role(), menu=menu, orders=order_items, orders_by_section=order_section_items)

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
                return redirect(url_for('home'))
            else:
                return redirect(url_for("student_register"))
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
                return redirect(url_for("home"))
            else:
                return redirect(url_for("teacher_register"))
        else:
            for i in results:
                if i != True:
                    flash(f"{i}", category="danger")

    return render_template("register.html", section=False, subject=True, title="Teacher Register")

@app.route("/")
def login_branch():
    return render_template("login_branch.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login_branch"))