from django.urls import path

from ranking.views import RankingView, ChartView
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', RankingView.as_view(), name='ranking'),
    path('chart',  cache_page(60)(ChartView.as_view()), name="chart")
]
