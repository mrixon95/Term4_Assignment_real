
from schemas.OptionSchema import option_schema
from schemas.OptionSchema import options_schema

from models.User import User
from models.SurveyQuestion import SurveyQuestion
from models.MentalHealthSurvey import MentalHealthSurvey
from models.Question import Question
from models.Option import Option


from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
from sqlalchemy import func

option = Blueprint('option', __name__, url_prefix="/option")

@option.route("/", methods=["GET"])
def option_all():

    options = Option.query.all()
    return jsonify(options_schema.dump(options))



@option.route("/", methods=["POST"])
def option_create():

    question_id = request.json["question"]
    option_text = request.json["option_text"]


    question_object = Question.query.filter_by(id=question_id).first()
    
    if question_object is None:
        return abort(401, description=f"There does not exist a question with id {question_id}")


    option_from_fields = Option()
    option_from_fields.question_id = question_id
    option_from_fields.option_text = option_text

    db.session.add(option_from_fields)
    
    db.session.commit()

    return jsonify(option_schema.dump(option_from_fields))


# @options.route("/<int:id>", methods=["GET"])
# def options_get(id):
    
#     option_object = Option.query.get(id)

#     if not option_object:
#         return abort(404, description=f"Optionwith id {id} does not exist")

#     return jsonify(mental_health_survey_schema.dump(mentalhealthsurvey_object))


@option.route("/", methods=["PUT", "PATCH"])
def option_update():


    question_id = request.json["question_id"]
    option_id = request.json["option_id"]
    option_text = request.json["option_text"]

    option_object = Option.query.filter_by(question_id=question_id, option_number=option_id).first()
    
    if option_object is None:
        return abort(401, description=f"There does not exist an option with id {option_id} and question id {question_id}")
    

    option_object.option_text = option_text

    db.session.commit()

    return jsonify(option_schema.dump(option_object))



@option.route("/", methods=["DELETE"])
def option_delete():

    question_id = request.json["question_id"]
    option_id = request.json["option_id"]

    option_object = Option.query.filter_by(question_id=question_id, option_number=option_id).first()
    
    if option_object is None:
        return abort(401, description=f"There does not exist an option with id {option_id} and question id {question_id}")
    

    json_object_to_return = jsonify(option_schema.dump(option_object))

    db.session.delete(option_object)

    db.session.commit()

    return json_object_to_return
