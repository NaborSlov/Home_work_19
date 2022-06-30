import calendar
import datetime
import hashlib

import jwt

from constants import HASH_NAME, PWD_HASH_SALT, PWD_HASH_ITERATOR, SECRET, ALGO


def get_hash(password):
    """
    Функция для хеширования пароля
    """
    return hashlib.pbkdf2_hmac(
        HASH_NAME,
        password.encode('utf-8'),
        PWD_HASH_SALT,
        PWD_HASH_ITERATOR
    ).decode('utf-8', 'ignore')


def generator_token(data_user: dict) -> dict:
    """
    Функция для генерации access_token(30 мин) и refresh_token(130 дней)
    """
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data_user['exp'] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data_user, SECRET, algorithm=ALGO)

    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data_user['exp'] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data_user, SECRET, algorithm=ALGO)

    return {'access_token': access_token, 'refresh_token': refresh_token}


def decode_token(token):
    """
    Функция для декодирования токена
    """
    return jwt.decode(token, SECRET, algorithms=ALGO)
