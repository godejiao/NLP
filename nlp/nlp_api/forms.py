# -*- coding: utf-8 -*-
from django import forms

class SearchForm(forms.Form):
    text=forms.CharField()
    type=forms.CharField()
    engine=forms.CharField()

class SearchKeyWordsFrom(forms.Form):
    text = forms.CharField()
    type = forms.CharField()
    engine = forms.CharField()
    title = forms.CharField()
    channel = forms.CharField()

#
# from django import forms
# class ContactForm(forms.Form):
#     subject = forms.CharField()
#     email = forms.EmailField(required=False)
#     message = forms.CharField()