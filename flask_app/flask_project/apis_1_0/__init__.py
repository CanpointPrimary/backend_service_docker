from flask import Blueprint
from flask_restful import Api

from flask_project.apis_1_0.users import RegisterUsersResource
from flask_project.apis_1_0.users import LoginUserResource
from flask_project.apis_1_0.users import TeachersResource
from flask_project.apis_1_0.refresh_token import RefreshTokenResource

# create blueprint
api = Blueprint('', __name__)

# create views
user_api = Api(api, '/user')
user_api.add_resource(RegisterUsersResource, '/register')
user_api.add_resource(LoginUserResource, '/login')
user_api.add_resource(RefreshTokenResource, '/token')
user_api.add_resource(TeachersResource, '/teacher')
