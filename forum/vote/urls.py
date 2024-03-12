from django.urls import path

from .views import *

app_name = "vote"

urlpatterns = [
    path('', home, name="home"),
    path('registration_project/', registration_project, name="registration_project"),
]
