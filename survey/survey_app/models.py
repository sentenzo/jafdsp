from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Survey(models.Model):
    class SurveyStatusEnum(models.TextChoices):
        # created and available for editing
        DRAFT = "DRAFT"

        # published, respondents can answer auestions"
        PUBLISHED = "PUBLISHED"

        # respondents can't get access, creator can see the results"
        CLOSED = "CLOSED"

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Creation datetime")
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, verbose_name="Title")
    status = models.CharField(
        max_length=255,
        choices=SurveyStatusEnum.choices,
        default=SurveyStatusEnum.DRAFT,
    )
    url_key = models.CharField(
        max_length=255, verbose_name="URL key", null=True)


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, verbose_name="Question text")


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=1023, verbose_name="Option text")


class Submission(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)


class Answer(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
