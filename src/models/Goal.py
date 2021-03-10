from main import db
from datetime import datetime

class Goal(db.Model):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    description = db.Column(db.String(), nullable=False)
    goal_type = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Goal {self.id} {self.description}>"