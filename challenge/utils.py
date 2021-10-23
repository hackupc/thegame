from challenge.models import Challenge


def is_template(file):
    try:
        return Challenge.objects.get(file=file).type == Challenge.TYPE_HTML
    except Challenge.DoesNotExist:
        return False
