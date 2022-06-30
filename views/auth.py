from flask import request
from flask_restx import Resource, Namespace
from implemented import user_service

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        """
        Получение access_token и refresh_token после авторизации
        """
        data_user = request.json
        return user_service.get_token(data_user)

    def put(self):
        """
        Обновление access_token и refresh_token по refresh_token
        """
        data_user = request.headers
        return user_service.get_token_by_refresh(data_user)
