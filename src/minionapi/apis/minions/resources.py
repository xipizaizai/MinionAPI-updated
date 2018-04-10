from flask import Flask, jsonify, request
from flask_jwt import jwt_required, current_identity
from flask_restplus import reqparse
from flask_restplus import Namespace, Resource
from flask.views import MethodView
from flask import current_app as app
from marshmallow import validates_schema, ValidationError, Schema, fields, pre_load
from minionapi import errors
from . import model


api = Namespace('minions', description='Minions related operations')


# Marshmallow schema
class MinionSchema(Schema):
    id = fields.Str()
    minion_name = fields.Str()


# Marshmallow custom validator
def validate_email(data):
    # email validation regex
    raise ValidationError('email address not valid')


# Schema instances
minion_schema = MinionSchema()
minions_schema = MinionSchema(many=True)


@api.route('', methods=['GET', 'POST', 'PUT'])
class Minions(Resource, MethodView):

    @api.response(200, 'Success')
    @api.response(404, 'Not found')
    @api.response(403, 'Not authorized')
    # @jwt_required()
    def get(self):
        minions = model.Minions(app.config['MONGODB'])
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, location='args')
        args = parser.parse_args()

        if args['email']:
            result = minions.get_by_email(args['email'])
        else:
            result = minions.get_all()

        if result is {}:
            return {}, 404

        _minions = [u.to_json() for u in result]
        return _minions

    @api.expect(fields=minion_schema)
    @api.response(200, 'Success')
    @api.response(400, 'Bad request')
    @api.response(409, 'Minion exists')
    def post(self):
        minions = model.Minions(app.config['MONGODB'])
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize data
        data, err = minion_schema.load(json_data)
        if err:
            return jsonify(err), 422

        try:
            minion = minions.insert(data)
        except errors.DuplicateError as de:
            return {'message': de.message}, 409
        except KeyError as ke:
            return {'message': "Key Missing"}, 500

        _id = str(minion.pk)
        return _id, 200

    @api.response(200, 'Success')
    @api.response(400, 'Bad request')
    @api.response(404, 'Not found')
    def put(self):
        minions = model.Minions(app.config['MONGODB'])
        data = request.get_json()
        if not data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize data
        minion, err = minion_schema.load(data)
        if err:
            return jsonify(err), 422

        result = minions.update(minion)
        if result is 0:
            return {'message': 'Not found'}, 404

        return result, 200


@api.route('/<string:minion_id>')
class MinionsById(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Bad request')
    @api.response(404, 'Not found')
    def get(self, minion_id):
        minions = model.Minions(app.config['MONGODB'])
        result = minions.get(minion_id)
        if result is None:
            return {'message': 'Not found'}, 404

        _minion = result.to_json()
        return _minion, 200

    @api.response(200, 'Success')
    @api.response(400, 'Bad request')
    @api.response(404, 'Not found')
    def delete(self, minion_id):
        minions = model.Minions(app.config['MONGODB'])
        # minion_id = request.args['id']
        result = minions.delete(minion_id)
        if result is 0:
            return {'message': 'Not found'}, 404

        res_string = "Deleted count: {}".format(result)
        return {'message': res_string}, 200
