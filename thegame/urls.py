"""thegame URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from thegame.views import FilesView, IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('user.urls')),
    path('challenge/', include('challenge.urls')),
    path('ranking/', include('ranking.urls')),
    path('files/<str:file>', FilesView.as_view(), name="protect_media"),
    path('', IndexView.as_view(), name="index"),
]
