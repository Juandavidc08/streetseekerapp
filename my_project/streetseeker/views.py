from django.shortcuts import render, HttpResponse
from django.shortcuts import render
from django.db.models import Count
from .models import Place
import random

# Create your views here.

def home(request):
    return render(request, "home.html")


def search(request):
    # Get all places from the database
    all_places = Place.objects.all()

    # Sample three random places if there are at least three places in the database
    if len(all_places) >= 3:
        random_places = sample(list(all_places), 3)
    else:
        random_places = all_places

    return render(request, 'search.html', {'random_places': random_places})
