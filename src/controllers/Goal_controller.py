from schemas.GoalSchema import goal_schema, goals_schema

from models.User import User
from models.Goal import Goal

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
from sqlalchemy import func

goal = Blueprint('goal', __name__, url_prefix="/goal")

@goal.route("/", methods=["GET"])
def goal_all():

    goals = Goal.query.all()
    return jsonify(goals_schema.dump(goals))


@goal.route("/user/<int:id>", methods=["GET"])
def goal_user(id):

    goal_object = Goal.query.filter_by(id=id).first()

    if not goal_object:
        return abort(401, description="Invalid user")

    goals_unordered = Goal.query.filter_by(user_id=id)

    if not goals_unordered:
        return abort(404, description=f"No goals to return for user with id {id}")

    goals_ordered = goals_unordered.order_by(Goal.week_start.desc()).all()
    return jsonify(goals_schema.dump(goals_ordered))


@goal.route("/", methods=["POST"])
@jwt_required
def goal_create():

    goal_inputted_fields = goal_schema.load(request.json)
    email_of_jwt = get_jwt_identity()


    user_of_jwt = Goal.query.filter_by(email=email_of_jwt).first()

    if not user_of_jwt:
        return abort(404, description="User does not exist")


    goal_from_fields = Goal()

    goal_from_fields.user_id = user_of_jwt.id
    goal_from_fields.description = goal_inputted_fields["description"]
    goal_from_fields.goal_type = goal_inputted_fields["goal_type"]

    db.session.add(goal_from_fields)
    
    db.session.commit()

    return jsonify(goal_schema.dump(goal_from_fields))


@goal.route("/<int:id>", methods=["GET"])
def goal_get(id):
    
    goal_object = Goal.query.get(id)

    if not goal_object:
        return abort(404, description=f"Goal with id {id} does not exist")

    return jsonify(goal_schema.dump(goal_object))


@goal.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def goal_update(id):


    email_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.filter_by(email=email_of_jwt).first()



    goal_fields = goal_schema.load(request.json, partial=True)

    if not user_of_jwt:
        return abort(401, description="Invalid user")

    goal_object = Goal.query.filter_by(id=id, user_id=user_of_jwt.id)

    if goal_object.count() != 1:
        return abort(401, description=f"Goal with id {id} does not belong to the logged in user")

    goal_object.update(goal_fields)
    db.session.commit()

    return jsonify(goal_schema.dump(goal_object[0]))



@goal.route("/<int:id>", methods=["DELETE"])
@jwt_required
def goal_delete(id):

    email_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.filter_by(email=email_of_jwt).first()

    if not user_of_jwt:
        return abort(401, description="Invalid user")

    goal_object = Goal.query.filter_by(id=id, user_id=user_of_jwt.id).first()

    if goal_object is None:
        return abort(401, description=f"There does not exist a goal with id {id} that belongs to the logged in user")

    json_object_to_return = jsonify(goal_schema.dump(goal_object))

    db.session.delete(goal_object)

    db.session.commit()

    return json_object_to_return