from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView


class FilesView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        file_name = kwargs.get('file')
        try:
            fs = FileSystemStorage()
            return FileResponse(fs.open(file_name))
        except FileNotFoundError:
            raise Http404


class IndexView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.username is None:
            return redirect(reverse('set_username'))
        return super().dispatch(request, *args, **kwargs)
