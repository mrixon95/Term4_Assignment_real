from main import db
from datetime import datetime

class MentalHealthSurvey(db.Model):
    __tablename__ = "mental_health_surveys"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<Mental Health Survey {self.id} {self.name}>"