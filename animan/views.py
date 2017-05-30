from django.shortcuts import render
from django.views.generic import ListView

from .models import Pet, Shelter

# Create your views here.


class ShowPetListView(ListView):
    model = Pet


class ShowShelterListView(ListView):
    model = Shelter
