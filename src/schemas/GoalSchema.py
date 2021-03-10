from main import ma
from models.Goal import Goal
from schemas.UserSchema import user_schema
from marshmallow.validate import Length, Email, OneOf
from datetime import datetime

class GoalSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Goal
    
    created = ma.Date(required=True)
    description = ma.String(required=True)
    goal_type = ma.String(required=True, validate=OneOf(["Physical", "Mental", "Financial"]))
    user = ma.Nested(user_schema)

goal_schema = GoalSchema()
goals_schema = GoalSchema(many=True)