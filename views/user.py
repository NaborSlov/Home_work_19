from flask import request
from flask_restx import Resource, Namespace
from implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def post(self):
        user_data = request.json
        user_service.create(user_data)
        return "", 201, {'location': f"/{user_ns.path}/{user_data.get('username')}"}
