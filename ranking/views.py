from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Max
from django_tables2 import SingleTableView
from django.http import JsonResponse

from challenge.models import ChallengeUser
from ranking.tables import RankingTable
from django.views import View

from thegame.views import CacheMixin


class RankingView(LoginRequiredMixin, SingleTableView):
    table_class = RankingTable
    template_name = 'ranking.html'

    def get_queryset(self):
        return ChallengeUser.objects.filter(success=True).values('user__username')\
            .annotate(count=Count('*'), time=Max('last_try')).order_by('-count', 'time')


class ChartView(CacheMixin, LoginRequiredMixin, View):

    def get(self, request, *args, **kwaergs):
        # Get all Successful attempts
        allEntries = list(ChallengeUser.objects.filter(success=True)
                          .values('user__username', 'last_try', 'total_attempts').order_by('last_try'))

        allPlayers = {}
        pointsCounter = {}
        # Classify them by player, in chronological order.
        for successes in allEntries:
            pointsCounter[successes['user__username']] = pointsCounter.get(successes['user__username'], 0) + 1
            playerDb = allPlayers.get(successes['user__username'], [])
            playerDb.append({"x": successes['last_try'], "y": pointsCounter[successes['user__username']]})
            allPlayers[successes['user__username']] = playerDb

        # Get the ranking and slice it to the first 10
        top10 = ChallengeUser.objects.filter(success=True).values('user__username')\
            .annotate(count=Count('*'), time=Max('last_try')).order_by('-count', 'time')[:10]

        # Generate a whitelist of tthe top 10 usernames
        top10names = [i['user__username'] for i in top10]

        # Format the output required from ChartJS in order to work
        final = []
        for username in allPlayers:
            if (username in top10names):
                final.append({
                    # Set dataset name to the username owner
                    "label": username,
                    "data": allPlayers[username]
                })
        return JsonResponse(
            {
                "title": "Top 10 players",
                "data": {
                    "datasets": final,
                }
            })
