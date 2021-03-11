from main import ma
from models.Question import Question
from marshmallow.validate import Length, Email, OneOf
from datetime import datetime

class QuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Question
    
    text = ma.String(required=True)

question_schema = QuestionSchema()
questions_schema = QuestionSchema(many=True)