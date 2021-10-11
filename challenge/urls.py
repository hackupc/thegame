from django.urls import path

from challenge.views import HomeView, ChallengeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('challenge/<int:c_id>/', ChallengeView.as_view(), name='challenge'),
]
