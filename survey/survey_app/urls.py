from django.urls import include, path

from .views import *

urlpatterns = [
    path('', landing, name="landing"),
    path('login/', LoginCreator.as_view(), name="login"),
    path('logout/', logout_creator, name='logout'),
    path('singup/', SingupCreator.as_view(), name="singup"),
    path('survey/list/', SurveyList.as_view(), name="survey_list"),

    path('survey/new/', NewSurvey.as_view(), name="new_survey"),
    path('survey/<int:survey_id>/', SurveyById.as_view(), name="survey_by_id"),

    path('survey/<int:survey_id>/question/new/',
         NewQuestion.as_view(), name="new_question"),
    path('survey/<int:survey_id>/question/<int:question_id>/',
         QuestionById.as_view(), name="question_by_id"),

    path('survey/<int:survey_id>/question/<int:question_id>/option/new/',
         NewOption.as_view(), name="new_option"),

    path('survey/<int:survey_id>/details/',
         survey_details, name="survey_details"),

    path('destroyer/<str:object_name>/<int:object_id>/',
         destroyer, name="destroyer"),
    path('publisher/<int:survey_id>/',
         publish_survey, name="publisher"),
    path('closer/<int:survey_id>/',
         close_survey, name="closer"),


    ###########

    path('survey/<str:url_key>/start/',
         SurveyStart.as_view(), name="survey_start"),
    path('survey/<str:url_key>/submit/',
         SurveySubmit.as_view(), name="survey_submit"),
    path('survey/<str:url_key>/thanks/', survey_thanks, name="survey_thanks"),

]
