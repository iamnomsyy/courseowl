import hashlib
from django.contrib.auth import authenticate
from django.contrib.auth import login as dj_login, logout as dj_logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from models import UserProfile
from django.forms import EmailField
from django.core.exceptions import ValidationError


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            temp_user = User.objects.get(email=email)
            user = authenticate(username=temp_user.username, password=password)
            if user is not None:
                dj_login(request, user)
                return redirect('/accounts/profile')
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

        if not unique_user(email):
            return HttpResponse(content='USER ALREADY EXISTS')

        if not valid_email_address(email):
            return HttpResponse(content='Invalid email address')

        valid_pw = check_valid_password(password, password_confirm)
        if not valid_pw:
            return HttpResponse(content='Invalid password input. Passwords must match and be >8 characters')

        user = User.objects.create_user(username_md5(email), email, password, first_name="", last_name="")
        userprofile = UserProfile()
        userprofile.user = user
        user.save()
        userprofile.save()
        return redirect('/personalize')
    else:
        return render(request, 'accounts/signup.html')


def check_valid_password(pw, pw_conf):
    if len(pw) < 8 or pw != pw_conf:
        return False
    return True


def unique_user(email):
    hashedemail = username_md5(email)
    if User.objects.filter(username=hashedemail).exists():
        return False
    else:
        return True


def username_md5(email):
    return hashlib.md5(email.lower()).hexdigest()[:30]


def valid_email_address(email):
    try:
        EmailField().clean(email)
        return True
    except ValidationError:
        return False
