from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render


def do_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            temp_user = User.objects.get(email=email)
            user = authenticate(username=temp_user.username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse(content='great success')
        except ObjectDoesNotExist:
            pass
        return HttpResponse(content='nope')
    else:
        return render(request, 'user_management/login.html')
