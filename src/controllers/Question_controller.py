
from schemas.QuestionSchema import question_schema
from schemas.QuestionSchema import questions_schema

from models.User import User
from models.Question import Question

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
from sqlalchemy import func

question = Blueprint('question', __name__, url_prefix="/question")

@question.route("/", methods=["GET"])
def question_all():

    questions = Question.query.all()
    return jsonify(questions_schema.dump(questions))



@question.route("/", methods=["POST"])
def question_create():

    question_inputted_fields = question_schema.load(request.json)

    question_from_fields = Question()
    question_from_fields.text = question_inputted_fields["text"]

    db.session.add(question_from_fields)
    
    db.session.commit()

    return jsonify(question_schema.dump(question_from_fields))


# @options.route("/<int:id>", methods=["GET"])
# def options_get(id):
    
#     option_object = Option.query.get(id)

#     if not option_object:
#         return abort(404, description=f"Optionwith id {id} does not exist")

#     return jsonify(mental_health_survey_schema.dump(mentalhealthsurvey_object))


@question.route("/<int:id>", methods=["PUT", "PATCH"])
def question_update(id):

    question_inputted_fields = question_schema.load(request.json)

    question_object = Question.query.filter_by(id=id)

    if question_object.count() != 1:
        return abort(401, description=f"No question with id {id}")

    question_object.update(question_inputted_fields)
    db.session.commit()

    return jsonify(question_schema.dump(question_object.first()))



@question.route("/<int:id>", methods=["DELETE"])
def question_delete(id):

    jwt_username = get_jwt_identity()

    question_object = Question.query.filter_by(id=id).first()

    if not question_object:
        return abort(401, description=f"Question with id {id} does not exist")

    json_object_to_return = jsonify(question_schema.dump(question_object))

    db.session.delete(question_object)

    db.session.commit()

    return json_object_to_return
