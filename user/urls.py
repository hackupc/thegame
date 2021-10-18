import django_cas_ng.views
from django.urls import path

from user import views

urlpatterns = [
    path('login/', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    path('logout/', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
    path('username/', views.ChooseUsername.as_view(), name='set_username'),
]
