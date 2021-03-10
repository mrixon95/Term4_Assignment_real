from schemas.AnswerSchema import answer_schema
from schemas.AnswerSchema import answers_schema

from models.User import User
from models.Answer import Answer
from models.MentalHealthSurvey import MentalHealthSurvey

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
from sqlalchemy import func

answer = Blueprint('answer', __name__, url_prefix="/answer")

@answer.route("/", methods=["GET"])
def answer_all():

    answers = Answer.query.all()
    return jsonify(answer_schema.dump(answers))



@answer.route("/", methods=["POST"])
@jwt_required
def answer_create():

    answer_inputted_fields = answer_schema.load(request.json)

    answer_from_fields = Answer()
    answer_from_fields.user_id = answer_inputted_fields["user_id"]
    answer_from_fields.question_id = answer_inputted_fields["question_id"]
    answer_from_fields.option_id = answer_inputted_fields["option_id"]

    db.session.add(answer_from_fields)
    
    db.session.commit()

    return jsonify(answer_schema.dump(answer_from_fields))


# @options.route("/<int:id>", methods=["GET"])
# def options_get(id):
    
#     option_object = Option.query.get(id)

#     if not option_object:
#         return abort(404, description=f"Optionwith id {id} does not exist")

#     return jsonify(mental_health_survey_schema.dump(mentalhealthsurvey_object))


@answer.route("/<int:user_id>/<int:question_id>", methods=["PUT", "PATCH"])
@jwt_required
def answer_update(user_id, question_id):

    jwt_username = get_jwt_identity()
    jwt_user = User.query.get(jwt_username)

    answer_fields = answer_schema.load(request.json, partial=True)

    if not jwt_user:
        return abort(401, description="Invalid user")

    answer_object = Answer.query.filter_by(user_id=user_id, question_id=question_id).first()

    if not answer_object:
        return abort(401, description=f"Answer answered by user with id {user_id} and with question id {question_id} does not exist")

    answer_object.update(answer_fields)
    db.session.commit()

    return jsonify(answer_schema.dump(answer_object))



@answer.route("/<int:user_id>/<int:question_id>", methods=["DELETE"])
@jwt_required
def answer_delete(user_id, question_id):

    jwt_username = get_jwt_identity()

    answer_object = Option.query.filter_by(user_id=user_id, question_id=question_id).first()

    if not answer_object:
        return abort(401, description=f"Answer answered by user with id {user_id} and with question id {question_id} does not exist")

    json_object_to_return = jsonify(answer_schema.dump(answer_object))

    db.session.delete(answer_object)

    db.session.commit()

    return json_object_to_return
