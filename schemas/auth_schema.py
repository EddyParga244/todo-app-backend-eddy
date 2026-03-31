from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    email = fields.Email(required=True, error_messages={"required": "Email is required."})
    password = fields.Str(required=True, error_messages={"required": "Password is required."}, validate=validate.Length(min=6))
