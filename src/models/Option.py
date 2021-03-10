from main import db
from datetime import datetime

class Option(db.Model):
    __tablename__ = "options"

    __table_args__ = (
        # this can be db.PrimaryKeyConstraint if you want it to be a primary key
        db.UniqueConstraint('question_id', 'option_number'),
      )

    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), primary_key=True)
    option_number = db.Column(db.Integer, primary_key=True, autoincrement=True)
    option_text = db.Column(db.String(), nullable=False)

    answer = db.relationship('Answer', primaryjoin="and_(Option.question_id==Answer.question_id, Option.option_number==Answer.option_number)", lazy='dynamic')

    def __repr__(self):
        return f"<Option. Question id: {self.question_id}, option number: {self.option_number}, option text: {self.option_text}>"