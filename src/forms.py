from flask_wtf import FlaskForm
from wtforms import (
    StringField, BooleanField, SubmitField,
    PasswordField, SelectField, IntegerField, DateField)
from wtforms.validators import DataRequired, Length, EqualTo


class RegistrationForm(FlaskForm):


    email = StringField('email', validators=[DataRequired()])
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    dob = DateField('dob', validators=[DataRequired()])
    gender = StringField('gender')
    mobile = StringField('mobile', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    country = StringField('country', validators=[DataRequired()])
    password = PasswordField(
        'password', validators=[DataRequired(), Length(min=2)])
    confirm = PasswordField(
        'confirm password', validators=[DataRequired(), EqualTo(
            'password', message='Passwords must match')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class UpdateUserForm(FlaskForm):
    first_name = StringField('first_name')
    last_name = StringField('last_name')
    dob = DateField('dob', validators=[DataRequired()])
    gender = StringField('gender')
    mobile = StringField('mobile')
    city = StringField('city')
    country = StringField('country')
    submit = SubmitField("Update Details")


class DeleteButton(FlaskForm):
    submit = SubmitField("Delete")


class CreateWeeklyExpenseSource(FlaskForm):
    amount = IntegerField("amount", validators=[DataRequired()])
    description = StringField("description", validators=[DataRequired(), Length(min=1)])
    expense_type = StringField("expense type", validators=[DataRequired(), Length(min=1)])
    week_start = DateField("week start", validators=[DataRequired()])
    week_end = DateField("week end", validators=[DataRequired()])

    submit = SubmitField("Create Weekly Expense Source")

class CreateWeeklyIncomeSource(FlaskForm):
    amount = IntegerField("amount", validators=[DataRequired()])
    description = StringField("description", validators=[DataRequired(), Length(min=1)])
    income_type = StringField("income type", validators=[DataRequired(), Length(min=1)])
    week_start = DateField("week start", validators=[DataRequired()])
    week_end = DateField("week end", validators=[DataRequired()])

    submit = SubmitField("Create Weekly Income Source")


class UpdateWeeklyExpenseSource(CreateWeeklyExpenseSource):
    submit = SubmitField("Update Weekly Expense Source")

class UpdateWeeklyIncomeSource(CreateWeeklyIncomeSource):
    submit = SubmitField("Update Weekly Income Source")


class UnrecommendButton(FlaskForm):
    submit = SubmitField("Unrecommend")


class RemoveButton(FlaskForm):
    submit = SubmitField("Remove")


