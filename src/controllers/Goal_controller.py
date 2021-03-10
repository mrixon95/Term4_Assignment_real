
from schemas.GoalSchema import goal_schema
from schemas.GoalSchema import goals_schema

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

    goal_sources = Goal.query.all()
    return jsonify(goal_schema.dump(goal_sources))


@goal.route("/user/<string:inputted_username>", methods=["GET"])
def goal_user(inputted_username):

    user_object = User.query.get(inputted_username)

    if not user_object:
        return abort(401, description="Invalid user")

    goals_unordered = Goal.query.filter_by(username=inputted_username)

    if not goals_unordered:
        return abort(404, description="No goals to return")

    goals_ordered = goals_unordered.order_by(Goal.created_at.desc()).all()
    return jsonify(goals_schema.dump(goals_ordered))


@goal.route("/", methods=["POST"])
@jwt_required
def goal_create():

    goal_inputted_fields = goal_schema.load(request.json)
    username_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.get(username_of_jwt)

    if not user_of_jwt:
        return abort(404, description="Goal does not exist")


    goal_from_fields = Goal()

    goal_from_fields.username = username_of_jwt
    goal_from_fields.description = goal_inputted_fields["description"]
    goal_from_fields.goal_type = goal_inputted_fields["goal_type"]

    db.session.add(goal_from_fields)
    
    db.session.commit()

    return jsonify(goal_schema.dump(goal_from_fields))


@goal.route("/<int:id>", methods=["GET"])
def goal_get(id):
    
    goal_object = Goal.query.get(id)

    if not goal_object:
        return abort(404, description=f"Weekly income source with id {id} does not exist")

    return jsonify(goal_schema.dump(goal_object))


@goal.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def goal_update(id):

    jwt_username = get_jwt_identity()
    jwt_user = User.query.get(jwt_username)

    goal_fields = goal_schema.load(request.json, partial=True)

    if not jwt_user:
        return abort(401, description="Invalid user")

    goal_object = Goal.query.filter_by(id=id, username=jwt_username)

    if goal_object.count() != 1:
        return abort(401, description=f"Goal with id {id} does not belong to the logged in user")

    goal_object.update(goal_fields)
    db.session.commit()

    return jsonify(goal_schema.dump(goal_object[0]))



@goal.route("/<int:id>", methods=["DELETE"])
@jwt_required
def goal_delete(id):

    jwt_username = get_jwt_identity()

    goal_object = Goal.query.filter_by(id=id).first()


    if goal_object is None:
        return abort(401, description=f"There does not exist a goal with id {id}")

    if (jwt_username != goal_object.username):
        return abort(401, description=f"The goal id of {id} belongs to a different user than your jwt token")



    goal_object = Goal.query.filter_by(id=id, username=jwt_username).first()

    if not goal_object:
        return abort(401, description=f"Goal of {id} does not exist for this user.")

    json_object_to_return = jsonify(goal_schema.dump(goal_object))

    db.session.delete(goal_object)

    db.session.commit()

    return json_object_to_return
