from main import db
from flask import Blueprint

db_commands = Blueprint("db-custom", __name__)

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted")

@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables Created")

@db_commands.cli.command("seed")
def seed_db():
    
    from models.User import User
    from models.WeeklyIncomeSource import WeeklyIncomeSource
    from models.WeeklyExpenseSource import WeeklyExpenseSource
    from models.Answer import Answer
    from models.Option import Option
    from models.ProfileImage import ProfileImage
    from models.SurveyQuestion import SurveyQuestion
    from models.Specialist import Specialist
    from models.Question import Question
    from models.MentalHealthSurvey import MentalHealthSurvey
    from models.Insight import Insight
    from models.Goal import Goal
    from models.DailyPhysicalHealthRecord import DailyPhysicalHealthRecord
    from models.ExerciseLogItem import ExerciseLogItem


    from main import bcrypt
    from faker import Faker
    from random import randrange, choice

    from datetime import datetime

    now = datetime.now()

    faker = Faker()
    users_list = []
    gender_list = ["Male", "Female", "Other"]


    for i in range(5):

        user = User()

        user.first_name = faker.first_name()
        user.last_name = faker.last_name()
        user.created_at = now.strftime('%Y-%m-%d %H:%M:%S')
        user.email = f"test{i}@gmail.com"
        user.gender = choice(gender_list)
        user.password = bcrypt.generate_password_hash("123456").decode("utf-8")
        user.mobile = faker.phone_number()
        user.city = faker.city()
        user.country = faker.country()
        user.dob = faker.date_of_birth()

        db.session.add(user)
        users_list.append(user)
    
    db.session.commit()


    
    income_type_list = ["Ongoing", "One-off"]
    description_list = ["Salary from work", "Casual Coles Shift", "High School Tutoring", "Playing guitar at bar", "Casual retail assistant", "Welfare payment"]


    for i in range(20):

        weeklyincomesource = WeeklyIncomeSource()

        weeklyincomesource.description = choice(description_list)
        weeklyincomesource.income_type = choice(income_type_list)
        weeklyincomesource.amount = randrange(0,1000)
        weeklyincomesource.week_start = faker.date_of_birth()
        weeklyincomesource.week_end = faker.date_of_birth()
        weeklyincomesource.user_id = choice(users_list).id

        db.session.add(weeklyincomesource)


    expense_type_list = ["Ongoing", "One-off"]
    description_list = ["Rent for appartment", "Petrol for car", "Public transport fares", "Groceries", "Home insurance", "Electricity bill", "Gas bill"]


    for i in range(20):

        weeklyexpensesource = WeeklyExpenseSource()

        weeklyexpensesource.description = choice(description_list)
        weeklyexpensesource.expense_type = choice(expense_type_list)
        weeklyexpensesource.amount = randrange(0,1000)
        weeklyexpensesource.week_start = faker.date_of_birth()
        weeklyexpensesource.week_end = faker.date_of_birth()
        weeklyexpensesource.user_id = choice(users_list).id

        db.session.add(weeklyexpensesource)


    questions_list_1 = [
        "About how often did you feel tired out for no good reason?",
        "About how often did you feel nervous?",
        "About how often did you feel so nervous that nothing could calm you down?",
        "About how often did you feel hopeless?",
        "About how often did you feel restless or fidgety?",
        "About how often did you feel so restless you could not sit still?",
        "About how often did you feel depressed?",
        "About how often did you feel that everything was an effort?",
        "About how often did you feel so sad that nothing could cheer you up?",
        "About how often did you feel worthless?"
    ]

    questions_list_2 = [
        "How do you feel today?",
        "Are you tired?",
        "When did I last eat a whole meal?",
        "Do you feel healthy?",
        "How many times did you exercise last week?",
    ]

    options_list_1 = ["Never", "Once a week", "2-3 times a week", "Most of the time", "All the time"]
    options_list_2 = [
        ["Good", "Average", "Bad"],
        ["Yes", "No"],
        ["Today", "Yesterday", "A few days ago", "At least many days ago"],
        ["Yes", "No"],
        ["Not at all", "Once", "2-3 times", "Most days", "Everyday"]
    ]


    mental_health_survey1 = MentalHealthSurvey()
    mental_health_survey1.name = "How often you do things"

    db.session.add(mental_health_survey1)
    db.session.commit()

    question_number = 1

    for question_text in questions_list_1:

        question = Question()
        question.text = question_text

        db.session.add(question)
        db.session.commit()

        surveyquestion = SurveyQuestion()
        surveyquestion.mental_health_survey_id = mental_health_survey1.id
        surveyquestion.question_id = question.id
        surveyquestion.question_number = question_number

        question_number += 1


        db.session.add(surveyquestion)
        db.session.commit()

        for option_text in options_list_1:
            option = Option()
            option.question_id = question.id
            option.option_text = option_text
            db.session.add(option)
            db.session.commit()


    mental_health_survey2 = MentalHealthSurvey()
    mental_health_survey2.name = "Recent activities"

    db.session.add(mental_health_survey2)
    db.session.commit()

    question_number = 1

    for i in range(len(questions_list_2)):

        question = Question()
        question.text = questions_list_2[i]

        db.session.add(question)
        db.session.commit()

        surveyquestion = SurveyQuestion()
        surveyquestion.mental_health_survey_id = mental_health_survey2.id
        surveyquestion.question_id = question.id
        surveyquestion.question_number = question_number

        question_number += 1

        db.session.add(surveyquestion)
        db.session.commit()

        for option_text in options_list_2[i]:
            option = Option()
            option.question_id = question.id
            option.option_text = option_text

            db.session.add(option)
            db.session.commit()

    
    activity_list = ["Push ups", "Sit ups", "Chin ups", "5km run", "10km run", "Cruches", "Squats", "Bench press"]
    intensity_list = ["High", "Medium", "Low"]

    for i in range(20):

        exerciselogitem = ExerciseLogItem()

        exerciselogitem.description = choice(activity_list)
        exerciselogitem.date = faker.date_of_birth()
        exerciselogitem.time_start = faker.date_of_birth()
        exerciselogitem.time_end = faker.date_of_birth()
        exerciselogitem.intensity = choice(intensity_list)
        exerciselogitem.user_id = choice(users_list).id

        db.session.add(exerciselogitem)
        db.session.commit()

    date_list = [
        "2020-01-05", "2020-02-14", "2020-03-27", "2020-04-13", "2020-05-03", "2020-06-08", "2020-07-12", "2020-08-01", "2020-09-12", "2020-10-03",
        "2020-01-08", "2020-02-19", "2020-03-14", "2020-04-03", "2020-05-23", "2020-06-19", "2020-07-25", "2020-08-02", "2020-09-08", "2020-10-16"
    ]
    health_list = ["Physical", "Mental", "Financial"]
    insights_list = ["Improvement", "Deterioration"]
    description_list = ["Lost Weight", "Increased height", "More stressful mood", "Less sleep"]
    graph_list = ["Box plot", "Scatter plot", "Pie chart", "Bar graph"]
    unit_list = ["kgs", "hours", "minutes", "%"]
    degree_good_bad_list = ["Very good", "Good", "Neutral", "Bad", "Very bad"]

    for i in range(20):

        insight = Insight()

        insight.date = choice(date_list)
        insight.insight_type = choice(insights_list)
        insight.health_type = choice(health_list)
        insight.description = choice(description_list)
        insight.graph_type = choice(graph_list)
        insight.value = randrange(10, 100)
        insight.unit = choice(unit_list)
        insight.degree_good_bad = choice(degree_good_bad_list)

        insight.user_id = choice(users_list).id

        db.session.add(insight)
        db.session.commit()

    
    for i in range(20):

        dailyphysicalhealthrecord = DailyPhysicalHealthRecord()

        dailyphysicalhealthrecord.date = date_list[i]
        dailyphysicalhealthrecord.user_id = choice(users_list).id
        dailyphysicalhealthrecord.weight_kgs = randrange(50,120)
        dailyphysicalhealthrecord.height_cm = randrange(150,200)
        dailyphysicalhealthrecord.hearth_bpm = randrange(60,120)
        dailyphysicalhealthrecord.BMI = randrange(18,30)

        db.session.add(dailyphysicalhealthrecord)
        db.session.commit()


    
    db.session.commit()
    print("Tables seeded")