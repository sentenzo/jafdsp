import string
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


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
        return Survey.objects.filter(creator=self.request.user)


class NewSurvey(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')

    form_class = NewSurveyForm
    template_name = 'survey_app/base_content/creation_section/new_survey.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = "New Survey => Survey List"
        return context

    def form_valid(self, form):
        form.instance.creator_id = self.request.user.id
        return super(NewSurvey, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('survey_list')


class SurveyById(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')

    model = Question
    template_name = 'survey_app/base_content/creation_section/survey_by_id.html'
    context_object_name = 'questions'

    def get_context_data(self, *, object_list=None, **kwargs):
        survey = get_object_or_404(
            Survey, pk=self.kwargs['survey_id'], creator=self.request.user)
        context = super().get_context_data(**kwargs)
        context['data'] = f"Survey({survey.pk}) = > Question or New Question or Survey List"
        context["survey"] = survey
        return context

    def get_queryset(self):
        return Question.objects.filter(survey_id=int(self.kwargs["survey_id"]))


class NewQuestion(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')

    form_class = NewQuestionForm
    template_name = 'survey_app/base_content/creation_section/new_question.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        get_object_or_404(
            Survey, pk=self.kwargs['survey_id'], creator=self.request.user)
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
        survey = get_object_or_404(
            Survey, pk=self.kwargs['survey_id'], creator=self.request.user)
        question = get_object_or_404(
            Question, pk=self.kwargs['question_id'], survey=survey)
        context = super().get_context_data(**kwargs)
        context['data'] = f"Question ({self.kwargs['question_id']}) => New Option or Survey"
        context["survey"] = survey
        context["question"] = question
        return context

    def get_queryset(self):
        return Option.objects.filter(question_id=int(self.kwargs["question_id"]))


class NewOption(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')

    form_class = NewOptionForm
    template_name = 'survey_app/base_content/creation_section/new_option.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        survey = get_object_or_404(
            Survey, pk=self.kwargs['survey_id'], creator=self.request.user)
        question = get_object_or_404(
            Question, pk=self.kwargs['question_id'], survey=survey)

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


@login_required
def destroyer(request, object_name, object_id):
    object_type = {"survey": Survey}[object_name]
    obj = get_object_or_404(object_type, pk=object_id, creator=request.user)
    obj.delete()

    redirection = {"survey": "survey_list"}[object_name]
    return redirect(redirection)


@login_required
def publish_survey(request, survey_id):
    survey = get_object_or_404(
        Survey, pk=survey_id, creator=request.user, status=Survey.SurveyStatusEnum.DRAFT)

    from random import choices
    url_key = "".join(choices(string.ascii_letters + string.digits, k=16))

    survey.status = Survey.SurveyStatusEnum.PUBLISHED
    survey.url_key = url_key

    survey.save()

    return redirect("survey_by_id", survey_id=survey_id)


@login_required
def close_survey(request, survey_id):
    survey = get_object_or_404(
        Survey, pk=survey_id, creator=request.user, status=Survey.SurveyStatusEnum.PUBLISHED)
    survey.status = Survey.SurveyStatusEnum.CLOSED
    survey.save()

    return redirect("survey_by_id", survey_id=survey_id)


###########

class SurveyStart(DetailView):
    model = Survey
    template_name = 'survey_app/base_content/survey_section/survey_by_url_key_start.html'
    slug_url_kwarg = 'url_key'
    slug_field = 'url_key'
    context_object_name = 'survey'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = "Survey Start => Survey Submit"
        return context


class SurveySubmit(DetailView):
    model = Survey
    template_name = 'survey_app/base_content/survey_section/survey_by_url_key_submit.html'
    slug_url_kwarg = 'url_key'
    slug_field = 'url_key'
    context_object_name = 'survey'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = "Survey Submit => Survey Submit"

        questions = []
        for q in Question.objects.filter(survey=self.object):
            options = []
            for o in Option.objects.filter(question=q):
                value = f"o_{o.pk}"
                text = o.text
                options.append((value, text))
            question_text = q.text
            group_name = f"q_{q.pk}"
            t = (question_text, group_name, options)
            questions.append(t)

        context['questions'] = questions
        return context

    def post(self, request, *args, **kwargs):
        submission = Submission(survey=self.get_object())
        answers = []
        for key in request.POST:
            if key.startswith("q_"):
                try:

                    q_id = int(key[2:])
                    o_id = int(request.POST[key][2:])

                    question = get_object_or_404(Question, pk=q_id)
                    option = get_object_or_404(
                        Option, pk=o_id, question=question)

                    answer = Answer(submission=submission, option=option)
                    answers.append(answer)
                except:
                    return redirect("survey_submit", **kwargs)
        submission.save()
        [answer.save() for answer in answers]

        return redirect("survey_submit", **kwargs)


def survey_thanks(request, url_key):
    return HttpResponse("Survey Thanks => ∅")
