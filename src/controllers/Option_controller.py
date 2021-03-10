
from schemas.OptionSchema import option_schema
from schemas.OptionSchema import options_schema

from models.User import User
from models.Option import Option
from models.MentalHealthSurvey import MentalHealthSurvey

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
from sqlalchemy import func

option = Blueprint('option', __name__, url_prefix="/option")

@option.route("/", methods=["GET"])
def option_all():

    options = Option.query.all()
    return jsonify(option_schema.dump(options))



@option.route("/", methods=["POST"])
@jwt_required
def option_create():

    option_inputted_fields = option_schema.load(request.json)

    option_from_fields = Option()
    option_from_fields.user = option_inputted_fields["user"]
    option_from_fields.question = option_inputted_fields["question"]
    option_from_fields.option_text = option_inputted_fields["option_text"]

    db.session.add(option_from_fields)
    
    db.session.commit()

    return jsonify(option_schema.dump(option_from_fields))


# @options.route("/<int:id>", methods=["GET"])
# def options_get(id):
    
#     option_object = Option.query.get(id)

#     if not option_object:
#         return abort(404, description=f"Optionwith id {id} does not exist")

#     return jsonify(mental_health_survey_schema.dump(mentalhealthsurvey_object))


@option.route("/<int:question_id>/<int:option_number>", methods=["PUT", "PATCH"])
@jwt_required
def option_update(question_id, option_number):

    jwt_username = get_jwt_identity()
    jwt_user = User.query.get(jwt_username)

    option_fields = option_schema.load(request.json, partial=True)

    if not jwt_user:
        return abort(401, description="Invalid user")

    option_object = Option.query.filter_by(question_id=question_id, option_number=option_number)

    if option_object.count() != 1:
        return abort(401, description=f"Option with question id {question_id} and option number {option_number} does not exist")

    option_object.update(option_fields)
    db.session.commit()

    return jsonify(option_schema.dump(option_object[0]))



@option.route("/<int:question_id>/<int:option_number>", methods=["DELETE"])
@jwt_required
def option_delete(question_id, option_number):

    jwt_username = get_jwt_identity()

    option_object = Option.query.filter_by(question_id=question_id, option_number=option_number).first()

    if not option_object:
        return abort(401, description=f"Option with question id {question_id} and option number {option_number} does not exist")

    json_object_to_return = jsonify(option_schema.dump(option_object))

    db.session.delete(option_object)

    db.session.commit()

    return json_object_to_return
