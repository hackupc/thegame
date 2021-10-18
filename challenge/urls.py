from django.urls import path

from challenge.views import HomeView, ChallengeView, ChallengeStatsView

urlpatterns = [
    path('', HomeView.as_view(), name='challenge-index'),
    path('<int:c_id>/', ChallengeView.as_view(), name='challenge'),
    path('<int:c_id>/stats/', ChallengeStatsView.as_view(), name='challenge-stats'),
]
