from main import ma
from schemas.QuestionSchema import question_schema
from schemas.MentalHealthSurveySchema import mental_health_survey_schema
from models.SurveyQuestion import SurveyQuestion
from marshmallow.validate import Length, Email, OneOf
from datetime import datetime

class SurveyQuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SurveyQuestion
    
    survey = ma.Nested(mental_health_survey_schema)
    question = ma.Nested(question_schema)
    question_number = ma.Integer(required=True)
    
survey_question_schema = SurveyQuestionSchema()
survey_questions_schema = SurveyQuestionSchema(many=True)