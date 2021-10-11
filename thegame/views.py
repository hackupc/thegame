from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from django.views import View


class FilesView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        file_name = kwargs.get('file')
        fs = FileSystemStorage()
        return FileResponse(fs.open(file_name))
