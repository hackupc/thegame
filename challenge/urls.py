from django.urls import path

from challenge.views import HomeView, ChallengeView, ChallengeStatsView, ChallengeStatsAttemptView, VoteChallengeView, \
    VoteChallengeReactionView, FileModelView

urlpatterns = [
    path('', HomeView.as_view(), name='challenge-index'),
    path('<int:c_id>/', ChallengeView.as_view(), name='challenge'),
    path('<int:c_id>/vote/', VoteChallengeView.as_view(), name='challenge-vote'),
    path('<int:c_id>/vote/reaction/<str:r_type>/', VoteChallengeReactionView.as_view(), name='challenge-reaction'),
    path('<int:c_id>/stats/', ChallengeStatsView.as_view(), name='challenge-stats'),
    path('<int:c_id>/stats/attempt/', ChallengeStatsAttemptView.as_view(), name='challenge-stats-attempt-all'),
    path('<int:c_id>/stats/attempt/<str:u_id>/', ChallengeStatsAttemptView.as_view(), name='challenge-stats-attempt'),
    path('file/<str:filename>/', FileModelView.as_view(), name='file'),
]
