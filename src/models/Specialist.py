from main import db
from datetime import datetime

class Specialist(db.Model):
    __tablename__ = "specialists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    specialisation = db.Column(db.String(), nullable=False)
    description = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    phone_number = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    street = db.Column(db.String(), nullable=False)
    suburb = db.Column(db.String(), nullable=False)
    first_registered = db.Column(db.DateTime(), nullable=False)
    last_updated = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<Specialist {self.id} {self.name}>"