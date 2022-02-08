import random

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import *
from .models import *


@login_required(login_url="/login")
def index(request):
    return render(request, "index.html")
