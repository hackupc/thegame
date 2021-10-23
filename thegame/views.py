from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from challenge.utils import is_template


class FilesView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        file_name = kwargs.get('file')
        if is_template(file_name):
            raise PermissionDenied()
        try:
            fs = FileSystemStorage()
            return FileResponse(fs.open(file_name))
        except FileNotFoundError:
            raise Http404


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.username is None:
            return redirect(reverse('set_username'))
        return redirect(reverse('challenge-index'))
