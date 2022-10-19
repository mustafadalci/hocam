from cgitb import text
from site import USER_BASE
from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ToDoList, Item, Academician, Comment, Lecture
from .forms import CommentAcademician, CreateNewList, CommentLecture
from django.contrib.auth.models import User
from django.db.models import Avg, Count



# Create your views here.

def index(response, id):
    ls = ToDoList.objects.get(id = id)
 
    if response.method == "POST":
        print(response.POST)
        if response.POST.get("save"):
            for item in ls.item_set.all():
                if response.POST.get("c" + str(item.id)) == "clicked":
                    item.complete = True
                else:
                    item.complete = False
                
                item.save()

        elif response.POST.get("newItem"):
            txt = response.POST.get("new")
            if len(txt) > 2:
                ls.item_set.create(text = txt, complete = False)
            else:
                print("invalid")


    return render(response, "main/list.html", {"ls": ls})

def home(response):
    return render(response, "main/home.html", {})

    
    
    

def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name = n)
            t.save()

    else:
        form = CreateNewList()

    return render(response, "main/create.html", {"form" : form})

def academician(response, name):
    user = response.user
    academician = Academician.objects.get(name = name)
    lectures = academician.lecture_set.all().order_by("name")
    form = CommentAcademician()
    form.fields["lecture"].queryset = Lecture.objects.filter(academician__name__startswith = academician.name)
    
    comment = Comment.objects.all()
    rating_avg = Comment.objects.filter(academician = academician.id).aggregate(rating_avg = Avg('rating'), comment_count = Count("text"))
    rating_avg["rating_avg"] = round(rating_avg["rating_avg"],2)
    if response.method == "POST":
        form = CommentAcademician(response.POST,  response.FILES)
        if form.is_valid():
            form.instance.academician = Academician.objects.get(name = name)
            form.instance.user = response.user
            form.save()

    return render(response, "main/academician.html", {"academician" : academician, "form" : form, "comment" : comment, "user" : user, "lectures" : lectures, "rating_avg" : rating_avg })

def lecture(response, name):
    user = response.user
    lecture = Lecture.objects.get(name = name)
    form = CommentLecture()
    form.fields["academician"].queryset = Academician.objects.filter(lecture__name__startswith = lecture.name)
    academicians = Academician.objects.all()
    comment = Comment.objects.all()

    if response.method == "POST":
        form = CommentLecture(response.POST,  response.FILES)
        if form.is_valid():
            form.instance.lecture = Lecture.objects.get(name = name)
            form.instance.user = response.user
            form.save()
    
    return render(response, "main/lecture.html", {"lecture" : lecture, "form" : form, "comment" : comment, "user" : user, "academicians" : academicians})

def academicians(response):
    academicians = Academician.objects.all().order_by("name")

    return render(response, "main/academicians.html", {"academicians" : academicians})

def mycomments(response):
    user = response.user
    comments = Comment.objects.all()
    return render(response, "main/my-comments.html",{"user" : user, "comments" : comments})

def delete_comment(response, comment_id):
    comment = Comment.objects.get(id = comment_id)
    comment.delete()

    return redirect("/my-comments")



def lectures(response):
    lectures = Lecture.objects.all().order_by("name")
    return render(response, "main/lectures.html", {"lectures" : lectures})

def profile(response):
    comments = Comment.objects.all().filter(user = response.user )
    return render(response, "main/profile.html", {"comments" : comments})