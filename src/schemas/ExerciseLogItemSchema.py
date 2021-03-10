from main import ma
from models.ExerciseLogItem import ExerciseLogItem
from marshmallow.validate import Length, OneOf
from schemas.UserSchema import UserSchema

class ExerciseLogItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ExerciseLogItem

    description = ma.String()
    date = ma.Date()
    time_start = ma.DateTime()
    time_end = ma.DateTime()
    intensity = ma.String(validate=OneOf(["Low", "Medium", "High"]))
    user =  ma.Nested(UserSchema)

    
exercise_log_item_schema = ExerciseLogItemSchema()
exercise_log_items_schema = ExerciseLogItemSchema(many=True)