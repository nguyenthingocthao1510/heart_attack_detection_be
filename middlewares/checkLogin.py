from flask import request
from utils.utils import decode_token
from utils.logger import Logger

logger = Logger('check_login')

def get_logged_in_user():
    logger.debug('Checking for Authorization header...')
    if 'Authorization' not in request.headers:
        logger.error('Authorization header is missing')
        return None
    
    auth_header = request.headers.get('Authorization')
    if not auth_header.startswith("Bearer "):
        logger.error(f'Authorization header format is incorrect: {auth_header}')
        return None

    token = auth_header.split("Bearer ")[-1]
    logger.debug(f'Retrieved token: {token}')

    try:
        user_data = decode_token(token)
        logger.debug(f'Decoded user data: {user_data}')
        return user_data.get('id')
    except Exception as e:
        logger.error(f'Error decoding token: {e}')
        return None

