from flask import (
    Blueprint, render_template, redirect, url_for, flash, abort)
from flask_login import current_user, login_required
from controllers.web_users_controller import load_user
from models.WeeklyExpenseSource import WeeklyExpenseSource
from schemas.WeeklyExpenseSourceSchema import weekly_expense_source_schema

from forms import (
    CreateWeeklyExpenseSource, UpdateWeeklyExpenseSource, DeleteButton,
    UnrecommendButton, RemoveButton)
from main import db

web_weeklyexpensesource = Blueprint("web_weeklyexpensesource", __name__, url_prefix="/web/web_weeklyexpensesource")


@web_weeklyexpensesource.route("/", methods=["GET"])
@login_required
def show_weeklyexpensesources():
    user = load_user(current_user.get_id())
    weeklyexpensesources = WeeklyExpenseSource.query.filter_by(user_id=user.id)

    empty = True
    if weeklyexpensesources.first():
        empty = False

    form = DeleteButton()
    return render_template("weeklyexpensesource.html", weeklyexpensesources=weeklyexpensesources, form=form, empty=empty)


@web_weeklyexpensesource.route("/create", methods=["GET", "POST"])
@login_required
def create_weeklyexpensesource():
    user = load_user(current_user.get_id())

    if not user:
        return abort(401, description="Unauthorised to view this page")

    form = CreateWeeklyExpenseSource()
    # print(form.job_title)
    # print(form.city)
    # print(form.validate_on_submit())
    if form.validate_on_submit():
        new_weeklyexpensesource = WeeklyExpenseSource()
        new_weeklyexpensesource.user_id = user.id
        new_weeklyexpensesource.amount = form.amount.data
        new_weeklyexpensesource.description = form.description.data
        new_weeklyexpensesource.expense_type = form.expense_type.data
        new_weeklyexpensesource.week_start = form.week_start.data
        new_weeklyexpensesource.week_end = form.week_end.data

        db.session.add(new_weeklyexpensesource)
        db.session.commit()
        flash("weeklyexpensesource added!")
        return redirect(url_for("web_weeklyexpensesource.show_weeklyexpensesources"))

    return render_template("create_weeklyexpensesource.html", form=form)


@web_weeklyexpensesource.route("/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_weeklyexpensesource(id):
    user = load_user(current_user.get_id())
    weeklyexpensesource = WeeklyExpenseSource.query.filter_by(id=id, user_id=user.id)

    if weeklyexpensesource.count() != 1:
        flash("Can't find weeklyexpensesource")
        return redirect(url_for("web_weeklyexpensesource.show_weeklyexpensesources"))

    form = UpdateWeeklyExpenseSource(obj=weeklyexpensesource.first())
    if form.validate_on_submit():
        data = {
            "amount": form.amount.data,
            "description": form.description.data,
            "expense_type": form.expense_type.data,
            "week_start": form.week_start.data,
            "week_end": form.week_end.data
        }
        fields = weekly_expense_source_schema.load(data, partial=True)
        weeklyexpensesource.update(fields)
        db.session.commit()
        flash("weeklyexpensesource updated!")
        return redirect(url_for("web_weeklyexpensesource.show_weeklyexpenseources"))

    return render_template("update_weeklyexpensesource.html", form=form, id=id)


@web_weeklyexpensesource.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete_weeklyexpensesource(id):
    form = DeleteButton()
    if form.submit.data:
        user = load_user(current_user.get_id())
        weeklyexpensesource = WeeklyExpenseSource.query.filter_by(id=id).first()

        if not weeklyexpensesource:
            flash("No weeklyexpensesource found")
            return redirect(url_for("web_weeklyexpensesource.show_weeklyexpensesources"))

        db.session.delete(weeklyexpensesource)
        db.session.commit()

        flash("weeklyexpensesource deleted")
        return redirect(url_for("web_weeklyexpensesource.show_weeklyexpensesources"))


@web_weeklyexpensesource.route("/<int:id>", methods=["GET"])
@login_required
def view_weeklyexpensesource(id):
    user = load_user(current_user.get_id())

    weeklyexpensesource = WeeklyExpenseSource.query.filter_by(id=id).first()

    if not weeklyexpensesource:
        flash("weeklyexpensesource not found")
        return redirect(
            url_for("web_weeklyexpensesource.view_weeklyexpensesource", id=weeklyexpensesource.id))

    form1 = UnrecommendButton()
    form2 = RemoveButton()

    return render_template(
        "view_weeklyexpensesource.html",
        weeklyexpensesource=weeklyexpensesource, form1=form1, form2=form2)