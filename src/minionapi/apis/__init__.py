from flask import Blueprint
from flask_restplus import Api
from .users import api as users
from .minions import api as minions


"""
Flask-RESTPlus implementation layout in the format described in documentation
Ref: http://flask-restplus.readthedocs.io/en/stable/scaling.html
"""

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(
    blueprint,
    title='Minion API',
    version='1.0',
    description='Minion API',
    # All API metadatas
)

api.add_namespace(users, path='/users')
api.add_namespace(minions, path='/minions')
