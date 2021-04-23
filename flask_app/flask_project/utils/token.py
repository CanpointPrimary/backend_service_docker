from functools import wraps
import jwt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature
from flask import request
from flask import jsonify
from flask import g

from models import Users
from config import Config


def generate_access_token(openId, identifyId, expires_in=120):
    """
    create business access_token
    :param openId:
    :param identifyId
    :param expires_in: expiration time is two hours
    :return:
    """
    access_it = Serializer(Config.SECRET_KEY, expires_in)
    access_payload = {
        'flag': 0,
        'iss': 'qin',
        'user_id': openId,
        'identify_id': identifyId
    }
    access_token = access_it.dumps(access_payload).decode('utf-8')
    return access_token


def generate_refresh_token(openId, identifyId, expires_in=20160):
    """
    create refresh token
    :param openId:
    :param identifyId
    :param expires_in: expiration time two weeks
    :return:
    """
    refresh_it = Serializer(Config.SECRET_KEY, expires_in)
    refresh_payload = {
        'user_id': openId,
        'identify_id': identifyId,
        'flag': 1,
        'iss': 'qin'
    }
    refresh_token = refresh_it.dumps(refresh_payload).decode('utf-8')
    return refresh_token


def access_loads_token(token, expires_in=120):
    """
    decrypt token
    :param token:
    :param expires_in:
    :return:
    """
    try:
        access_it = Serializer(Config.SECRET_KEY, expires_in)
        payload = access_it.loads(token.encode('utf-8'))
    except BadSignature:
        return jsonify({' msg': 'failure'})
    return payload


def refresh_loads_token(token, expires_in=20160):
    """
    decrypt refresh token
    :param token:
    :param expires_in:
    :return:
    """
    try:
        refresh_it = Serializer(Config.SECRET_KEY, expires_in)
        payload = refresh_it.loads(token.encode('utf-8'))
    except(jwt.ExpiredSignatureError, jwt.InvalidTokenError, jwt.InvalidSignatureError):
        return jsonify({' msg': 'failure'})

    return payload


def identify(token):
    """
    determine the identity of the token
    :param token:
    :return:
    """
    payload = access_loads_token(token)
    if not payload:
        return False
    if 'openId' in payload and 'flag' in payload:
        if payload['flag'] == 1:
            return False
        elif payload['flag'] == 0:
            return payload['openId']
    else:
        return False


def login_required(func):
    """
    login protection
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('access_token', default=None)
        if not token:
            return jsonify({'code': 404, 'msg': 'ni'})
        openId = identify(token)
        if not openId:
            return jsonify({'code': 404, 'msg': 'wo'})
        user = Users.query.filter_by(userId=openId).first()
        if not user:
            return jsonify({'code': 404, 'msg': 'ta'})
        g.user = user
        return func(*args, **kwargs)
    return wrapper