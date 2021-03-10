from main import db
from datetime import datetime

class SurveyQuestion(db.Model):
    __tablename__ = "survey_questions"

    mental_health_survey_id = db.Column(db.Integer, db.ForeignKey("mental_health_surveys.id"), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), primary_key=True)
    question_number = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Survey number: {self.mental_health_survey_id}, Question id: {self.question_id}, Question number: {self.question_number}>"