from .models import Student, Teacher

def password_equal_confirm_password(password, confirm_password):
    if password == confirm_password:
        return True
    return "Password must equal confirmed password"

def unique_username_student(username):
    check = Student.query.filter_by(username=username).all()
    if len(check) > 0:
        return "This username already exists"
    return True

def unique_username_teacher(username):
    check = Teacher.query.filter_by(username=username).all()
    if len(check) > 0:
        return "This username already exists"
    return True