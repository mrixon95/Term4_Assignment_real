
from schemas.MentalHealthSurveySchema import mental_health_survey_schema
from schemas.MentalHealthSurveySchema import mental_health_surveys_schema

from models.User import User
from models.MentalHealthSurvey import MentalHealthSurvey
from models.SurveyQuestion import SurveyQuestion


from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
from sqlalchemy import func

mentalhealthsurvey = Blueprint('mentalhealthsurvey', __name__, url_prefix="/mentalhealthsurvey")

@mentalhealthsurvey.route("/", methods=["GET"])
def mentalhealthsurvey_all():

    mentalhealthsurveys = MentalHealthSurvey.query.all()
    return jsonify(mental_health_surveys_schema.dump(mentalhealthsurveys))



@mentalhealthsurvey.route("/", methods=["POST"])
def mentalhealthsurvey_create():

    mentalhealthsurvey_inputted_fields = mental_health_survey_schema.load(request.json)

    mentalhealthsurvey_from_fields = MentalHealthSurvey()
    mentalhealthsurvey_from_fields.name = mentalhealthsurvey_inputted_fields["name"]

    db.session.add(mentalhealthsurvey_from_fields)
    
    db.session.commit()

    return jsonify(mental_health_survey_schema.dump(mentalhealthsurvey_from_fields))


@mentalhealthsurvey.route("/<int:id>", methods=["GET"])
def mentalhealthsurvey_get(id):
    
    mentalhealthsurvey_object = MentalHealthSurvey.query.get(id)

    if not mentalhealthsurvey_object:
        return abort(404, description=f"Mental Health Survey with id {id} does not exist")

    return jsonify(mental_health_survey_schema.dump(mentalhealthsurvey_object))


@mentalhealthsurvey.route("/<int:id>", methods=["PUT", "PATCH"])
def mentalhealthsurvey_update(id):

    mentalhealthsurvey_fields = mental_health_survey_schema.load(request.json, partial=True)

    mentalhealthsurvey_object = MentalHealthSurvey.query.filter_by(id=id)

    if mentalhealthsurvey_object.count() != 1:
        return abort(401, description=f"Mental Health Survey with id {id} does not exist")

    mentalhealthsurvey_object.update(mentalhealthsurvey_fields)
    db.session.commit()

    return jsonify(mental_health_survey_schema.dump(mentalhealthsurvey_object[0]))



@mentalhealthsurvey.route("/<int:id>", methods=["DELETE"])
def mentalhealthsurvey_delete(id):

    mentalhealthsurvey_object = MentalHealthSurvey.query.filter_by(id=id).first()


    if mentalhealthsurvey_object is None:
        return abort(401, description=f"There does not exist a Mental Health Survey with id {id}")

    surveyquestion_object = SurveyQuestion.query.filter_by(mental_health_survey_id=id)

    num_questions = surveyquestion_object.count()

    if num_questions > 0:
        return abort(401, description=f"The Mental Health Survey with id {id} has {num_questions} questions that must be deleted first.")

    json_object_to_return = jsonify(mental_health_survey_schema.dump(mentalhealthsurvey_object))

    db.session.delete(mentalhealthsurvey_object)

    db.session.commit()

    return json_object_to_return
