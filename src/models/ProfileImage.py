from main import db
from datetime import datetime

class ProfileImage(db.Model):
    __tablename__ = "profile_images"

    id =  db.Column(db.Integer,  primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    path = db.Column(db.String(), nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __repr__(self):
        return f"<ProfileImage {self.id} User {self.user_id}>"