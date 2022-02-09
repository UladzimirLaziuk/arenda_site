from django.contrib import admin
from django.urls import path
from site_app.models import Renter
from site_app import views

urlpatterns = [
    path('', views.RenterViewList.as_view()),
    path('create/', views.RenterViewCreate.as_view(), name='renter_create'),
]