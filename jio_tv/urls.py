"""jio_tv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from .views import auto_m3u_gen, live, stream, play, home

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",home),
    path("play/",play),
    path('auto/', auto_m3u_gen, name='auto'),
    path("live/", live, name="live"),
    path("stream/", stream, name="stream")
]
