from django.contrib.auth import authenticate
from django.contrib.auth import login as dj_login
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            temp_user = User.objects.get(email=email)
            user = authenticate(username=temp_user.username, password=password)
            if user is not None:
                dj_login(request, user)
                return HttpResponse(content='great success')
        except ObjectDoesNotExist:
            pass
        return HttpResponse(content='nope')
    else:
        return render(request, 'accounts/login.html')
