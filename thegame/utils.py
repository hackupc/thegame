from django.conf import settings


def get_substitutions_templates(request):
    return {
        'app_name': settings.APP_NAME,
    }
