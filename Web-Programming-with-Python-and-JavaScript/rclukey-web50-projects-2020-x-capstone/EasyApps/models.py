from django.contrib.auth.models import AbstractUser
from django.db import models

from django import forms

# Create your models here.
class College(models.Model):
    college_name = models.CharField(max_length=64, default="", blank=True, null=True)
    location = models.CharField(max_length=100, default="", blank=True, null=True)
    accept_rate = models.FloatField(default=0, blank=True, null=True)
    tuition = models.CharField(max_length=10, default="", blank=True, null=True)
    student_to_faculty = models.CharField(max_length=10, default="", blank=True, null=True)
    school_size = models.CharField(max_length=10, default="", blank=True, null=True)

    def __str__(self):
        return f"{self.college_name}"

class User(AbstractUser, models.Model):
    age = models.IntegerField(default=0, blank=True, null=True)
    gender = models.CharField(max_length=20, default="", blank=True, null=True)
    ethnicity = models.CharField(max_length=20, default="", blank=True, null=True)
    military = models.CharField(max_length=5, default="")
    picture = models.URLField(max_length=200, default="", blank=True, null=True)
    personal = models.TextField(default="", blank=True, null=True)
    university = models.CharField(max_length=64, default="", null=True)

    def __str__(self):
        return f"{self.username}"

class Question(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="questions")
    essay_question = models.TextField(default="", blank=True, null=True)

    def __str__(self):
        return f"{self.college.college_name}: {self.essay_question}"

class Answer(models.Model):
    college_name = models.ForeignKey(College, on_delete=models.CASCADE, related_name="application_answers")
    applier = models.ForeignKey(User, on_delete=models.CASCADE, related_name="application_appliers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    essay_answer = models.TextField(default="")

    def __str__(self):
        return f"{self.applier.username} answered {self.question.essay_question}"

class Question_Answer(models.Model):
    question = models.ManyToManyField(Question)
    answer = models.ManyToManyField(Answer)

class Application(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="college_applications")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_applications")
    question_answer_pair = models.ManyToManyField(Question_Answer)
    application_status = models.CharField(max_length=5, default="", null=True)

    def __str__(self):
        return f"{self.user.username} applied to {self.college.college_name}"