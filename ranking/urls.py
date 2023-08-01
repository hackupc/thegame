from django.urls import path

from ranking.views import RankingView, get_chart

urlpatterns = [
    path('', RankingView.as_view(), name='ranking'),
    path('chart', get_chart, name="chart")
]
