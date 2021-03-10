from flask import Blueprint, abort, jsonify, request
from schemas.UserSchema import user_schema, users_schema
from models.User import User
from main import db, bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta
import zipfile
from os.path import basename
import sys
import os
import csv
from datetime import datetime
from pathlib import Path

now = datetime.now()

user = Blueprint("user",  __name__,  url_prefix="/user")

@user.route("/register", methods=["POST"])
def user_register():

    user_fields = user_schema.load(request.json)

    user_with_same_email = User.query.filter_by(email=user_fields["email"]).first()

    if user_with_same_email:
        return abort(400, description="Email already registered")
    
    user = User()

    user.email = user_fields["email"]
    user.first_name = user_fields["first_name"]
    user.last_name = user_fields["last_name"]
    user.created_at = user_fields["created_at"]
    user.dob = user_fields["dob"]
    user.gender = user_fields["gender"]
    user.mobile = user_fields["mobile"]
    user.city = user_fields["city"]
    user.country = user_fields["country"]

    user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")

    db.session.add(user)
    db.session.commit()

    return jsonify(user_schema.dump(user))
    

@user.route("/login", methods=["POST"])
def user_login():

    email_submitted = request.json["email"]
    password_submitted = request.json["password"]

    user = User.query.filter_by(email=email_submitted).first()

    if not user or not bcrypt.check_password_hash(user.password, password_submitted):
        return abort(401, description="Incorrect email and password")
    
    expiry = timedelta(days=1)
    access_token = create_access_token(identity=str(user.email), expires_delta=expiry)

    return jsonify({ "token": access_token })


@user.route("/", methods=["GET"])
def user_index():
    # Retrieve all users
    users = User.query.all()
    return jsonify(users_schema.dump(users))


