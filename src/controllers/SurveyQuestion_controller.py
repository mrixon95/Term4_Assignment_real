
from schemas.SurveyQuestionSchema import survey_question_schema
from schemas.SurveyQuestionSchema import survey_questions_schema

from models.User import User
from models.SurveyQuestion import SurveyQuestion
from models.MentalHealthSurvey import MentalHealthSurvey
from models.Question import Question


from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
from sqlalchemy import func

surveyquestion = Blueprint('surveyquestion', __name__, url_prefix="/surveyquestion")

@surveyquestion.route("/", methods=["GET"])
def surveyquestion_all():

    surveyquestions = SurveyQuestion.query.all()
    return jsonify(survey_questions_schema.dump(surveyquestions))



@surveyquestion.route("/", methods=["POST"])
def surveyquestion_create():

    mental_health_survey_id = request.json["survey"]
    question_id = request.json["question"]
    question_number = request.json["question_number"]


    mentalhealthsurvey_object = MentalHealthSurvey.query.filter_by(id=mental_health_survey_id).first()
    
    if mentalhealthsurvey_object is None:
        return abort(401, description=f"There does not exist a Mental Health Survey with id {mental_health_survey_id}")


    question_object = Question.query.filter_by(id=question_id).first()
    
    if question_object is None:
        return abort(401, description=f"There does not exist a Question with id {question_id}")


    surveyquestion_object = SurveyQuestion.query.filter_by(mental_health_survey_id=mental_health_survey_id, question_id=question_id).first()
    
    if surveyquestion_object:
        return abort(401, description=f"There already exists a Survey Question with survey id {mental_health_survey_id} and question id {question_id}")




    surveyquestion_from_fields = SurveyQuestion()
    surveyquestion_from_fields.mental_health_survey_id = mental_health_survey_id
    surveyquestion_from_fields.question_id = question_id
    surveyquestion_from_fields.question_number = question_number

    db.session.add(surveyquestion_from_fields)
    
    db.session.commit()

    return jsonify(survey_question_schema.dump(surveyquestion_from_fields))


# @options.route("/<int:id>", methods=["GET"])
# def options_get(id):
    
#     option_object = Option.query.get(id)

#     if not option_object:
#         return abort(404, description=f"Optionwith id {id} does not exist")

#     return jsonify(mental_health_survey_schema.dump(mentalhealthsurvey_object))


@surveyquestion.route("/", methods=["PUT", "PATCH"])
def surveyquestion_update():


    mental_health_survey_id = request.json["survey"]
    question_id = request.json["question"]
    question_number = request.json["question_number"]

    surveyquestion_object_list = SurveyQuestion.query.filter_by(mental_health_survey_id=mental_health_survey_id, question_id=question_id)
    
    if surveyquestion_object_list.count() != 1:
        return abort(401, description=f"There does not exist a Survey Question with survey id {mental_health_survey_id} and question id {question_id}")

    
    surveyquestion_object = surveyquestion_object_list.first()

    surveyquestion_object.mental_health_survey_id = mental_health_survey_id
    surveyquestion_object.question_id = question_id
    surveyquestion_object.question_number = question_number

    db.session.commit()

    return jsonify(survey_question_schema.dump(surveyquestion_object))



@surveyquestion.route("/", methods=["DELETE"])
def surveyquestion_delete():

    mental_health_survey_id = request.json["survey"]
    question_id = request.json["question"]

    surveyquestion_object_list = SurveyQuestion.query.filter_by(mental_health_survey_id=mental_health_survey_id, question_id=question_id)
    
    if surveyquestion_object_list.count() != 1:
        return abort(401, description=f"There does not exist a Survey Question with survey id {mental_health_survey_id} and question id {question_id}")


   
    surveyquestion_object = surveyquestion_object_list.first()


    json_object_to_return = jsonify(survey_question_schema.dump(surveyquestion_object))

    db.session.delete(surveyquestion_object)

    db.session.commit()

    return json_object_to_return
