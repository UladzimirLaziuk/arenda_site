from django.shortcuts import render
from django.views.generic import ListView
from site_app import models


# Create your views here.

class RenterViewList(ListView):
    model = models.Renter
    template_name = 'main/list_renter.html'
