from main import ma
from models.Image import Image
from marshmallow.validate import Length, Email, OneOf
from datetime import datetime

class ImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Image
    
    username = ma.String(required=True, validate=Length(min=4))
    path = ma.String(required=True)
    last_updated = ma.DateTime(required=True,nullable=False, default=datetime.utcnow)

image_schema = ImageSchema()
image_schemas = ImageSchema(many=True)