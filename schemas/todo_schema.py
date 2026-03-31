from marshmallow import Schema, fields, validate

class TodoSchema(Schema):
    text = fields.Str(required=True, error_messages={"required": "Todo text cannot be empty."}, validate=validate.Length(min=1))
    completed = fields.Boolean()
    position = fields.Integer()
