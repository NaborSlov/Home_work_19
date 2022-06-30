from flask import abort

from dao.model.user import User, UserSchema
from dao.user import UserDAO
from utils.hash_token_functions import get_hash, generator_token, decode_token


class UserService:
    def __init__(self, dao_user: UserDAO):
        self.dao_user = dao_user

    def get_one(self, uid: int) -> User:
        """
        Получение пользователя по его id
        """
        return self.dao_user.get_one(uid)

    def get_one_by_usernames(self, usernames):
        return self.dao_user.get_by_username(usernames)

    def get_all(self) -> list[User]:
        """
        Получение все пользователей
        """
        return self.dao_user.get_all()

    def put(self, uid: int, user_data: dict):
        """
        Полное изменение данных пользователя
        """
        user = self.dao_user.get_one(uid)

        user.username = user_data.get('username')
        user.password = user_data.get('password')
        user.role = user_data.get('role')

        self.dao_user.put(user)

    def patch(self, uid: int, user_data: dict):
        """
        Частичное изменение данных пользователя
        """
        user = self.dao_user.get_one(uid)

        if 'username' in user_data:
            user.username = user_data.get('username')
        if 'password' in user_data:
            user.password = user_data.get('password')
        if 'role' in user_data:
            user.role = user_data.get('role')

        self.dao_user.put(user)

    def get_token(self, data_user):
        """
        Выдача access_token и refresh_token после проверки пароля пользователя
        """
        # проверяем наличие username и password в полученных данных
        username = data_user.get('username', None)
        password = data_user.get('password', None)
        if None in [username, password]:
            abort(401)
        # получим пользователя по его имени из базы данных
        user = self.dao_user.get_by_username(username)
        # если его нет, выбрасываем ошибку
        if not user:
            return {"error": "Неверные учётные данные"}, 401
        # хешируем пароль из полученных данных
        password_hash = get_hash(password)
        # проверка полученного пароля и из базы данных
        if password_hash != user.password:
            abort(401)
        # сериализируем объект User
        data_user = UserSchema().dump(user)
        # возвращаем access_token и refresh_token
        return generator_token(data_user)

    def get_token_by_refresh(self, data_header: dict):
        """
        Обновление токенов по refresh_token
        """
        # проверка в наличие в заголовке refresh_token
        if 'refresh_token' not in data_header:
            abort(404)

        refresh_token = data_header.get('refresh_token')

        data_user = None
        # декодирование токена
        try:
            data_user = decode_token(refresh_token)
        except Exception as e:
            abort(401)
        # получение пользователя по username из базы данных
        user = self.dao_user.get_by_username(data_user.get('username'))
        # сериализируем полученного пользователя
        data_user = UserSchema().dump(user)
        # возвращаем токены
        return generator_token(data_user)

    def create(self, user_data: dict):
        """
        Создание нового пользователя
        """
        # проверяем полученные данные на наличие ключей username и password
        if 'username' not in user_data or 'password' not in user_data:
            abort(404)
        # хешируем пароль
        user_data['password'] = get_hash(user_data.get('password'))
        # если роль не была указанна, устанавливаем роль user
        user_data['role'] = user_data.get('role', 'user')
        # проверка на то что такого пользователя нет в базе данных
        user = self.dao_user.get_by_username(user_data.get('username'))
        if user:
            abort(404)

        self.dao_user.create(user_data)

    def delete(self, uid: int):
        self.dao_user.delete(uid)
