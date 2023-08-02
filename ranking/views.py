from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Max
from django_tables2 import SingleTableView
from django.http import JsonResponse

from challenge.models import ChallengeUser
from ranking.tables import RankingTable
from datetime import datetime


class RankingView(LoginRequiredMixin, SingleTableView):
    table_class = RankingTable
    template_name = 'ranking.html'

    def get_queryset(self):
        return ChallengeUser.objects.filter(success=True).values('user__username')\
            .annotate(count=Count('*'), time=Max('last_try')).order_by('-count', 'time')
    
def get_chart(request):
    # Get all Successful attempts
    # TODO: limit to 10 players
    allEntries = list(ChallengeUser.objects.filter(success=True).values('user__username', 'last_try', 'total_attempts').order_by('last_try'))

    players = {}
    Pcounter = {}
    # Classify them by player, in chronological order.
    for successes in allEntries:
        Pcounter[successes['user__username']] = Pcounter.get(successes['user__username'],0)+1
        playerDb =  players.get(successes['user__username'],[])
        playerDb.append({"x": successes['last_try'],"y": Pcounter[successes['user__username']]})
        players[successes['user__username']] = playerDb
    
    # Format the output required from ChartJS in order to work 
    final = []
    for username in players:
        final.append({
            # Set dataset name to the username owner
            "label" : username,
            "data": players[username]
        })
    return JsonResponse(
        {
            "title": f"Top 10 players",
            "data":  {
                "datasets": final
                
            }
        })
