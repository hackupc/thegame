from django.urls import path

from ranking.views import RankingView

urlpatterns = [
    path('', RankingView.as_view(), name='ranking'),
]
