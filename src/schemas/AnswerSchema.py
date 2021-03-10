from main import ma
from models.Answer import Answer
from schemas.UserSchema import user_schema
from schemas.QuestionSchema import question_schema
from schemas.OptionSchema import option_schema

from marshmallow.validate import Length, Email, OneOf
from datetime import datetime

class AnswerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Answer
    
    user = ma.Nested(user_schema)
    question = ma.Nested(question_schema)
    option = ma.Nested(option_schema)

    
answer_schema = AnswerSchema()
answers_schema = AnswerSchema(many=True)