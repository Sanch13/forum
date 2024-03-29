from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from vote import views

urlpatterns = [
    path('', views.index, name="index"),
    path('vote/', include("vote.urls", namespace="vote")),
    path('captcha/', include('captcha.urls')),
    # path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
