from django.shortcuts import render, redirect

from django.http import HttpResponse
from .models import Tutorial
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm

# Create your views here.
def homepage(request):
    return render(request=request,
                  template_name="main/home.html",
                  context={"tutorials": Tutorial.objects.all})

# A view for register requests
def register(request):
    #This is for when a POST request will be made
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created: {username}")

            login(request, user)
            messages.info(request, f"You are now logged in as: {username}")
            return redirect("main:homepage")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: form.error_messages[msg]")

    #This is for default GET requests
    form = NewUserForm
    return render(request=request,
                  template_name="main/register.html",
                  context={"form": form})

# A view for login requests
def login_request(request):
    #This is for when a POST request will be made
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as: {username}")
                return redirect("main:homepage")
            else:
                messages.error(request, "Invalid unername or password")
        else:
            messages.error(request, "Invalid unername or password")

    #This is for default GET requests
    form = AuthenticationForm
    return render(request=request,
                  template_name="main/login.html",
                  context={"form": form})

# A view for logout requests
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")
