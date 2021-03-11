from main import db
from datetime import datetime
from models.SurveyQuestion import SurveyQuestion

class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(), nullable=False)

    survey_question = db.relationship("SurveyQuestion", backref="question", lazy="dynamic")

    def __repr__(self):
        return f"<Question {self.id} {self.text}>"