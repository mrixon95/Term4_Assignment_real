from main import db
from datetime import datetime

class DailyPhysicalHealthRecord(db.Model):
    __tablename__ = "daily_physical_health_records"

    date = db.Column(db.Date(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True, nullable=False)
    weight_kgs = db.Column(db.String(), nullable=False)
    height_cm = db.Column(db.String(), nullable=False)
    hearth_bpm = db.Column(db.Integer(), nullable=False)
    BMI = db.Column(db.Float(), nullable=False)

    def __repr__(self):
        return f"<Daily Physical Health Record {self.date} {self.username}>"