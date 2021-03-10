
from schemas.WeeklyExpenseSourceSchema import weekly_expense_source_schema
from schemas.WeeklyExpenseSourceSchema import weekly_expense_sources_schema

from models.User import User
from models.WeeklyExpenseSource import WeeklyExpenseSource

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
from sqlalchemy import func

weeklyexpensesource = Blueprint('weeklyexpensesource', __name__, url_prefix="/weeklyexpensesource")

@weeklyexpensesource.route("/", methods=["GET"])
def weeklyexpensesource_all():

    weekly_expense_sources = WeeklyExpenseSource.query.all()
    return jsonify(weekly_expense_sources_schema.dump(weekly_expense_sources))


@weeklyexpensesource.route("/user/<int:id>", methods=["GET"])
def weeklyexpensesource_user(id):

    user_object = User.query.filter_by(id=id).first()

    if not user_object:
        return abort(401, description="Invalid user")

    weekly_expense_sources_unordered = WeeklyExpenseSource.query.filter_by(user_id=id)

    if not weekly_expense_sources_unordered:
        return abort(404, description=f"No weekly expenses to return for user with id {id}")

    weekly_expense_sources_ordered = weekly_expense_sources_unordered.order_by(WeeklyExpenseSource.week_start.desc()).all()
    return jsonify(weekly_expense_sources_schema.dump(weekly_expense_sources_ordered))


@weeklyexpensesource.route("/", methods=["POST"])
@jwt_required
def weeklyexpensesource_create():

    weekly_expense_source_inputted_fields = weekly_expense_source_schema.load(request.json)
    email_of_jwt = get_jwt_identity()


    user_of_jwt = User.query.filter_by(email=email_of_jwt).first()

    if not user_of_jwt:
        return abort(404, description="User does not exist")


    weekly_expense_source_from_fields = WeeklyExpenseSource()

    weekly_expense_source_from_fields.user_id = user_of_jwt.id
    weekly_expense_source_from_fields.description = weekly_expense_source_inputted_fields["description"]
    weekly_expense_source_from_fields.expense_type = weekly_expense_source_inputted_fields["expense_type"]
    weekly_expense_source_from_fields.amount = weekly_expense_source_inputted_fields["amount"]
    weekly_expense_source_from_fields.week_start = weekly_expense_source_inputted_fields["week_start"]
    weekly_expense_source_from_fields.week_end = weekly_expense_source_inputted_fields["week_end"]

    db.session.add(weekly_expense_source_from_fields)
    
    db.session.commit()

    return jsonify(weekly_expense_source_schema.dump(weekly_expense_source_from_fields))


@weeklyexpensesource.route("/<int:id>", methods=["GET"])
def weeklyexpensesource_get(id):
    
    weekly_expense_source_object = WeeklyExpenseSource.query.get(id)

    if not weekly_expense_source_object:
        return abort(404, description=f"Weekly expense source with id {id} does not exist")

    return jsonify(weekly_expense_source_schema.dump(weekly_expense_source_object))


@weeklyexpensesource.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def weeklyexpensesource_update(id):


    email_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.filter_by(email=email_of_jwt).first()



    weekly_expense_source_fields = weekly_expense_source_schema.load(request.json, partial=True)

    if not user_of_jwt:
        return abort(401, description="Invalid user")

    weekly_expense_source_object = WeeklyExpenseSource.query.filter_by(id=id, user_id=user_of_jwt.id)

    if weekly_expense_source_object.count() != 1:
        return abort(401, description=f"Weekly expense source with id {id} does not belong to the logged in user")

    weekly_expense_source_object.update(weekly_expense_source_fields)
    db.session.commit()

    return jsonify(weekly_expense_source_schema.dump(weekly_expense_source_object[0]))



@weeklyexpensesource.route("/<int:id>", methods=["DELETE"])
@jwt_required
def weeklyexpensesource_delete(id):

    email_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.filter_by(email=email_of_jwt).first()

    if not user_of_jwt:
        return abort(401, description="Invalid user")

    weekly_expense_source_object = WeeklyExpenseSource.query.filter_by(id=id, user_id=user_of_jwt.id).first()

    if weekly_expense_source_object is None:
        return abort(401, description=f"There does not exist a weekly expense source with id {id} that belongs to the logged in user")

    json_object_to_return = jsonify(weekly_expense_source_schema.dump(weekly_expense_source_object))

    db.session.delete(weekly_expense_source_object)

    db.session.commit()

    return json_object_to_return
