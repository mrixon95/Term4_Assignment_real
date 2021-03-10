
from schemas.SpecialistSchema import specialist_schema
from schemas.SpecialistSchema import specialists_schema

from models.User import User
from models.Specialist import Specialist

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
from sqlalchemy import func

specialist = Blueprint('specialist', __name__, url_prefix="/specialist")

@specialist.route("/", methods=["GET"])
def specialist_all():

    specialists = Specialist.query.all()
    return jsonify(specialists_schema.dump(specialists))



@specialist.route("/", methods=["POST"])
@jwt_required
def specialist_create():

    specialist_inputted_fields = specialist_schema.load(request.json)

    username_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.get(username_of_jwt)

    if not user_of_jwt:
        return abort(404, description="User does not exist")


    specialist_for_user = Specialist.query.filter_by(user_id=user_of_jwt.id)

    if specialist_for_user:
        return abort(404, description="You have already created a specialist. Only one specialist may be created per user")


    specialist_from_fields = Specialist()

    specialist_from_fields.name = specialist_inputted_fields["name"]
    specialist_from_fields.specialisation = specialist_inputted_fields["specialisation"]
    specialist_from_fields.phone_number = specialist_inputted_fields["phone_number"]
    specialist_from_fields.email = specialist_inputted_fields["email"]
    specialist_from_fields.street = specialist_inputted_fields["street"]
    specialist_from_fields.suburb = specialist_inputted_fields["suburb"]
    specialist_from_fields.first_registered = specialist_inputted_fields["first_registered"]
    specialist_from_fields.last_updated = specialist_inputted_fields["first_registered"]


    db.session.add(specialist_from_fields)
    
    db.session.commit()

    return jsonify(specialist_schema.dump(specialist_from_fields))


@specialist.route("/<int:id>", methods=["GET"])
def specialist_get(id):
    
    specialist_object = Specialist.query.get(id)

    if not specialist_object:
        return abort(404, description=f"Specialist with id {id} does not exist")

    return jsonify(specialist_schema.dump(specialist_object))


@specialist.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def specialist_update(id):

    jwt_username = get_jwt_identity()
    jwt_user = User.query.get(jwt_username)

    specialist_fields = specialist_schema.load(request.json, partial=True)

    if not jwt_user:
        return abort(401, description="Invalid user")

    specialist_object = Specialist.query.filter_by(id=id, username=jwt_username)

    if specialist_object.count() != 1:
        return abort(401, description=f"Specialist with id {id} does not belong to the logged in user")

    specialist_object.update(specialist_fields)
    db.session.commit()

    return jsonify(specialist_schema.dump(specialist_object[0]))



@specialist.route("/<int:id>", methods=["DELETE"])
@jwt_required
def specialist_delete(id):

    jwt_username = get_jwt_identity()

    specialist_object = Specialist.query.filter_by(id=id).first()


    if specialist_object is None:
        return abort(401, description=f"There does not exist a specialist with id {id}")

    if (jwt_username != specialist_object.user_id):
        return abort(401, description=f"The specialist {id} belongs to a different user than your jwt token")

    json_object_to_return = jsonify(specialist_schema.dump(specialist_object))

    db.session.delete(specialist_object)

    db.session.commit()

    return json_object_to_return
