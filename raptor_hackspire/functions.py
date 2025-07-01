from flask_login import current_user
from flask import abort
from functools import wraps
from .models import Student, Teacher, Canteen
from . import bcrypt, db, session
from flask_login import login_user

def hash_password(password):
    hashed = bcrypt.generate_password_hash(password).decode(encoding="utf-8")
    return hashed

def check_hash_password(hash_password: bytes, password: str) -> bool:
    return bcrypt.check_password_hash(hash_password, bytes(password, "utf-8"))

def roles_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.get_role() not in roles:
                abort(401)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def CreateStudent(username, section, password):
    try:
        new_student = Student(
            username=username,
            section=section,
            password=password,
        )

        db.session.add(new_student)
        db.session.commit()
        login_user(new_student)
        session["user_type"] = "student"       

        return "User created successfully", "success"
    except Exception as e:
        print(e)
        return f"Failed to create student: {e}", "danger"

def CreateTeacher(username, subject, password):
    try:
        new_teacher = Teacher(
            username=username,
            subject=subject,
            password=password,
        )

        db.session.add(new_teacher)
        db.session.commit()

        login_user(new_teacher)
        session["user_type"] = "teacher"

        return "Account created succesfully", "success"
    except Exception as e:
        print(e)
        return f"Failed to create teacher: {e}", "danger"

def LoginStudent(username, password):
    student = Student.query.filter_by(username=username).first()
    if student:
        check = check_hash_password(student.password, password)
        if check:
            return student
        else:
            return False
    else:
        return False
    
def LoginTeacher(username, password):
    teacher = Teacher.query.filter_by(username=username).first()
    if teacher:
        check = check_hash_password(teacher.password, password)
        if check:
            return teacher
        else:
            return False
    else:
        return False

def LoginCanteen(username, password):
    canteen = Canteen.query.filter_by(username=username).first()
    if canteen:
        check = check_hash_password(canteen.password, password)
        if check:
            return canteen
        else:
            return False
    else:
        return False