from flask_login import UserMixin
from . import db, login_manager, session
from flask import session

@login_manager.user_loader
def load_user(user_id):
    user_type = session.get("user_type")
    if user_type == "student":        
        return Student.query.get(int(user_id))
    if user_type == "canteen":
        return Canteen.query.get(int(user_id))
    if user_type == "teacher":
        return Teacher.query.get(int(user_id))
    

class Student(UserMixin, db.Model):
    __tablename__ = "student"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    section = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)

    def get_role(self):
        return "student"

class Canteen(UserMixin, db.Model):
    __tablename__ = "canteen"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    
    def get_role(self):
        return "canteen"

class Teacher(UserMixin, db.Model):
    __tablename__ = "teacher"
    
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    subject = db.Column(db.String(), nullable=False)
    
    def get_role(self):
        return "teacher"

class Menu(db.Model):
    __tablename__ = "menu"

    id = db.Column(db.Integer(), primary_key=True)
    category = db.Column(db.String(), nullable=False)
    item_name = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    availability = db.Column(db.Boolean(), default=True, nullable=False)

class Orders(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer(), primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey("student.id"))
    menu_id = db.Column(db.Integer(), db.ForeignKey("menu.id"))
    section = db.Column(db.String(), nullable=False)

class Assignments(db.Model):
    __tablename__ = "assignments"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    subject = db.Column(db.String(), nullable=False)
    deadline = db.Column(db.DateTime(), nullable=False)
    links = db.Column(db.String(), nullable=True)
    teacher_id = db.Column(db.Integer(), db.ForeignKey("teacher.id"))