from django.contrib import admin
from django.urls import path
from site_app.models import Renter
from site_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.RenterViewList.as_view()),
    path('create/', views.RenterViewCreate.as_view(), name='renter_create'),
]

if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
