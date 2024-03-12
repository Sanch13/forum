from django.contrib import admin
from django.urls import path, include

from vote import views

urlpatterns = [
    path('', views.index, name="index"),
    path('vote/', include("vote.urls", namespace="vote")),
    path('admin/', admin.site.urls),
]
