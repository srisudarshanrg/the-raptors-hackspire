from flask_login import current_user
from flask import abort
from functools import wraps

def roles_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.get_role() not in roles:
                abort(401)
            return func(*args, **kwargs)
        return wrapper
    return decorator