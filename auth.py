from functools import wraps
from flask import request, jsonify
from config import API_KEY

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                'error_code': 1001,
                'error_msg': 'Missing Authorization header'
            }), 401

        try:
            # Bearer トークンの形式をチェック
            scheme, token = auth_header.split()
            if scheme.lower() != 'bearer':
                return jsonify({
                    'error_code': 1001,
                    'error_msg': "Invalid Authorization header format. Expected 'Bearer ' format."
                }), 401
            
            if token != API_KEY:
                return jsonify({
                    'error_code': 1002,
                    'error_msg': 'Authorization failed'
                }), 403

        except ValueError:
            return jsonify({
                'error_code': 1001,
                'error_msg': "Invalid Authorization header format. Expected 'Bearer ' format."
            }), 401

        return f(*args, **kwargs)
    return decorated
