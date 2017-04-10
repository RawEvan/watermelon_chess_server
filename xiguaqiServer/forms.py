# coding:utf-8
from django import forms


class roomForm(forms.Form):
    roomID = forms.IntegerField()
    name = forms.CharField(max_length=100)
