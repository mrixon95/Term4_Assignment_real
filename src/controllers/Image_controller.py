from models.Image import Image
from models.User import User
from schemas.ImageSchema import image_schema, image_schemas
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort, current_app, Response
from pathlib import Path
from main import db
import boto3

image = Blueprint('image', __name__, url_prefix="/image")

@image.route("/", methods=["POST"])
@jwt_required
def user_image_create():

    email_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.filter_by(email=email_of_jwt).first()

    if not user_of_jwt:
        return abort(404, description="User does not exist")


    if "image" not in request.files:
        return abort(400, description="No image")
        
    image = request.files["image"]

    if Path(image.filename).suffix not in [".jpg", ".png"]:
        return abort(400, description="Invalid file type")


    new_image = Image()
    new_image.user_id = user_of_jwt.id 
    new_image.path = ""

    db.session.add(new_image)
    
    db.session.commit()

    filename = str(new_image.id) + Path(image.filename).suffix
    bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
    key = f"images/user-{user_of_jwt.id}-image-{filename}"
    bucket.upload_fileobj(image, key)

    new_image.path = key
    db.session.commit()

    return jsonify(image_schema.dump(new_image))


@image.route("/<int:image_number>/user/<string:id>", methods=["GET"])
def user_image_show(image_number, id):

    image = Image.query.filter_by(id=image_number, user_id=id).first()

    if not image:
        return abort(404, description=f"No image with id {image_number} for user with id {id}")
    
    bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
    filename = image.path
    file_obj = bucket.Object(f"{filename}").get()

    return Response(
        file_obj['Body'].read(),
        mimetype='image/png',
        headers={"Content-Disposition": f"attachment;filename=image"}
    )

# @image.route("/<string:username>/image/<int:id>", methods=["GET"])
# def user_image_show_all(username):
#     pass


@image.route("/<int:id>", methods=["DELETE"])
@jwt_required
def user_image_delete(id):


    email_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.filter_by(email=email_of_jwt).first()

    image_object = Image.query.filter_by(id=id).first()

    if image_object is None:
        return abort(401, description=f"There does not exist an image with id {id}")


    if (user_of_jwt.id != image_object.user_id):
        return abort(401, description=f"You are logged in as the wrong user to access image with id {id} ")

    json_object_to_return = jsonify(image_schema.dump(image_object))


    bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
    filename = image_object.path

    bucket.Object(f"{filename}").delete()



    db.session.delete(image_object)
    
    db.session.commit()

    return json_object_to_return