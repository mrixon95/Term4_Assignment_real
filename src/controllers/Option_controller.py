
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


    mental_health_survey_id = request.json["survey"]
    question_id = request.json["question"]
    question_number = request.json["question_number"]

    option_object_list = SurveyQuestion.query.filter_by(mental_health_survey_id=mental_health_survey_id, question_id=question_id)
    
    if option_object_list.count() != 1:
        return abort(401, description=f"There does not exist an option with survey id {mental_health_survey_id} and question id {question_id}")

    
    surveyquestion_object = surveyquestion_object_list.first()

    surveyquestion_object.mental_health_survey_id = mental_health_survey_id
    surveyquestion_object.question_id = question_id
    surveyquestion_object.question_number = question_number

    db.session.commit()

    return jsonify(survey_question_schema.dump(surveyquestion_object))



@option.route("/", methods=["DELETE"])
def option_delete():

    mental_health_survey_id = request.json["survey"]
    question_id = request.json["question"]

    option_object_list = Option.query.filter_by(mental_health_survey_id=mental_health_survey_id, question_id=question_id)
    
    if option_object_list.count() != 1:
        return abort(401, description=f"There does not exist an option with survey id {mental_health_survey_id} and question id {question_id}")


   
    option_object = option_object_list.first()


    json_object_to_return = jsonify(option_schema.dump(option_object))

    db.session.delete(option_object)

    db.session.commit()

    return json_object_to_return
