from django.urls import path

from user import views

urlpatterns = [
    path('username/', views.ChooseUsername.as_view(), name='set_username'),
]
