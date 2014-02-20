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
    # Create a state token to prevent request forgery.
    # Store it in the session for later validation.
    #     state = ''.join(random.choice(string.ascii_uppercase + string.digits)
    #                     for x in xrange(32))
    #     session['state'] = state
    #     # Set the Client ID, Token State, and Application Name in the HTML while
    #     # serving it.
    #     response = make_response(
    #         render_template('index.html',
    #                         CLIENT_ID=CLIENT_ID,
    #                         STATE=state,
    #                         APPLICATION_NAME=APPLICATION_NAME))
        return render(request, 'accounts/login.html')

#
# def google_login(request):
#     if request.method == 'POST':


#
# def facebook_login(request):
#     if request.method == 'POST':
