from django.shortcuts import render
from django.views.generic import ListView
from .models import Binder

# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>PokeTracker Home</h1>')

class BinderList(ListView):
    model = Binder