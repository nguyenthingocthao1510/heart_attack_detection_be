import os
from hashlib import pbkdf2_hmac
from dbconfig.app import db
import jwt
from dotenv import load_dotenv

load_dotenv()

def validate_user_input(input_type, **kwargs):
    if input_type == "authentication":
        if len(kwargs["username"]) <= 255 and len(kwargs["password"]) <= 255:
            return True
        else:
            return False

def generate_salt():
    salt = os.urandom(16)
    return salt.hex()

def generate_hash(plain_password, password_salt):
    password_hash = pbkdf2_hmac(
        "sha256",
        b"%b" % bytes(plain_password, "utf-8"),
        b"%b" % bytes(password_salt, "utf-8"),
        10000,
    )
    return password_hash.hex()

def db_write(query, params):
    cursor = db.cursor()
    try:
        cursor.execute(query, params)
        db.commit()
        cursor.close()

        return True

    except Exception as e:
        cursor.close()
        print ('Error: ', str(e))
        return False
    
def db_read(query, params=None):
    cursor = db.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    entries = cursor.fetchall()
    cursor.close()

    content = []

    for entry in entries:
        content.append(entry)

    return content

def generate_jwt_token(content):
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # Pass the name of the environment variable as a string
    if not JWT_SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY is not set in the environment variables")
    
    encoded_content = jwt.encode(content, JWT_SECRET_KEY, algorithm="HS256")  # Use jwt.encode
    token = encoded_content  # The token is already a string in modern versions of PyJWT
    return token

def validate_user(username, password):
    current_user = db_read('''SELECT * FROM account WHERE username = %s''', (username,))

    if len(current_user) == 1:
        saved_password_hash = current_user[0][4]  # password_hash is the 5th column
        saved_password_salt = current_user[0][3]  # password_salt is the 4th column
        password_hash = generate_hash(password, saved_password_salt)

        if password_hash == saved_password_hash:
            user_id = current_user[0][0]  # id is the 1st column
            jwt_token = generate_jwt_token({"id": user_id})
            return jwt_token
        else:
            return False
    else:
        return False



