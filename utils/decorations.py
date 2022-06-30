from flask import request, abort
import jwt
from constants import SECRET, ALGO


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'token_access' in request.headers:
            abort(401)

        token = request.headers.get('access_token')

        try:
            jwt.decode(token, SECRET, algorithms=[ALGO])
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)

        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'token_access' in request.headers:
            abort(401)

        token = request.headers.get('access_token')
        data_user = None

        try:
            data_user = jwt.decode(token, SECRET, algorithms=[ALGO])
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)

        role = data_user.get('role')

        if not role or role != 'admin':
            abort(403)

        return func(*args, **kwargs)
    return wrapper
