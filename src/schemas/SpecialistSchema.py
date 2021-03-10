from main import ma
from models.Specialist import Specialist
from marshmallow.validate import Length, Email, OneOf
from datetime import datetime

class SpecialistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Specialist
    
    name = ma.String(required=True, validate=Length(min=2))
    specialist_type = ma.DateTime(required=False, default=datetime.now())
    description = ma.Date(required=True)
    phone_number = ma.String(required=True)
    email = ma.String(required=True, validate=Email())
    address_street = ma.String()
    suburb = ma.String()
    first_registered = ma.DateTime(default=datetime.now())
    last_updated = ma.DateTime(default=datetime.now())
    
specialist_schema = SpecialistSchema()
specialists_schema = SpecialistSchema(many=True)