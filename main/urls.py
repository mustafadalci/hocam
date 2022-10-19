from django.urls import path
from . import views

urlpatterns = [
    path("<int:id>", views.index, name = "index"),  
    path("home", views.home, name = "home"),
    path("", views.home, name = "home"),
    path("create/", views.create, name = "create"),
    path("academicians/<str:name>", views.academician, name = "academician"),  
    path("academicians", views.academicians, name = "academicians"),
    path("my-comments", views.mycomments, name = "mycomments"),
    path("lectures", views.lectures, name = "lectures"),
    path("lectures/<str:name>", views.lecture, name = "lecture"),
    path("delete_comment/<comment_id>", views.delete_comment, name = "delete-comment"),
    path("profile", views.profile, name = "profile"),

]
