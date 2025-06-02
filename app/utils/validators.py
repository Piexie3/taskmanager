import re
from marshmallow import Schema, fields, validate, ValidationError

class UserRegistrationSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class TaskSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(missing='')
    status = fields.Str(validate=validate.OneOf(['pending', 'in_progress', 'completed']))
    priority = fields.Str(validate=validate.OneOf(['low', 'medium', 'high']))
    due_date = fields.DateTime()

class TaskUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=200))
    description = fields.Str()
    status = fields.Str(validate=validate.OneOf(['pending', 'in_progress', 'completed']))
    priority = fields.Str(validate=validate.OneOf(['low', 'medium', 'high']))
    due_date = fields.DateTime()