import jwt
import random
import string
import json
import hashlib
from bson import ObjectId

SALT = 'secret_salt'


def create_token(user_id):
    """Create JWT token"""

    key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    token = jwt.encode({'user_id': user_id}, key).decode('utf8')
    return token, key


def verify_password(input_hash, password):
    """Verify a password against a SHA256 hashed password"""
    # password_hash = pwd_context.encrypt(password)
    password_hash = hashlib.sha256(SALT.encode() + password.encode()).hexdigest()
    return input_hash == password_hash


def hash_password(password):
    """Create a password SHA256 hash"""
    # password_hash = pwd_context.encrypt(password)
    password_hash = hashlib.sha256(SALT.encode() + password.encode()).hexdigest()
    return password_hash


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


