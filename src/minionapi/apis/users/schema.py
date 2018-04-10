from marshmallow import Schema, fields

# Marshmallow schema
class UserSchema(Schema):
    id = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Str()
    password = fields.Str()
    gender = fields.Str()