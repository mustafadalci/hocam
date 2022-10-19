from django.contrib import admin
from .models import ToDoList, Item, Department, Lecture, Academician, Comment

# Register your models here.

admin.site.register(ToDoList)
admin.site.register(Item)
admin.site.register(Department)
admin.site.register(Lecture)
admin.site.register(Academician)
admin.site.register(Comment)
