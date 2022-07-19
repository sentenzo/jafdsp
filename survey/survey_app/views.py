from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout


from .forms import *
from .models import *


def landing(request):
    is_authenticated = request.user.is_authenticated
    user_name = request.user.username if is_authenticated else "Anonymous"
    return render(request, 'survey_app/base_content/creation_section/landing.html',
                  context={
                      "data": "Landing => Create Survey or Login or Singup",
                      "is_authenticated": is_authenticated,
                      "user_name": user_name,
                  })


class LoginCreator(LoginView):
    form_class = LoginCreatorForm
    template_name = 'survey_app/base_content/creation_section/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = "Login => Landing or Login or Singup"
        return context

    def get_success_url(self):
        return reverse_lazy('landing')


def logout_creator(request):
    logout(request)
    return redirect('landing')


class SingupCreator(CreateView):
    form_class = SingupCreatorForm
    template_name = 'survey_app/base_content/creation_section/singup.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = "Singup => Landing or Login or Singup"
        return context

    def get_success_url(self):
        return reverse_lazy('survey_list')


class SurveyList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')

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


class NewSurvey(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')

    form_class = NewSurveyForm
    template_name = 'survey_app/base_content/creation_section/new_survey.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = "New Survey => Survey List"
        return context

    def get_success_url(self):
        return reverse_lazy('survey_list')


class SurveyById(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')

    model = Question
    template_name = 'survey_app/base_content/creation_section/survey_by_id.html'
    context_object_name = 'questions'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = f"Survey({self.kwargs['survey_id']}) = > Question or New Question or Survey List"
        context["survey"] = Survey.objects.get(pk=self.kwargs['survey_id'])
        return context

    def get_queryset(self):
        return Question.objects.filter(survey_id=int(self.kwargs["survey_id"]))


class NewQuestion(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')

    form_class = NewQuestionForm
    template_name = 'survey_app/base_content/creation_section/new_question.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = "New Question => Survey"
        return context

    def form_valid(self, form):
        survey = get_object_or_404(Survey, pk=self.kwargs["survey_id"])
        form.instance.survey_id = survey.id
        return super(NewQuestion, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('survey_by_id', kwargs={'survey_id': self.kwargs['survey_id']})


class QuestionById(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')

    model = Option
    template_name = 'survey_app/base_content/creation_section/question_by_id.html'
    context_object_name = 'options'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = f"Question ({self.kwargs['question_id']}) => New Option or Survey"
        context["survey"] = Question.objects.get(pk=self.kwargs['survey_id'])
        context["question"] = Question.objects.get(
            pk=self.kwargs['question_id'])
        return context

    def get_queryset(self):
        return Option.objects.filter(question_id=int(self.kwargs["question_id"]))


class NewOption(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')

    form_class = NewOptionForm
    template_name = 'survey_app/base_content/creation_section/new_option.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = "New Option => Question"
        return context

    def form_valid(self, form):
        question = get_object_or_404(Question, pk=self.kwargs["question_id"])
        form.instance.question_id = question.id
        return super(NewOption, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('question_by_id', kwargs={'survey_id': self.kwargs['survey_id'], 'question_id': self.kwargs['question_id']})


def survey_details(request, survey_id):
    return HttpResponse("Survey Details => Survey List")

###########


def survey_start(request, survey_id):
    return HttpResponse("Survey Start => Survey Submit")


def survey_submit(request, survey_id):
    return HttpResponse("Survey Submit => Survey Submit")


def survey_thanks(request, survey_id):
    return HttpResponse("Survey Thanks => ∅")
