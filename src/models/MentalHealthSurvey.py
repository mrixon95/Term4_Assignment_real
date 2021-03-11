from main import db
from datetime import datetime
from models.SurveyQuestion import SurveyQuestion

class MentalHealthSurvey(db.Model):
    __tablename__ = "mental_health_surveys"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    survey_question = db.relationship("SurveyQuestion", backref="survey", lazy="dynamic")

    def __repr__(self):
        return f"<Mental Health Survey {self.id} {self.name}>"