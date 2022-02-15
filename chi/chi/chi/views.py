import random

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import RegistrationForm
from .models import *


def index(request):
    if request.user.is_authenticated:
        return render(request, "home.html")
    else:
        return render(request, "index.html")
    
def register(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegistrationForm()

    return render(request, "registration/register.html", {"form": form})
