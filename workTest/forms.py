from django import forms
from django.forms import ModelChoiceField

from .models import *


class RecruitQuestionsForm(forms.ModelForm):
    """Форма для теста"""
    question = ModelChoiceField(Question.objects.all(), widget=forms.HiddenInput())
    recruit = ModelChoiceField(Recruit.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = ResultTest
        fields = ['answer', 'question', 'recruit']

    def __init__(self, *args, **kwargs):
        super(RecruitQuestionsForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs.keys():
            self.fields['answer'].label = kwargs['initial']['question']


class RecruitForm(forms.ModelForm):
    """Форма для рекрута"""
    class Meta:
        model = Recruit
        fields = ['name', 'old', 'email', 'planet']


class SithChoiceForm(forms.Form):
    """Форма для Ситха"""
    sith = ModelChoiceField(Sith.objects.all())


class RecruitChoiceForm(forms.Form):
    """Форма для выбора рекрута"""
    sith = forms.IntegerField(widget=forms.HiddenInput())
    recruit = ModelChoiceField(Recruit.objects.none())

    def __init__(self, *args, **kwargs):
        qs = kwargs.pop('query')
        super(RecruitChoiceForm, self).__init__(*args, **kwargs)
        self.fields['recruit'].queryset = qs
