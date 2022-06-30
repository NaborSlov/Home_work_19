from flask import abort

from dao.model.user import User, UserSchema
from dao.user import UserDAO
from utils.hash_token_functions import get_hash, generator_token, decode_token


class UserService:
    def __init__(self, dao_user: UserDAO):
        self.dao_user = dao_user

    def get_one(self, uid: int) -> User:
        return self.dao_user.get_one(uid)

    def get_all(self) -> list[User]:
        return self.dao_user.get_all()

    def put(self, uid: int, user_data: dict):
        user = self.dao_user.get_one(uid)

        user.username = user_data.get('username')
        user.password = user_data.get('password')
        user.role = user_data.get('role')

        self.dao_user.put(user)

    def patch(self, uid: int, user_data: dict):
        user = self.dao_user.get_one(uid)

        if 'username' in user_data:
            user.username = user_data.get('username')
        if 'password' in user_data:
            user.password = user_data.get('password')
        if 'role' in user_data:
            user.role = user_data.get('role')

        self.dao_user.put(user)

    def get_token(self, data_user):
        username = data_user.get('username')
        password = data_user.get('password')

        if None in [username, password]:
            abort(400)

        user = self.dao_user.get_by_username(username)

        if not user:
            return {"error": "Неверные учётные данные"}, 401

        password_hash = get_hash(password)

        if password_hash != user.password:
            return {"error": "Неверные учётные данные"}, 401

        data_user = UserSchema().dump(user)

        return generator_token(data_user)

    def get_token_by_refresh(self, data_header: dict):
        if 'refresh_token' not in data_header:
            abort(400)

        refresh_token = data_header.get('refresh_token')

        data_user = None

        try:
            data_user = decode_token(refresh_token)
        except Exception as e:
            abort(400)

        user = self.dao_user.get_by_username(data_user.get('username'))

        data_user = UserSchema().dump(user)

        return generator_token(data_user)

    def create(self, user_data: dict):
        if 'username' not in user_data or 'password' not in user_data:
            return 401

        user_data['password'] = get_hash(user_data.get('password'))
        user_data['role'] = user_data.get('role', 'user')

        self.dao_user.create(user_data)

    def delete(self, uid: int):
        self.dao_user.delete(uid)
