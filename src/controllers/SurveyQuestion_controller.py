
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

    surveyquestion_inputted_fields = survey_question_schema.load(request.json)
    survey_id = surveyquestion_inputted_fields["survey_id"]
    question_id = surveyquestion_inputted_fields["question_id"]
    question_number = surveyquestion_inputted_fields["question_number"]


    mentalhealthsurvey_object = MentalHealthSurvey.query.filter_by(id=survey_id).first()
    
    if mentalhealthsurvey_object is None:
        return abort(401, description=f"There does not exist a Mental Health Survey with id {survey_id}")


    question_object = Question.query.filter_by(id=question_id).first()
    
    if question_object is None:
        return abort(401, description=f"There does not exist a Question with id {question_id}")


    surveyquestion_object = SurveyQuestion.query.filter_by(mental_health_survey_id=survey_id, question_id=question_id).first()
    
    if surveyquestion_object:
        return abort(401, description=f"There already exists a Survey Question with survey id {survey_id} and question id {question_id}")




    surveyquestion_from_fields = SurveyQuestion()
    surveyquestion_from_fields.survey_id = survey_id
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


@surveyquestion.route("/<int:survey_id>/<int:question_id>", methods=["PUT", "PATCH"])
@jwt_required
def surveyquestion_update(survey_id, question_id):

    jwt_username = get_jwt_identity()
    jwt_user = User.query.get(jwt_username)

    surveyquestion_fields = survey_question_schema.load(request.json, partial=True)

    if not jwt_user:
        return abort(401, description="Invalid user")

    surveyquestion_object = SurveyQuestion.query.filter_by(survey_id=survey_id, question_id=question_id).first()

    if not surveyquestion_object:
        return abort(401, description=f"Survey question with survey id {survey_id} and question id {question_id} does not exist")

    surveyquestion_object.update(surveyquestion_fields)
    db.session.commit()

    return jsonify(survey_question_schema.dump(surveyquestion_object))



@surveyquestion.route("/<int:survey_id>/<int:question_id>", methods=["DELETE"])
@jwt_required
def surveyquestion_delete(survey_id, question_id):

    jwt_username = get_jwt_identity()

    surveyquestion_object = SurveyQuestion.query.filter_by(survey_id=survey_id, question_id=question_id).first()

    if not surveyquestion_object:
        return abort(401, description=f"Survey question with survey id {survey_id} and question id {question_id} does not exist")

    json_object_to_return = jsonify(survey_question_schema.dump(surveyquestion_object))

    db.session.delete(surveyquestion_object)

    db.session.commit()

    return json_object_to_return
