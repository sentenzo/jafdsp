from django.urls import include, path

from .views import *

urlpatterns = [
    path('', landing, name="landing"),
    path('login/', LoginCreator.as_view(), name="login"),
    path('singup/', SingupCreator.as_view(), name="singup"),
    path('survey/list/', SurveyList.as_view(), name="survey_list"),

    path('survey/new/', NewSurvey.as_view(), name="new_survey"),
    path('survey/<int:survey_id>/', SurveyById.as_view(), name="survey_by_id"),

    path('survey/<int:survey_id>/question/new/',
         NewQuestion.as_view(), name="new_question"),
    path('survey/<int:survey_id>/question/<int:question_id>/',
         QuestionById.as_view(), name="question_by_id"),

    path('survey/<int:survey_id>/question/<int:question_id>/option/new/',
         new_option, name="new_option"),

    path('survey/<int:survey_id>/details/',
         survey_details, name="survey_details"),

    ###########

    path('survey/<int:survey_id>/start/', survey_start, name="survey_start"),
    path('survey/<int:survey_id>/submit/', survey_submit, name="survey_submit"),
    path('survey/<int:survey_id>/thanks/', survey_thanks, name="survey_thanks"),

]
