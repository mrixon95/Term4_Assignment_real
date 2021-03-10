from main import ma
from models.DailyPhysicalHealthRecord import DailyPhysicalHealthRecord
from marshmallow.validate import Length
from schemas.UserSchema import UserSchema

class DailyPhysicalHealthRecordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DailyPhysicalHealthRecord

    date = ma.Date()
    weight_kgs = ma.Integer()
    height_cm = ma.Integer()
    hearth_bpm = ma.Integer()
    BMI = ma.Double()
    user =  ma.Nested(UserSchema)
    
daily_physical_health_record_schema = DailyPhysicalHealthRecordSchema()
daily_physical_health_records_schema = DailyPhysicalHealthRecordSchema(many=True)
