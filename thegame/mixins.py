from django.views.decorators.cache import cache_page


class CacheMixin(object):
    cache_timeout = 60
    # timeout is calculated in seconds

    def get_cache_timeout(self):
        force_update = self.request.GET.get('force_update', None)
        if force_update == 'true':
            # Disable cache if the query param: force_update=true is recieved.
            return 0
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout())(super(CacheMixin, self).dispatch)(*args, **kwargs)
