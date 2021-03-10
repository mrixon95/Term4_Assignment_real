from schemas.InsightSchema import insight_schema
from schemas.InsightSchema import insights_schema

from models.User import User
from models.Insight import Insight

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
from sqlalchemy import func

insight = Blueprint('insight', __name__, url_prefix="/insight")

@insight.route("/", methods=["GET"])
def insight_all():

    insights = Insight.query.all()
    return jsonify(insights_schema.dump(insights))


@insight.route("/user/<string:id>", methods=["GET"])
def insight_user(id):

    user_object = User.query.get(id)

    if not user_object:
        return abort(401, description="Invalid user")

    insights_unordered = Insight.query.filter_by(id=id)

    if not insights_unordered:
        return abort(404, description="No insights to return")

    insights_ordered = insights_unordered.order_by(Insight.week_start.desc()).all()
    return jsonify(insights_schema.dump(insights_ordered))


@insight.route("/", methods=["POST"])
@jwt_required
def insight_create():

    insight_inputted_fields = insight_schema.load(request.json)
    username_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.get(username_of_jwt)

    if not user_of_jwt:
        return abort(404, description="User does not exist")


    insight_from_fields = Insight()

    insight_from_fields.user = username_of_jwt
    insight_from_fields.date = insight_inputted_fields["date"]
    insight_from_fields.insight_type = insight_inputted_fields["insight_type"]
    insight_from_fields.health_type = insight_inputted_fields["health_type"]
    insight_from_fields.description = insight_inputted_fields["description"]
    insight_from_fields.graph_type = insight_inputted_fields["graph_type"]
    insight_from_fields.value = insight_inputted_fields["value"]
    insight_from_fields.unit = insight_inputted_fields["unit"]
    insight_from_fields.degree_good_bad = insight_inputted_fields["degree_good_bad"]

    db.session.add(insight_from_fields)
    
    db.session.commit()

    return jsonify(insight_schema.dump(insight_from_fields))


@insight.route("/<int:id>", methods=["GET"])
def insight_get(id):
    
    insight_object = Insight.query.get(id)

    if not insight_object:
        return abort(404, description=f"Insight with id {id} does not exist")

    return jsonify(insight_schema.dump(insight_object))


@insight.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def insight_update(id):

    jwt_username = get_jwt_identity()
    jwt_user = User.query.get(jwt_username)

    insight_fields = insight_schema.load(request.json, partial=True)

    if not jwt_user:
        return abort(401, description="Invalid user")

    insight_object = Insight.query.filter_by(id=id, username=jwt_username)

    if insight_object.count() != 1:
        return abort(401, description=f"Insight with id {id} does not belong to the logged in user")

    insight_object.update(insight_fields)
    db.session.commit()

    return jsonify(insight_schema.dump(insight_object[0]))



@insight.route("/<int:id>", methods=["DELETE"])
@jwt_required
def insight_delete(id):

    jwt_username = get_jwt_identity()

    user_object = User.query.filter_by(id=jwt_username).first()


    if user_object is None:
        return abort(401, description=f"There does not exist an user with id {id}")

    if (jwt_username != user_object.id):
        return abort(401, description=f"The insight id of {id} belongs to a different user than your jwt token")



    insight_object = Insight.query.filter_by(id=id, user=jwt_username).first()

    if not insight_object:
        return abort(401, description=f"The insight id of {id} does not exist for this user.")

    json_object_to_return = jsonify(insight_schema.dump(insight_object))

    db.session.delete(insight_object)

    db.session.commit()

    return json_object_to_return
