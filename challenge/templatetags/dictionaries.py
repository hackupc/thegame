from django.template.defaulttags import register


@register.filter
def is_allowed(dictionary, challenge):
    return dictionary.get(challenge.topic, 1) >= challenge.order
