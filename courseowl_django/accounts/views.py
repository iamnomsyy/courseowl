import md5
from django.contrib.auth import authenticate
from django.contrib.auth import login as dj_login, logout as dj_logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from models import UserProfile


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


def logout(request):
    dj_logout(request)
    return HttpResponse(content='logged out successfully')


def email_signup(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            return render(request, 'accounts/signup.html')

        user = User.objects.create_user(username_md5(email), email, password="1234", first_name="", last_name="")
        userprofile = UserProfile()
        userprofile.user = user
        user.save()
        userprofile.save()
        return HttpResponse(content='Hi ' + user.email)
    else:
        return render(request, 'accounts/signup.html')


def username_md5(email):
    return md5.new(email.lower()).hexdigest()[:30]
