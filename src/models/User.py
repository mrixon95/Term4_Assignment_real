from main import db, bcrypt
from datetime import datetime
from models.DailyPhysicalHealthRecord import DailyPhysicalHealthRecord
from models.ExerciseLogItem import ExerciseLogItem
from models.Insight import Insight
from models.Goal import Goal
from models.ProfileImage import ProfileImage
from models.WeeklyIncomeSource import WeeklyIncomeSource
from models.WeeklyExpenseSource import WeeklyExpenseSource
from models.Answer import Answer
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    dob = db.Column(db.DateTime(), nullable=False)
    gender = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    mobile = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(), nullable=False)
    country = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)

    exercise_log_items = db.relationship("ExerciseLogItem", backref="user", lazy="dynamic")
    insights = db.relationship("Insight", backref="user", lazy="dynamic")
    goals = db.relationship("Goal", backref="user", lazy="dynamic")
    profile_images = db.relationship("ProfileImage", backref="user", lazy="dynamic")
    weekly_income_source = db.relationship("WeeklyIncomeSource", backref="user", lazy="dynamic")
    weekly_expense_source = db.relationship("WeeklyExpenseSource", backref="user", lazy="dynamic")
    answer = db.relationship("Answer", backref="user", lazy="dynamic")

    daily_physical_health = db.relationship(
        "DailyPhysicalHealthRecord",
        foreign_keys="DailyPhysicalHealthRecord.user_id",
        backref ="user"
    )


    def __repr__(self):
        return f"<User {self.id} {self.email}>"

    
    def get_id(self):
        try:
            return str(self.email)
        except AttributeError:
            raise NotImplementedError('No `email` attribute - override `get_id`')

    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)