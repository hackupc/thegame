from django import forms

from challenge.models import Challenge, ChallengeUser, File


class ChallengeAdminForm(forms.ModelForm):
    solution_code = forms.CharField(initial='', required=False, widget=forms.Textarea(attrs={'rows': 1}))

    def save(self, commit=True):
        solution_code = self.cleaned_data.get('solution_code', '')
        if solution_code != '':
            self.instance.set_solution(solution_code)
        return super().save(commit)

    class Meta:
        model = Challenge
        exclude = ['solution']


class ChallengeTryForm(forms.Form):
    code = forms.CharField(initial='', required=True, max_length=1000)


class VoteForm(forms.ModelForm):
    class Meta:
        fields = ('vote', 'comment')
        model = ChallengeUser


class FileAdminForm(forms.ModelForm):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data.get('file')
        return file.read()

    class Meta:
        model = File
        exclude = ['id']
