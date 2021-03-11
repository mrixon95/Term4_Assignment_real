from main import ma
from models.MentalHealthSurvey import MentalHealthSurvey
from marshmallow.validate import Length, Email, OneOf
from datetime import datetime

class MentalHealthSurveySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MentalHealthSurvey
    
    name = ma.String(required=True)

mental_health_survey_schema = MentalHealthSurveySchema()
mental_health_surveys_schema = MentalHealthSurveySchema(many=True)