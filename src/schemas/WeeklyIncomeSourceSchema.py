from main import ma
from models.WeeklyIncomeSource import WeeklyIncomeSource
from schemas.UserSchema import user_schema
from marshmallow.validate import Length, Email, OneOf
from datetime import datetime

class WeeklyIncomeSourceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WeeklyIncomeSource
    
    description = ma.String(required=True)
    income_type = ma.String(required=True, validate=OneOf(["Ongoing", "One-off"]))
    amount = ma.Integer(required=True)
    week_start = ma.Date(required=True)
    week_end = ma.Date(required=True)
    user = ma.Nested(user_schema)

weekly_income_source_schema = WeeklyIncomeSourceSchema()
weekly_income_sources_schema = WeeklyIncomeSourceSchema(many=True)