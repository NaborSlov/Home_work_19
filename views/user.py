from flask import request
from flask_restx import Resource, Namespace
from implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def post(self):
        """
        Регистрация нового пользователя
        """
        user_data = request.json
        user_service.create(user_data)
        new_user = user_service.get_one_by_usernames(user_data.get('username'))
        return "", 201, {'location': f"/{user_ns.path}/{new_user.id}"}
