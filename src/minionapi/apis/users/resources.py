from flask import Flask, jsonify, request
from flask_jwt import jwt_required, current_identity
from flask_restplus import reqparse, fields
from flask_restplus import Namespace, Resource
from flask.views import MethodView
from flask import current_app as app
from marshmallow import validates_schema, ValidationError,  pre_load
from minionapi import errors
from . import model
from .schema import UserSchema

api = Namespace('users', description='Users related operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name', default='minion'),
    'last_name': fields.String(required=True, description='Last name', default='minion'),
    'email': fields.String(required=True, description='The user email', default='minion@backend.team'),
    'gender': fields.String(required=True, description='The user gender', default='female'),
    'dob': fields.String(required=True, description='The user date of birth', default='1984-07-31T00:38:21.702Z'),
})

# ma = Marshmallow(current_app)

# flask_marshmallow schema
# class UserSchema(ma.Schema):
#     class Meta():
#         fields = (
#             'id',
#             'first_name',
#             'last_name',
#             'email',
#             'gender',
#             'dob'
#         )

# class UserSchema(ma.Schema):
#     class Meta:
#         # Fields to expose
#         fields = ('first_name', 'last_name', 'email')





# Marshmallow custom validator
def validate_email(data):
    # email validation regex
    raise ValidationError('email address not valid')


# Schema instances
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@api.route('', methods=['GET', 'POST', 'PUT'])
class Users(Resource, MethodView):

    @api.response(200, 'Success')
    @api.response(404, 'Not found')
    @api.response(403, 'Not authorized')
    # @jwt_required()
    def get(self):
        users = model.Users(app.config['MONGODB'])
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, location='args')
        args = parser.parse_args()

        if args['email']:
            result = users.get_by_email(args['email'])
        else:
            result = users.get_all()

        if result is {}:
            return {}, 404

        _users = [u.to_json() for u in result]
        return _users

    @api.expect(user_model)
    @api.response(200, 'Success')
    @api.response(400, 'Bad request')
    @api.response(409, 'User exists')
    def post(self):
        users = model.Users(app.config['MONGODB'])
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize data
        data = user_schema.load(json_data)
        try:
            user = users.insert(data)
        except errors.DuplicateError as de:
            return {'message': de.message}, 409
        except KeyError as ke:
            return {'message': "Key Missing"}, 500

        _id = str(user.pk)
        return _id, 200


    user_put_model = api.clone('Put', user_model, {
        'id': fields.String(required=True, description='The user ID', default='Input ID')
    })
    @api.response(200, 'Success')
    @api.response(400, 'Bad request')
    @api.response(404, 'Not found')
    @api.expect(user_put_model)
    def put(self):
        users = model.Users(app.config['MONGODB'])
        data = request.get_json()
        if not data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize data
        user = user_schema.load(data)
        result = users.update(user)
        if result is 0:
            return {'message': 'Not found'}, 404

        return result, 200


@api.route('/<string:user_id>')
class UsersById(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Bad request')
    @api.response(404, 'Not found')
    def get(self, user_id):
        users = model.Users(app.config['MONGODB'])
        result = users.get(user_id)
        if result is None:
            return {'message': 'Not found'}, 404

        _user = result.to_json()
        return _user, 200

    @api.response(200, 'Success')
    @api.response(400, 'Bad request')
    @api.response(404, 'Not found')
    def delete(self, user_id):
        users = model.Users(app.config['MONGODB'])
        # user_id = request.args['id']
        result = users.delete(user_id)
        if result is 0:
            return {'message': 'Not found'}, 404

        res_string = "Deleted count: {}".format(result)
        return {'message': res_string}, 200
