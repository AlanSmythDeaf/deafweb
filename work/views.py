from django.shortcuts import render
from .models import Website


def work(request):
    websites = Website.objects.all()
    return render(request, 'work/work.html', {'websites': websites})
