from flask import session, redirect, request, url_for
from functools import wraps
from random import randint
def generate_code(n=6):
    join_code = ''.join(["{}".format(randint(0, 9))
                            for num in range(0, n)])
    print("Join code: {}".format(join_code))
    with open('joinCode', 'w') as f:
        f.write(join_code)
    return join_code

joinCode = generate_code()

def get_code():
    return joinCode


def code_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('joinCode') != joinCode:
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
