
from schemas.ExerciseLogItemSchema import exercise_log_item_schema
from schemas.ExerciseLogItemSchema import exercise_log_items_schema

from models.User import User
from models.ExerciseLogItem import ExerciseLogItem

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
from sqlalchemy import func

exerciselogitem = Blueprint('exerciselogitem', __name__, url_prefix="/exerciselogitem")

@exerciselogitem.route("/", methods=["GET"])
def exerciselogitem_all():

    exercise_log_items = ExerciseLogItem.query.all()
    return jsonify(exercise_log_items_schema.dump(exercise_log_items))


@exerciselogitem.route("/user/<string:inputted_username>", methods=["GET"])
def exerciselogitem_user(inputted_username):

    user_object = User.query.get(inputted_username)

    if not user_object:
        return abort(401, description="Invalid user")

    exercise_log_items_unordered = ExerciseLogItem.query.filter_by(username=inputted_username)

    if not exercise_log_items_unordered:
        return abort(404, description="No weekly incomes to return")

    exercise_log_items_ordered = exercise_log_items_unordered.order_by(ExerciseLogItem.date.desc()).all()
    return jsonify(exercise_log_items_schema.dump(exercise_log_items_ordered))


@exerciselogitem.route("/", methods=["POST"])
@jwt_required
def exerciselogitem_create():

    exercise_log_item_inputted_fields = exercise_log_item_schema.load(request.json)
    username_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.get(username_of_jwt)

    if not user_of_jwt:
        return abort(404, description="User does not exist")


    exercise_log_item_from_fields = ExerciseLogItem()

    exercise_log_item_from_fields.username = username_of_jwt
    exercise_log_item_from_fields.description = exercise_log_item_inputted_fields["description"]
    exercise_log_item_from_fields.date = exercise_log_item_inputted_fields["date"]
    exercise_log_item_from_fields.time_start = exercise_log_item_inputted_fields["time_start"]
    exercise_log_item_from_fields.time_end = exercise_log_item_inputted_fields["time_end"]
    exercise_log_item_from_fields.intensity_level = exercise_log_item_inputted_fields["intensity_level"]

    db.session.add(exercise_log_item_from_fields)
    
    db.session.commit()

    return jsonify(exercise_log_item_schema.dump(exercise_log_item_from_fields))


@exerciselogitem.route("/<int:id>", methods=["GET"])
def exerciselogitem_get(id):
    
    exercise_log_item_object = ExerciseLogItem.query.get(id)

    if not exercise_log_item_object:
        return abort(404, description=f"Exercise log item with id {id} does not exist")

    return jsonify(exercise_log_item_schema.dump(exercise_log_item_object))


@exerciselogitem.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def exerciselogitem_update(id):

    jwt_username = get_jwt_identity()
    jwt_user = User.query.get(jwt_username)

    exercise_log_item_fields = exercise_log_item_schema.load(request.json, partial=True)

    if not jwt_user:
        return abort(401, description="Invalid user")

    exercise_log_item_object = ExerciseLogItem.query.filter_by(id=id, username=jwt_username)

    if exercise_log_item_object.count() != 1:
        return abort(401, description=f"Exercise log item with id {id} does not belong to the logged in user")

    exercise_log_item_object.update(exercise_log_item_fields)
    db.session.commit()

    return jsonify(exercise_log_item_schema.dump(exercise_log_item_object[0]))



@exerciselogitem.route("/<int:id>", methods=["DELETE"])
@jwt_required
def exerciselogitem_delete(id):

    jwt_username = get_jwt_identity()

    exercise_log_item_object = ExerciseLogItem.query.filter_by(id=id).first()


    if exercise_log_item_object is None:
        return abort(401, description=f"There does not exist an exercise log item with id {id}")

    if (jwt_username != exercise_log_item_object.user_id):
        return abort(401, description=f"The exercise log item with id of {id} belongs to a different user than your jwt token")



    exercise_log_item_object = ExerciseLogItem.query.filter_by(id=id, username=jwt_username).first()

    if not exercise_log_item_object:
        return abort(401, description=f"Exercise log item of {id} does not exist for this user.")

    json_object_to_return = jsonify(exercise_log_item_schema.dump(exercise_log_item_object))

    db.session.delete(exercise_log_item_object)

    db.session.commit()

    return json_object_to_return
