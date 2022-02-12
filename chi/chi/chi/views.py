import random

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import *
from .models import *


def index(request):
    if request.user.is_authenticated:
        return render(request, "home.html")
    else:
        return render(request, "index.html")