from controllers.WeeklyIncomeSource_controller import weeklyincomesource
from controllers.WeeklyExpenseSource_controller import weeklyexpensesource
from controllers.User_controller import user
from controllers.Insight_controller import insight
from controllers.Image_controller import image
from controllers.Specialist_controller import specialist
from controllers.Goal_controller import goal
from controllers.ExerciseLogItem_controller import exerciselogitem
from controllers.MentalHealthSurvey_controller import mentalhealthsurvey
from controllers.Question_controller import question
from controllers.SurveyQuestion_controller import surveyquestion
from controllers.Option_controller import option
from controllers.Answer_controller import answer
from controllers.web_users_controller import web_users
from controllers.web_weeklyexpensesource_controller import web_weeklyexpensesource
from controllers.web_weeklyincomesource_controller import web_weeklyincomesource

registerable_controllers = [
    weeklyincomesource,
    weeklyexpensesource,
    user,
    insight,
    image,
    specialist,
    goal,
    exerciselogitem,
    mentalhealthsurvey,
    surveyquestion,
    question,
    option,
    answer,
    web_users,
    web_weeklyexpensesource,
    web_weeklyincomesource
]