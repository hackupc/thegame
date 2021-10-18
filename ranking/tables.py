import django_tables2 as tables

from challenge.models import ChallengeUser


class RankingTable(tables.Table):
    count = tables.Column(verbose_name='Challenges')
    time = tables.TemplateColumn(template_code='<span name="dates">{{ record.time|date:"m/d/Y H:i:s T" }}</span>')

    class Meta:
        orderable = False
        model = ChallengeUser
        template_name = "django_tables2/bootstrap.html"
        fields = ['user__username', 'count', 'time']
        empty_text = "No challenges completed. Run and be the first one to succeed!"
