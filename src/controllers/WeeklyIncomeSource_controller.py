from schemas.WeeklyIncomeSourceSchema import weekly_income_source_schema, weekly_income_sources_schema

from models.User import User
from models.WeeklyIncomeSource import WeeklyIncomeSource

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
from sqlalchemy import func

weeklyincomesource = Blueprint('weeklyincomesource', __name__, url_prefix="/weeklyincomesource")

@weeklyincomesource.route("/", methods=["POST"])
@jwt_required
def weeklyincomesource_create():

    weekly_income_source_inputted_fields = weekly_income_source_schema.load(request.json)
    email_of_jwt = get_jwt_identity()


    user_of_jwt = User.query.filter_by(email=email_of_jwt).first()

    if not user_of_jwt:
        return abort(404, description="User does not exist")


    weekly_income_source_from_fields = WeeklyIncomeSource()

    weekly_income_source_from_fields.user_id = user_of_jwt.id
    weekly_income_source_from_fields.description = weekly_income_source_inputted_fields["description"]
    weekly_income_source_from_fields.income_type = weekly_income_source_inputted_fields["income_type"]
    weekly_income_source_from_fields.amount = weekly_income_source_inputted_fields["amount"]
    weekly_income_source_from_fields.week_start = weekly_income_source_inputted_fields["week_start"]
    weekly_income_source_from_fields.week_end = weekly_income_source_inputted_fields["week_end"]

    db.session.add(weekly_income_source_from_fields)
    
    db.session.commit()

    return jsonify(weekly_income_source_schema.dump(weekly_income_source_from_fields))


@weeklyincomesource.route("/", methods=["GET"])
def weeklyincomesource_all():

    weekly_income_sources = WeeklyIncomeSource.query.all()
    return jsonify(weekly_income_sources_schema.dump(weekly_income_sources))


@weeklyincomesource.route("/user/<int:id>", methods=["GET"])
def weeklyincomesource_user(id):

    user_object = User.query.filter_by(id=id).first()

    if not user_object:
        return abort(401, description="Invalid user")

    weekly_income_sources_unordered = WeeklyIncomeSource.query.filter_by(user_id=id)

    if not weekly_income_sources_unordered:
        return abort(404, description=f"No weekly incomes to return for user with id {id}")

    weekly_income_sources_ordered = weekly_income_sources_unordered.order_by(WeeklyIncomeSource.week_start.desc()).all()
    return jsonify(weekly_income_sources_schema.dump(weekly_income_sources_ordered))



@weeklyincomesource.route("/<int:id>", methods=["GET"])
def weeklyincomesource_get(id):
    
    weekly_income_source_object = WeeklyIncomeSource.query.get(id)

    if not weekly_income_source_object:
        return abort(404, description=f"Weekly income source with id {id} does not exist")

    return jsonify(weekly_income_source_schema.dump(weekly_income_source_object))


@weeklyincomesource.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def weeklyincomesource_update(id):


    email_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.filter_by(email=email_of_jwt).first()



    weekly_income_source_fields = weekly_income_source_schema.load(request.json, partial=True)

    if not user_of_jwt:
        return abort(401, description="Invalid user")

    weekly_income_source_object = WeeklyIncomeSource.query.filter_by(id=id, user_id=user_of_jwt.id)

    if weekly_income_source_object.count() != 1:
        return abort(401, description=f"Weekly income source with id {id} does not belong to the logged in user")

    weekly_income_source_object.update(weekly_income_source_fields)
    db.session.commit()

    return jsonify(weekly_income_source_schema.dump(weekly_income_source_object[0]))



@weeklyincomesource.route("/<int:id>", methods=["DELETE"])
@jwt_required
def weeklyincomesource_delete(id):

    email_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.filter_by(email=email_of_jwt).first()

    if not user_of_jwt:
        return abort(401, description="Invalid user")

    weekly_income_source_object = WeeklyIncomeSource.query.filter_by(id=id, user_id=user_of_jwt.id).first()

    if weekly_income_source_object is None:
        return abort(401, description=f"There does not exist a weekly income source with id {id} that belongs to the logged in user")

    json_object_to_return = jsonify(weekly_income_source_schema.dump(weekly_income_source_object))

    db.session.delete(weekly_income_source_object)

    db.session.commit()

    return json_object_to_return
