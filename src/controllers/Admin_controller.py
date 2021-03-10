from flask import Blueprint, abort, jsonify, request
from schemas.UserSchema import user_schema, users_schema
from models.User import User
from models.Admin import Admin
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
from schemas.AdminSchema import admin_schema

now = datetime.now()

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/login", methods=["POST"])
def admin_login():
    admin_fields = admin_schema.load(request.json)

    admin = Admin.query.filter_by(username=admin_fields["username"]).first()

    if not admin or not bcrypt.check_password_hash(
            admin.password, admin_fields["password"]):
        return abort(401, description="Incorrect username and password")

    expiry = timedelta(hours=2)
    access_token = create_access_token(
        identity=str(admin.admin_id), expires_delta=expiry)

    return jsonify({"token": access_token})



@admin.route("/downloadalldata", methods=["GET"])
@jwt_required
def download_all_data():

    dir = Path.cwd().joinpath("data")
    admin_id = get_jwt_identity()

    admin = Admin.query.get(admin_id)

    if not admin:
        return abort(401, description="Invalid admin user")

    cursor = db.session.connection().connection.cursor()
    cursor.execute(
        """SELECT tablename
        FROM pg_catalog.pg_tables
        WHERE schemaname = 'public' """)
    table_names = cursor.fetchall()

    print("table names are " + str(table_names))

    names = []
    for name in table_names:
        names.append(*name)

    timestamp = now.strftime('%Y%m%d_%H%M%S')

    for table in names:
        result = db.engine.execute(f"SELECT * FROM {table};").fetchall()
        filename = dir.joinpath(f"{table}__{timestamp}.csv")

        with open(filename, "w", encoding="utf-8") as file:
            csv.writer(file).writerows(result)

    return "data exported"