from django.shortcuts import render, HttpResponse
# from django account.models import Account
from django.contrib.auth import login, logout, authenticate
from account.forms import SignupForm
# Create your views here.

def signup(request):
    context = {}
    if request.method == 'POST':
        form = SignupForm( request.POST )
        if form.is_valid():
            user = form.save()
            user.save()
            return HttpResponse("OK")
    else:
        form = SignupForm()
    context = {
        'form': form
    }
    return render( request, 'user/auth/signup.html', context )            

            

