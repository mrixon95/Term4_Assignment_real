from main import ma
from models.WeeklyExpenseSource import WeeklyExpenseSource
from schemas.UserSchema import user_schema
from marshmallow.validate import Length, Email, OneOf
from datetime import datetime

class WeeklyExpenseSourceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WeeklyExpenseSource
    
    description = ma.String(required=True)
    expense_type = ma.String(required=True, validate=OneOf(["Ongoing", "One-off"]))
    amount = ma.Integer(required=True)
    week_start = ma.Date(required=True)
    week_end = ma.Date(required=True)
    user = ma.Nested(user_schema)

weekly_expense_source_schema = WeeklyExpenseSourceSchema()
weekly_expense_sources_schema = WeeklyExpenseSourceSchema(many=True)