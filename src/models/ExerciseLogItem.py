from main import db
from datetime import datetime

class ExerciseLogItem(db.Model):
    __tablename__ = "exercise_log_items"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    date = db.Column(db.Date(), nullable=False)
    time_start = db.Column(db.DateTime(), nullable=False)
    time_end = db.Column(db.DateTime(), nullable=False)
    intensity = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Exercise Log Item {self.id} {self.date}>"