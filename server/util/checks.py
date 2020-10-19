from flask import session, redirect, request, url_for
from functools import wraps
from server.util.code import generate_joincode

joinCode = generate_joincode()


def get_code():
    return joinCode


def code_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('joinCode') != joinCode:
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
