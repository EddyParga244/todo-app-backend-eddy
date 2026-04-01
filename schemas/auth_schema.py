from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    email = fields.Email(required=True, error_messages={"required": "Email is required."})
    password = fields.Str(required=True, error_messages={"required": "Password is required."}, validate=validate.Regexp(r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*]).{8,}$', error="Password must have at least 8 characters, one uppercase, one number and one special character"))

class ChangePasswordSchema(Schema):
    current_password = fields.Str(required=True, error_messages={"required": "Password is required."}, validate=validate.Regexp(r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*]).{8,}$', error="Password must have at least 8 characters, one uppercase, one number and one special character"))
    new_password = fields.Str(required=True, error_messages={"required": "Password is required."}, validate=validate.Regexp(r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*]).{8,}$', error="Password must have at least 8 characters, one uppercase, one number and one special character"))

class DeleteUserSchema(Schema):
    password = fields.Str(required=True, error_messages={"required": "Password is required."}, validate=validate.Regexp(r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*]).{8,}$', error="Password must have at least 8 characters, one uppercase, one number and one special character"))
