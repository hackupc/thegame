from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page


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


class CacheMixin(object):
    cache_timeout = 60

    def get_cache_timeout(self):
        force_update = self.request.GET.get('force_update', None)
        if force_update == 'true':
            # Disable cache if the query param: force_update=true is recieved.
            return 0
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout())(super(CacheMixin, self).dispatch)(*args, **kwargs)
