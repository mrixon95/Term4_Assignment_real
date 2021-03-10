from main import db
from datetime import datetime

from sqlalchemy import UniqueConstraint, ForeignKeyConstraint

class Answer(db.Model):
    __tablename__ = "answers"

    __table_args__ = (
        # this can be db.PrimaryKeyConstraint if you want it to be a primary key
        ForeignKeyConstraint(
            ['question_id', 'option_number'],
            ['options.question_id', 'options.option_number'],
        ),
      )

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    question_id = db.Column(db.Integer, primary_key=True)
    option_number = db.Column(db.Integer)

    def __repr__(self):
        return f"<Answer. User id: {self.user_id}, question id: {self.question_id}, option number: {self.option_number}>"
