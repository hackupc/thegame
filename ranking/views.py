from typing import List, Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Max
from django_tables2 import SingleTableView
from datetime import datetime


from challenge.models import ChallengeUser
from ranking.tables import RankingTable
from challenge.models import ChallengeUser
def getPlayerName(userid:int):
    return userid #TODO DB name lookup

def getHistoricData(userid: int):
    # get historical data ordered from older to newer.
    historic = ChallengeUser.objects.filter(success=True, user_id=userid).order_by('-attempt_date').values()
    # iterate points
    accumulatedPoints = 0
    # CHANGE THIS TO TIMESTAMP WHERE THEGAME IS GOING TO START
    startingTheGameTimeStamp = "1659000000"
    toReturn = startingTheGameTimeStamp+",0|"
    for correctsolution in historic:
        accumulatedPoints+=1
        timestamp = int(datetime.fromisoformat(str(correctsolution.get('attempt_date'))).timestamp()) # get & remove timestamp decimals
        toReturn += str(timestamp)+","+str(accumulatedPoints)+"|"
    return toReturn[:len(toReturn)-1]


class RankingView(LoginRequiredMixin, SingleTableView):
    table_class = RankingTable
    template_name = 'ranking.html'

    def GetChartData(self):
        # future db select top 10

        correctSolutions = ChallengeUser.objects.filter(success=True).values()
        allRankingPlayers={}
        for correctSol in correctSolutions:
            if not correctSol.get('user_id') in allRankingPlayers :
                allRankingPlayers[correctSol.get('user_id')] = {
                    'user_id': correctSol.get('user_id'),
                    'points': 0
                }

            allRankingPlayers[correctSol.get('user_id')]['points'] += 1

        toReturn = {}
        i = 1
        for uid, _ in allRankingPlayers.items():
            if(i>10): break
            toReturn[i] = {
                "name": getPlayerName(uid),
                "points": getHistoricData(uid),
            }
            i += 1

        print(toReturn)
        return toReturn
#
   # "0":{
   #     "name" : "user1",
   #     "points":"1658151927,0|1658152927,43.25|1658152927,43.25|1658152927,443.25"
   # }, "2":{
   #     "name" : "user2",
   #     "points":"1658151927,0|2658152927,12.25|2658152927,12.25|2658152927,142.25"
   # }, "3":{
   #     "name" : "user3",
   #     "points":"1658151927,0|3658152927,34.25|3658152927,34.25|3658152927,134.25"
   # }, "4":{
   #     "name" : "user4",
   #     "points":"1658151927,0|4658152927,42.25|4658152927,42.25|4658152927,142.25"
   # },
   #     "5":{
   #     "name" : "user5",
   #     "points":"1658151927,0|5658152927,42.25|5658152927,42.25|5658152927,142.25"
   # },
   #     "6":{
   #     "name" : "user6",
   #     "points":"1658151927,0|6658152927,42.25|6658152927,42.25|6658152927,412.25"
   # },
   #     "7":{
   #     "name" : "user7",
   #     "points":"1658151927,0|7658152927,42.25|7658152927,42.25|7658152927,142.25"
   # },
   #     "8":{
   #     "name" : "user8",
   #     "points":"1658151927,0|8658152927,42.25|8658152927,42.25|8658152927,142.25"
   # },
   #     "9":{
   #     "name" : "user9",
   #     "points":"1658151927,0|9658152927,42.25|9658152927,42.25|9658152927,42.25"
   # },
   #
   # }"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'ChartData': self.GetChartData()})
        return context

    def get_queryset(self):
        return ChallengeUser.objects.filter(success=True).values('user__username') \
            .annotate(count=Count('*'), time=Max('last_try')).order_by('-count', 'time')
