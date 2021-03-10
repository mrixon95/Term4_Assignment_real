from main import db
from datetime import datetime

class Insight(db.Model):
    __tablename__ = "insights"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date(), nullable=False)
    insight_type = db.Column(db.String(), nullable=False)
    health_type = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    graph_type = db.Column(db.String(), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(), nullable=False)
    degree_good_bad = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Insight {self.id} {self.date}>"