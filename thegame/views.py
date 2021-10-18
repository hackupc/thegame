from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View


class FilesView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        file_name = kwargs.get('file')
        fs = FileSystemStorage()
        return FileResponse(fs.open(file_name))


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.username is None:
            return redirect(reverse('set_username'))
        return redirect(reverse('challenge-index'))
