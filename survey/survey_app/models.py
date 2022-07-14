from django.conf import settings
from django.db import models


class Survey(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, verbose_name="Title")


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
