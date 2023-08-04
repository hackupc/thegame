from django.urls import path

from ranking.views import RankingView, ChartView

urlpatterns = [
    path('', RankingView.as_view(), name='ranking'),
    path('chart', ChartView.get_chart, name="chart")
]
