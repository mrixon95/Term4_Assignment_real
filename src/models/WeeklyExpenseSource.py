from main import db
from datetime import datetime

class WeeklyExpenseSource(db.Model):
    __tablename__ = "weekly_expense_sources"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    expense_type = db.Column(db.String(), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    week_start = db.Column(db.Date(), nullable=False)
    week_end = db.Column(db.Date(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Weekly Expense Source {self.id} {self.description}>"