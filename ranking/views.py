from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Max
from django_tables2 import SingleTableView

from challenge.models import ChallengeUser
from ranking.tables import RankingTable


class RankingView(LoginRequiredMixin, SingleTableView):
    table_class = RankingTable
    template_name = 'ranking.html'

    def get_queryset(self):
        return ChallengeUser.objects.filter(success=True).values('user__username')\
            .annotate(count=Count('*'), time=Max('last_try')).order_by('-count', '-time')
