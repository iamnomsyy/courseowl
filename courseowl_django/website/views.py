from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'website/index.html')


@login_required
def personalize(request):
    context = {}
    return render(request, 'website/personalize.html', context)
