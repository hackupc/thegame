from django import forms
from django.forms import ModelForm, Form

from challenge.models import Challenge


class ChallengeAdminForm(ModelForm):
    solution_code = forms.CharField(initial='', required=False)

    def save(self, commit=True):
        solution_code = self.cleaned_data.get('solution_code', '')
        if solution_code != '':
            self.instance.set_solution(solution_code)
        self.instance.check_solution(solution_code)
        return super().save(commit)

    class Meta:
        model = Challenge
        exclude = ['solution']


class ChallengeTryForm(Form):
    code = forms.CharField(initial='', required=True)
