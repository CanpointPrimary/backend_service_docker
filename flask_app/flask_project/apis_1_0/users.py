from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal
from flask_restful import inputs
from flask_restful.reqparse import RequestParser
from flask import session
from flask import jsonify

from flask_project import db
from models import Users
from flask_project.utils.wechatSDK.wechat import WXSDK_jscode2session
from flask_project.utils.token import generate_access_token
from flask_project.utils.token import generate_refresh_token
from flask_project.utils.token import login_required


class LoginUserResource(Resource):
    """
    Realize the login of ordinary users such as tourists. If you want to further operate and join the class,
    you must obtain the access token through registration
    """
    login_parser = RequestParser()
    login_parser.add_argument('js_code', type=str, required=True)

    login_fields = {
        'session': fields.String,
    }

    def post(self):
        log_args = self.login_parser.parse_args()
        resp = WXSDK_jscode2session(log_args['js_code'])

        if isinstance(resp, dict):
            openid = resp.get('openid')
            user = Users.get(openid)
            if not user:
                Users.add(openid)
            # Update the openID in the cache
            session.update({'openid': openid})
            data = {
                'code': 201,
                'msg': 'login success'
            }
            return marshal(data, self.login_fields)


class RegisterUsersResource(Resource):
    """
    If the user wants to continue other operations (except tourists),
    then according to the logged-in openID,
    find out the corresponding user or corresponding student, and complete the registration.
    If you have already registered, you don’t need to
    """
    register_parser = RequestParser()
    register_parser.add_argument('username', type=str, required=True)
    register_parser.add_argument('nickname', type=str)
    register_parser.add_argument('mobile', type=inputs.regex(r'^1[3-9]\d{9}$'), required=True)
    register_parser.add_argument('email', type=inputs.regex(r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)'
                                                            r'{0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'))
    register_parser.add_argument('-sex', choices=[0, 1], type=int, required=True)
    register_parser.add_argument('age', type=inputs.regex(r'^(\d{4}-\d{1,2}-\d{1,2})$'), required=True)
    register_parser.add_argument('avatar', type=str)
    register_parser.add_argument('-identifyId', choices=[0, 1, 2], type=int, required=True)

    register_fields = {
        'useId': fields.Integer,
        'username': fields.String,
        'nickname': fields.String,
        'mobile': fields.String,
        'sex': fields.Integer,
        'identifyId': fields.Integer,
        'avatar': fields.String,
        'age': fields.String,
        'isActive': fields.Boolean
    }

    def post(self):

        """
        Verify the existence of openID, and then complete the registration
        :return: access_token, refresh_token
        """
        args = self.register_parser.parse_args()
        openid = session.get("openid")
        if openid is None:
            return jsonify({'code': 404, 'msg': 'please login again'})
        user = Users.get(openid)
        if not user.username:
            user.username = args.get('username')
            user.nickname = args.get('nickname')
            user.mobile = args.get('mobile')
            user.email = args.get('email')
            user.sex = args.get('sex')
            user.age = args.get('age')
            user.avatar = args.get('avatar')
            user.identifyId = args.get('identifyId')
            user.isActive = True
            db.session.add(user)
            db.session.commit()

        access_token = generate_access_token(openId=user.openId, identifyId=user.identifyId)
        refresh_token = generate_refresh_token(openId=user.openId, identifyId=user.identifyId)

        data = {
            'code': 201,
            'msg': 'register success',
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return marshal(data, self.register_fields)


class TeachersResource(Resource):

    @login_required
    def get(self):
        return jsonify({'code': 200, 'msg': 'I happy'})





