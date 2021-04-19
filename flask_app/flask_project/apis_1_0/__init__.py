from flask import Blueprint
from flask_restful import Api

from flask_project.apis_1_0.users import RegisterUsersResource

# 创建蓝图对象
api = Blueprint('', __name__)

# 用户视图
user_api = Api(api, url_part_order='/api/v1_0')
user_api.add_resource(RegisterUsersResource, '/register')
