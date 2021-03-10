from main import db
from datetime import datetime

class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<Question {self.id} {self.text}>"