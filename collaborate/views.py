from django.shortcuts import render

# Create your views here.

def collaborate(request):
    return render(request, 'collaborate/collaborate.html')