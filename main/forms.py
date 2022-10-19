from socket import fromshare
from django import forms
from .models import Academician, Comment

class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    check = forms.BooleanField(required=False)

class CommentAcademician(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        exclude = ["academician", "user"]

class CommentLecture(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        exclude = ["lecture", "user"]
    
        