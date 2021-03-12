from flask import (
    Blueprint, render_template, redirect, url_for, flash, abort)
from flask_login import current_user, login_required
from controllers.web_users_controller import load_user
from models.WeeklyIncomeSource import WeeklyIncomeSource
from schemas.WeeklyIncomeSourceSchema import weekly_income_source_schema

from forms import (
    CreateWeeklyIncomeSource, UpdateWeeklyIncomeSource, DeleteButton,
    UnrecommendButton, RemoveButton)
from main import db

web_weeklyincomesource = Blueprint("web_weeklyincomesource", __name__, url_prefix="/web/web_weeklyincomesource")


@web_weeklyincomesource.route("/", methods=["GET"])
@login_required
def show_weeklyincomesources():
    user = load_user(current_user.get_id())
    weeklyincomesources = WeeklyIncomeSource.query.filter_by(user_id=user.id)

    empty = True
    if weeklyincomesources.first():
        empty = False


    form = DeleteButton()
    return render_template("weeklyincomesource.html", weeklyincomesources=weeklyincomesources, form=form, empty=empty)


@web_weeklyincomesource.route("/create", methods=["GET", "POST"])
@login_required
def create_weeklyincomesource():
    user = load_user(current_user.get_id())

    if not user:
        return abort(401, description="Unauthorised to view this page")

    form = CreateWeeklyIncomeSource()
    # print(form.job_title)
    # print(form.city)
    # print(form.validate_on_submit())
    if form.validate_on_submit():
        new_weeklyincomesource = WeeklyIncomeSource()
        new_weeklyincomesource.user_id = user.id
        new_weeklyincomesource.amount = form.amount.data
        new_weeklyincomesource.description = form.description.data
        new_weeklyincomesource.income_type = form.income_type.data
        new_weeklyincomesource.week_start = form.week_start.data
        new_weeklyincomesource.week_end = form.week_end.data

        db.session.add(new_weeklyincomesource)
        db.session.commit()
        flash("weeklyincomesource added!")
        return redirect(url_for("web_weeklyincomesource.show_weeklyincomesources"))

    return render_template("create_weeklyincomesource.html", form=form)


@web_weeklyincomesource.route("/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_weeklyincomesource(id):
    user = load_user(current_user.get_id())
    weeklyincomesource = WeeklyIncomeSource.query.filter_by(id=id, user_id=user.id)

    if weeklyincomesource.count() != 1:
        flash("Can't find weeklyincomesource")
        return redirect(url_for("web_weeklyincomesource.show_weeklyincomesources"))

    form = UpdateWeeklyIncomeSource(obj=weeklyincomesource.first())
    if form.validate_on_submit():
        data = {
            "amount": form.amount.data,
            "description": form.description.data,
            "income_type": form.income_type.data,
            "week_start": form.week_start.data,
            "week_end": form.week_end.data
        }
        fields = weekly_income_source_schema.load(data, partial=True)
        weeklyincomesource.update(fields)
        db.session.commit()
        flash("weeklyincomesource updated!")
        return redirect(url_for("web_weeklyincomesource.show_weeklyincomesources"))

    return render_template("update_weeklyincomesource.html", form=form, id=id)


@web_weeklyincomesource.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete_weeklyincomesource(id):
    form = DeleteButton()
    if form.submit.data:
        user = load_user(current_user.get_id())
        weeklyincomesource = WeeklyIncomeSource.query.filter_by(id=id).first()

        if not weeklyincomesource:
            flash("No weeklyincomesource found")
            return redirect(url_for("web_weeklyincomesource.show_weeklyincomesources"))

        db.session.delete(weeklyincomesource)
        db.session.commit()

        flash("weeklyincomesource deleted")
        return redirect(url_for("web_weeklyincomesource.show_weeklyincomesources"))


@web_weeklyincomesource.route("/<int:id>", methods=["GET"])
@login_required
def view_weeklyincomesource(id):
    user = load_user(current_user.get_id())

    weeklyincomesource = WeeklyIncomeSource.query.filter_by(id=id).first()

    if not weeklyincomesource:
        flash("weeklyincomesource not found")
        return redirect(
            url_for("web_weeklyincomesource.view_weeklyincomesource", id=weeklyincomesource.id))

    form1 = UnrecommendButton()
    form2 = RemoveButton()

    return render_template(
        "view_weeklyincomesource.html",
        weeklyincomesource=weeklyincomesource, form1=form1, form2=form2)
