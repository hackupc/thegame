from django.urls import path

from ranking.views import RankingView, ChartView

urlpatterns = [
    path('', RankingView.as_view(), name='ranking'),
    path('chart',  ChartView.as_view(), name="chart")
]
