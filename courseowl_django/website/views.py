from django.shortcuts import render


def index(request):
    return render(request, 'website/index.html')


def personalize(request):
    return render(request, 'website/personalize.html')
