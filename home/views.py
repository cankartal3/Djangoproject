from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from home.models import Settings


def index(request):
    settings = Settings.objects.get(pk=1)
    context = {'settings': settings, 'page':'home'}
    return render(request, 'index.html', context)

def hakkimizda(request):
    settings = Settings.objects.get(pk=1)
    context = {'settings': settings, 'page':'hakkimizda'}
    return render(request, 'hakkimizda.html', context)

def referanslarimiz(request):
    settings = Settings.objects.get(pk=1)
    context = {'settings': settings, 'page':'referanslarimiz'}
    return render(request, 'referanslarimiz.html', context)

def iletisim(request):
    settings = Settings.objects.get(pk=1)
    context = {'settings': settings, 'page':'iletisim'}
    return render(request, 'iletisim.html', context)