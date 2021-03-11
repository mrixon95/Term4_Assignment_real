
from schemas.AnswerSchema import answer_schema
from schemas.AnswerSchema import answers_schema

from models.User import User
from models.SurveyQuestion import SurveyQuestion
from models.MentalHealthSurvey import MentalHealthSurvey
from models.Question import Question
from models.Option import Option
from models.Answer import Answer


from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
from sqlalchemy import func

answer = Blueprint('answer', __name__, url_prefix="/answer")

@answer.route("/", methods=["GET"])
def answer_all():

    answers = Answer.query.all()
    return jsonify(answers_schema.dump(answers))



@answer.route("/", methods=["POST"])
@jwt_required
def answer_create():

    email_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.filter_by(email=email_of_jwt).first()


    user_id = user_of_jwt.id
    question_id = request.json["question_id"]
    option_number = request.json["option_number"]


    answer_object = Answer.query.filter_by(user_id=user_id, question_id=question_id).first()
    
    if answer_object:
        return abort(401, description=f"There already exists an answer for this user and for question id {question_id}")


    option_object = Option.query.filter_by(question_id=question_id, option_number=option_number).first()

    if not option_object:
        return abort(401, description=f"There does not exists a response with question id {question_id} and option number {option_number}")



    answer_from_fields = Answer()
    answer_from_fields.user_id = user_id
    answer_from_fields.question_id = question_id
    answer_from_fields.option_number = option_number

    db.session.add(answer_from_fields)
    
    db.session.commit()

    return jsonify(answer_schema.dump(answer_from_fields))


# @options.route("/<int:id>", methods=["GET"])
# def options_get(id):
    
#     option_object = Option.query.get(id)

#     if not option_object:
#         return abort(404, description=f"Optionwith id {id} does not exist")

#     return jsonify(mental_health_survey_schema.dump(mentalhealthsurvey_object))


@answer.route("/", methods=["PUT", "PATCH"])
@jwt_required
def answer_update():


    email_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.filter_by(email=email_of_jwt).first()


    user_id = user_of_jwt.id
    question_id = request.json["question_id"]
    option_number = request.json["option_number"]


    answer_object = Answer.query.filter_by(question_id=question_id, option_number=option_id).first()
    
    if answer_object is None:
        return abort(401, description=f"There does not exist an answer for this user with question id {question_id}")
    

    answer_object.option_text = option_number

    db.session.commit()

    return jsonify(answer_schema.dump(answer_object))



@answer.route("/", methods=["DELETE"])
def answer_delete():

    question_id = request.json["question_id"]
    option_id = request.json["option_id"]

    answer_object = Answer.query.filter_by(question_id=question_id, option_number=option_id).first()
    
    if answer_object is None:
        return abort(401, description=f"There does not exist an answer with id {option_id} and question id {question_id}")
    

    json_object_to_return = jsonify(answer_schema.dump(answer_object))

    db.session.delete(answer_object)

    db.session.commit()

    return json_object_to_return
