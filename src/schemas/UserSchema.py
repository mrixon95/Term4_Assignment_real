from main import ma
from models.User import User
from marshmallow.validate import Length, Email, OneOf
from datetime import datetime

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_only = ["password"]
    
    first_name = ma.String(required=True, validate=Length(min=2))
    last_name = ma.String(required=True, validate=Length(min=2))
    created_at = ma.DateTime(required=False, default=datetime.now())
    dob = ma.Date(required=True)
    gender = ma.String(required=True, validate=OneOf(["Male", "Female", "Other"]))
    email = ma.String(required=True, validate=Email())
    mobile = ma.String()
    city = ma.String(required=True)
    country = ma.String(required=True)
    password = ma.String(required=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)