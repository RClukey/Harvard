from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView

import json

from .models import User, College, Question, Answer, Application, Question_Answer

# Create your views here.
def handle_uploaded_file(f):
    with open("some/file/name.txt", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def index(request):
    all_universities = College.objects.all().order_by('college_name').values()

    try:
        university = College.objects.get(college_name=request.user.university)
        is_college = True
        college_id = university.id
    except:
        is_college = False
        college_id=0
    
    return render(request, "EasyApps/index.html", {
        "is_college": is_college,
        "college_id": college_id,
        "universities": all_universities,
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "EasyApps/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "EasyApps/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "EasyApps/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "EasyApps/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "EasyApps/register.html")

def profile(request, user):
    profile_user = User.objects.get(username=user)
    
    try:
        university = College.objects.get(college_name=request.user.university)
        is_college = True
        college_id = university.id
    except:
        is_college = False
        college_id = 0
        application = ""
        application_college = ""

    try:
        app = Application.objects.get(college = university, user=profile_user)
        application_status = app.application_status
    except:
        application_status = ""

    if is_college:
        try:
            application = Answer.objects.filter(college_name=university, applier=profile_user)
            application_college = university.college_name
        except:
            application = ""
            application_college = ""

    return render(request, "EasyApps/profile.html", {
        "profile_user": profile_user,
        "is_college": is_college,
        "college_id": college_id,
        "application": application,
        "application_college": application_college,
        "application_status": application_status,
    })

def uni(request, college):
    try:
        university = College.objects.get(college_name=request.user.university)
        is_college = True
        college_id = university.id
    except:
        is_college = False
        college_id=0

    university = College.objects.get(id=college)
    questions = Question.objects.filter(college=university)
    all_apps = Application.objects.filter(college=college, application_status="")

    try:
        apps = Application.objects.get(college=college, user=request.user)
        application_status = apps.application_status
    except:
        application_status = ""

    quest = []
    for question in questions:
        quest.append(question.essay_question)
    
    ans = []

    try:
        for question in questions:
            answer = Answer.objects.get(college_name=university, applier=request.user, question=question)
            ans.append(answer.essay_answer)
        edit_app = True
    except:
        edit_app = False

    try:
        app = Application.objects.get(college = university, user=request.user)
        not_submitted = False
    except:
        not_submitted = True

    return render(request, "EasyApps/college.html", {
        "college": university,
        "questions": quest,
        "answers": ans,
        "all_applications": all_apps,
        "edit_app": edit_app,
        "not_submitted": not_submitted,
        "is_college": is_college,
        "college_id": college_id,
        "application_status": application_status,
    })

def apply(request, college_id):
    if request.method == 'POST':
        college = College.objects.get(id=college_id)
        questions = Question.objects.filter(college=college)
        count = questions.count()

        quest = []
        for question in questions:
            quest.append(question)
        
        if "save_application" in request.POST:
            try:
                all_answer = Answer.objects.filter(college_name=college, applier=request.user)

                for i in range(0, count):
                    answer = request.POST[f"answer_to_question_{i+1}"]
                    a = Answer.objects.get(college_name=college, applier=request.user, question=quest[i])
                    a.essay_answer = answer
                    a.save()

            except:
                for i in range(0, count):
                    answer = request.POST[f"answer_to_question_{i+1}"]
                    a = Answer(college_name=college, applier=request.user, question=quest[i], essay_answer=answer)
                    a.save()
        
        elif "submit_application" in request.POST:
            try:
                all_answer = Answer.objects.filter(college_name=college, applier=request.user)

                for i in range(0, count):
                    answer = request.POST[f"answer_to_question_{i+1}"]
                    a = Answer.objects.get(college_name=college, applier=request.user, question=quest[i])
                    a.essay_answer = answer
                    a.save()

            except:
                for i in range(0, count):
                    answer = request.POST[f"answer_to_question_{i+1}"]
                    a = Answer(college_name=college, applier=request.user, question=quest[i], essay_answer=answer)
                    a.save()

            app = Application(college=college, user=request.user)
            app.save()

            for i in range(0, count):
                answers = Answer.objects.get(college_name=college, applier=request.user, question=quest[i])
                question_answer = Question_Answer()
                question_answer.save()
                question_answer.question.add(quest[i])
                question_answer.answer.add(answers)

                app.question_answer_pair.add(question_answer)
    
    return HttpResponseRedirect(reverse("uni",args=(college_id, )))

def edit_profile(request, user_id):
    if request.method == "POST":
        user = User.objects.get(id=user_id)
        username = user.username

        user.age = request.POST['age']
        user.gender = request.POST['gender']
        user.ethnicity = request.POST['ethnicity']
        user.military = request.POST['military']
        user.picture = request.POST['picture']
        user.personal = request.POST['personal']

        user.save()

        return HttpResponseRedirect(reverse("profile",args=(username, )))

def accept(request, college, profile):
    university = College.objects.get(college_name=college)
    user = User.objects.get(username=profile)
    application = Application.objects.get(college=university, user=user)

    print(application)

    if request.method == "POST":
        if "accept" in request.POST:
            application.application_status = "Accept"
            application.save()
        elif "deny" in request.POST:
            application.application_status = "Deny"
            application.save()
    
    college_id = university.id
    return HttpResponseRedirect(reverse("uni",args=(college_id, )))
