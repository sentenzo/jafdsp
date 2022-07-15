from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy

from .forms import *
from .models import *


def landing(request):
    return render(request, 'survey_app/base_content/creation_section/landing.html',
                  context={"data": "Landing => Create Survey or Login or Singup"})


class LoginCreator(LoginView):
    form_class = LoginCreatorForm
    template_name = 'survey_app/base_content/creation_section/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = "Login => Landing or Login or Singup"
        return context

    def get_success_url(self):
        return reverse_lazy('survey_list')


class SingupCreator(CreateView):
    form_class = SingupCreatorForm
    template_name = 'survey_app/base_content/creation_section/singup.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = "Singup => Landing or Login or Singup"
        return context

    def get_success_url(self):
        return reverse_lazy('survey_list')


class SurveyList(ListView):
    model = Survey

    template_name = 'survey_app/base_content/creation_section/survey_list.html'
    context_object_name = 'surveys'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = "Survey List => Survey or New Survey or Survey Details"
        tr_class_choise = {
            Survey.SurveyStatusEnum.DRAFT.value: "table-primary",
            Survey.SurveyStatusEnum.PUBLISHED.value: "table-info",
            Survey.SurveyStatusEnum.CLOSED.value: "table-success",
        }
        context['tr_class_choise'] = tr_class_choise
        return context

    def get_queryset(self):
        return Survey.objects.all()


class NewSurvey(CreateView):
    form_class = NewSurveyForm
    template_name = 'survey_app/base_content/creation_section/new_survey.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = "New Survey => Survey List"
        return context

    def get_success_url(self):
        return reverse_lazy('survey_list')


class SurveyById(DetailView):
    model = Survey
    template_name = 'survey_app/base_content/creation_section/survey_by_id.html'
    pk_url_kwarg = 'survey_id'
    context_object_name = 'survey'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = f"Survey({self.kwargs['survey_id']}) = > Question or New Question or Survey List"
        return context


def new_question(request, survey_id):
    return HttpResponse("New Question => Survey")


def question(request, survey_id, question_id):
    return HttpResponse("Question ({question_id}) => New Option or Survey")


def new_option(request, survey_id, question_id):
    return HttpResponse("New Option => Question")


def survey_details(request, survey_id):
    return HttpResponse("Survey Details => Survey List")

###########


def survey_start(request, survey_id):
    return HttpResponse("Survey Start => Survey Submit")


def survey_submit(request, survey_id):
    return HttpResponse("Survey Submit => Survey Submit")


def survey_thanks(request, survey_id):
    return HttpResponse("Survey Thanks => ∅")
