import django_tables2 as tables

from challenge.models import ChallengeUser


class ChallengeStatsTable(tables.Table):
    first_try = tables.TemplateColumn(template_code='<span name="dates">'
                                                    '{{ record.first_try|date:"m/d/Y H:i:s T" }}</span>')
    last_try = tables.TemplateColumn(template_code='<span name="dates">'
                                                   '{{ record.last_try|date:"m/d/Y H:i:s T" }}</span>')

    class Meta:
        orderable = False
        model = ChallengeUser
        template_name = "django_tables2/bootstrap.html"
        fields = ['user__username', 'user__email', 'total_attempts', 'last_try', 'first_try', 'success']
        empty_text = "User hasn't tried this challenge yet"
