from main import ma
from models.ProfileImage import ProfileImage
from marshmallow.validate import Length
from schemas.UserSchema import UserSchema

class ProfileImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProfileImage

    path = ma.String(required=True)
    last_updated = ma.DateTime()
    user =  ma.Nested(UserSchema)
    
profile_image_schema = ProfileImageSchema()
profile_images_schema = ProfileImageSchema(many=True)