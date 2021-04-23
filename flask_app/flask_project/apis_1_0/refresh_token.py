from flask import request
from flask import jsonify
from flask_restful import Resource

from flask_project.utils.token import refresh_loads_token
from flask_project.utils.token import generate_access_token


class RefreshTokenResource(Resource):
    """
    Refresh the token and get a new business token
    """
    def get(self):
        refresh_token = request.args.get('refresh_token')
        if not refresh_token:
            return jsonify({'code': 404, 'msg': 'ni'})
        payload = refresh_loads_token(refresh_token)
        if not payload:
            return jsonify({'code': 404, 'msg': 'wo'})
        if 'user_id' not in payload:
            return jsonify({'code': 404, 'msg': 'ta'})
        access_token = generate_access_token(user_id=payload['user_id'])
        data = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return jsonify(data)