from flask import request
from utils.utils import decode_token

def get_logged_in_user():
    if 'Authorization' in request.headers:
        token = request.headers.get('Authorization').split("Bearer ")[-1]
        user_data = decode_token(token)
        return user_data.get('accountId')
    return None

