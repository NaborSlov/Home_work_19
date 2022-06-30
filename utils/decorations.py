from flask import request, abort
from utils.hash_token_functions import decode_token


def auth_required(func):
    """
    Проверка token_access
    """
    def wrapper(*args, **kwargs):
        # проверка на наличие токена в заголовке
        if 'token_access' in request.headers:
            abort(401)

        token = request.headers.get('access_token')
        # декодирование токена
        try:
            decode_token(token)
        except Exception as e:
            # если не прошёл декодирование, то вывод ошибки
            print("JWT Decode Exception", e)
            abort(401)

        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    """
    Проверка access_token и роли пользователя
    """
    def wrapper(*args, **kwargs):
        # проверка на наличие токена в заголовке
        if 'token_access' in request.headers:
            abort(401)

        token = request.headers.get('access_token')
        data_user = None

        try:
            data_user = decode_token(token)
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        # получение роли из токена
        role = data_user.get('role')
        # проверка роли
        if not role or role != 'admin':
            abort(403)

        return func(*args, **kwargs)
    return wrapper
