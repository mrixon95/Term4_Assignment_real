from main import ma
from models.Option import Option
from schemas.UserSchema import user_schema
from schemas.QuestionSchema import question_schema

from marshmallow.validate import Length, Email, OneOf
from datetime import datetime

class OptionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Option
    
    question = ma.Nested(question_schema)
    option_text = ma.String(required=True)
    
    
option_schema = OptionSchema()
options_schema = OptionSchema(many=True)