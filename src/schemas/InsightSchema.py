from main import ma
from models.Insight import Insight
from schemas.UserSchema import user_schema
from marshmallow.validate import Length, Email, OneOf
from datetime import datetime

class InsightSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Insight
    
    date = ma.Date(required=True)
    insight_type = ma.String(required=True)
    health_type = ma.String(required=True, validate=OneOf(["Physical", "Mental", "Financial"]))
    description = ma.String(required=True, validate=Length(min=2))
    graph_type = ma.String(required=True)
    value = ma.Integer()
    unit = ma.String()
    degree_good_bad = ma.String(required=True, validate=OneOf(["Very good", "Good", "Neutral", "Bad", "Very bad"]))
    user = ma.Nested(user_schema)

insight_schema = InsightSchema()
insights_schema = InsightSchema(many=True)