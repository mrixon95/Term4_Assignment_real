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

    username_of_jwt = get_jwt_identity()
    
    image_id = 1
    images = Image.query.order_by(Image.id.desc()).first()
    if images is None:
        pass
    else:
        image_id = images.id + 1


    if "image" not in request.files:
        return abort(400, description="No image")
        
    image = request.files["image"]

    if Path(image.filename).suffix not in [".jpg", ".png"]:
        return abort(400, description="Invalid file type")



    filename = str(image_id) + Path(image.filename).suffix
    bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
    key = f"images/user-{username_of_jwt}-image-{filename}"
    bucket.upload_fileobj(image, key)

    new_image = Image()
    new_image.username = username_of_jwt 
    new_image.path = key

    db.session.add(new_image)
    
    db.session.commit()

    return jsonify(image_schema.dump(new_image))


@image.route("/<int:image_number>/username/<string:username_inputted>", methods=["GET"])
def user_image_show(image_number, username_inputted):

    image = Image.query.filter_by(id=image_number, username=username_inputted).first()

    if not image:
        return abort(404, description="No book image")
    
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

    jwt_username = get_jwt_identity()

    image_object = Image.query.filter_by(id=id).first()

    if image_object is None:
        return abort(401, description=f"There does not exist an image with id {id}")


    if (jwt_username != image_object.username):
        return abort(401, description=f"You are logged in as the wrong user to access image with id {id} ")

    json_object_to_return = jsonify(image_schema.dump(image_object))

    db.session.delete(image_object)
    
    db.session.commit()

    return json_object_to_return