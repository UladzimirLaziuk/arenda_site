from django.shortcuts import render
from django.views.generic import ListView, CreateView
from site_app import models


# Create your views here.

class RenterViewList(ListView):
    model = models.Renter
    template_name = 'main/list_renter.html'


class RenterViewCreate(CreateView):
    model = models.Renter
    template_name = 'main/create_renter.html'
    fields = '__all__'
