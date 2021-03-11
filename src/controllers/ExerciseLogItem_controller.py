from schemas.ExerciseLogItemSchema import exercise_log_item_schema, exercise_log_items_schema

from models.User import User
from models.ExerciseLogItem import ExerciseLogItem

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
from sqlalchemy import func

exerciselogitem = Blueprint('exerciselogitem', __name__, url_prefix="/exerciselogitem")

@exerciselogitem.route("/", methods=["POST"])
@jwt_required
def exerciselogitem_create():

    exerciselogitem_inputted_fields = exercise_log_item_schema.load(request.json)
    email_of_jwt = get_jwt_identity()


    user_of_jwt = User.query.filter_by(email=email_of_jwt).first()

    if not user_of_jwt:
        return abort(404, description="User does not exist")


    exerciselogitem_from_fields = ExerciseLogItem()

    exerciselogitem_from_fields.user_id = user_of_jwt.id
    exerciselogitem_from_fields.description = exerciselogitem_inputted_fields["description"]
    exerciselogitem_from_fields.date = exerciselogitem_inputted_fields["date"]
    exerciselogitem_from_fields.time_start = exerciselogitem_inputted_fields["time_start"]
    exerciselogitem_from_fields.time_end = exerciselogitem_inputted_fields["time_end"]
    exerciselogitem_from_fields.intensity = exerciselogitem_inputted_fields["intensity"]

    db.session.add(exerciselogitem_from_fields)
    
    db.session.commit()

    return jsonify(exercise_log_item_schema.dump(exerciselogitem_from_fields))


@exerciselogitem.route("/", methods=["GET"])
def exerciselogitem_all():

    exerciselogitems = ExerciseLogItem.query.all()
    return jsonify(exercise_log_items_schema.dump(exerciselogitems))


@exerciselogitem.route("/user/<int:id>", methods=["GET"])
def exerciselogitem_user(id):

    user_object = User.query.filter_by(id=id).first()

    if not user_object:
        return abort(401, description="Invalid user")

    exerciselogitems_unordered = ExerciseLogItem.query.filter_by(user_id=id)

    if not exerciselogitems_unordered:
        return abort(404, description=f"No exercise log item to return for user with id {id}")

    exerciselogitems_ordered = exerciselogitems_unordered.order_by(ExerciseLogItem.time_start.desc()).all()
    return jsonify(exercise_log_items_schema.dump(exerciselogitems_ordered))



@exerciselogitem.route("/<int:id>", methods=["GET"])
def exerciselogitem_get(id):
    
    exerciselogitem_object = ExerciseLogItem.query.get(id)

    if not exerciselogitem_object:
        return abort(404, description=f"Exercise log item with id {id} does not exist")

    return jsonify(exercise_log_item_schema.dump(exerciselogitem_object))


 
@exerciselogitem.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def exerciselogitem_update(id):


    email_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.filter_by(email=email_of_jwt).first()



    exerciselogitem_fields = exercise_log_item_schema.load(request.json, partial=True)

    if not user_of_jwt:
        return abort(401, description="Invalid user")

    exerciselogitem_object = ExerciseLogItem.query.filter_by(id=id, user_id=user_of_jwt.id)

    if exerciselogitem_object.count() != 1:
        return abort(401, description=f"Goal with id {id} does not belong to the logged in user")

    exerciselogitem_object.update(exerciselogitem_fields)
    db.session.commit()

    return jsonify(exercise_log_item_schema.dump(exerciselogitem_object[0]))



@exerciselogitem.route("/<int:id>", methods=["DELETE"])
@jwt_required
def exerciselogitem_delete(id):

    email_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.filter_by(email=email_of_jwt).first()

    if not user_of_jwt:
        return abort(401, description="Invalid user")

    exerciselogitem_object = ExerciseLogItem.query.filter_by(id=id, user_id=user_of_jwt.id).first()

    if exerciselogitem_object is None:
        return abort(401, description=f"There does not exist an exercise log item with id {id} that belongs to the logged in user")

    json_object_to_return = jsonify(exercise_log_item_schema.dump(exerciselogitem_object))

    db.session.delete(exerciselogitem_object)

    db.session.commit()

    return json_object_to_return
