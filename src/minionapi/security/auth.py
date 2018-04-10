from flask_jwt import JWT, jwt_required,current_identity
from flask import g
from flask import current_app as app
from minionapi.apis.users.model import Users
from minionapi.util import util
from minionapi.models.user import User


class JWTAuth:

    def __init__(self, app):
        self.app = app
        self.uri = app.config['DB_URI']
        self.db = app.config['DATABASE']

    def jwt(self):
        return JWT(self.app, self.authenticate, self.identity)

    def get_user(self, email):
        """Get user from DB and return User object"""
        users = Users(self.db, self.uri)
        result = users.get_by_email(email)
        user = User.user(result)

        return user

    def authenticate(self, username, password):
        """Authentication handler for JWT token"""
        users = Users(self.db, self.uri)
        user = users.get_by_email(username)
        if user == {}:
            return None

        if util.verify_password(user['password'], password):
            u = User.user(user)
            del u.__dict__['password']
            g.current_user = u # set current user in app context
            return u

    def identity(self, payload):
        """Identity handler for JWT token"""
        users = Users(self.uri)
        user_id = payload['identity']
        return users.get(user_id)

