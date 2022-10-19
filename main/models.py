from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ToDoList(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Item(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete = models.CASCADE)
    text =  models.CharField(max_length=300)
    complete = models.BooleanField()

    def __str__(self):
        return self.text

class Department(models.Model):
    name = models.CharField(max_length=500)
    def __str__(self):
        return self.name

class Academician(models.Model):
    name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete = models.CASCADE)
    def __str__(self):
        return self.name

class Lecture(models.Model):
    name = models.CharField(max_length=400)
    academician = models.ManyToManyField(Academician)
    def __str__(self):
        return self.name

RATE_CHOICES = [
    (1, "1 - Very Bad"),
    (2, "2 - Bad"),
    (3, "3 - Neutral"),
    (4, "4 - Good"),
    (5, "5 - Very Good")
]

class Comment(models.Model):
    academician = models.ForeignKey(Academician, on_delete = models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete = models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name= "user", null=True)
    rating = models.PositiveSmallIntegerField(choices = RATE_CHOICES, null = True)
    text =  models.CharField(max_length=10000)
    live = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add= True)


    def __str__(self):
        return self.text


