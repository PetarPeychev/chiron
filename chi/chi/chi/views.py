import random
from typing import Dict, Any
from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.shortcuts import render

from lyre import LichessClient

from .forms import RegistrationForm
from .models import *


def index(request):
    if request.user.is_authenticated:
        rating_history = LichessClient.get_user_rating_history("petarpeychev")
        user_data = LichessClient.get_user_data("petarpeychev")
        bullet_performance = LichessClient.get_performance_statistics("petarpeychev", "bullet")
        blitz_performance = LichessClient.get_performance_statistics("petarpeychev", "blitz")
        rapid_performance = LichessClient.get_performance_statistics("petarpeychev", "rapid")
        classical_performance = LichessClient.get_performance_statistics("petarpeychev", "classical")
        
        bullet_data = []
        bullet_labels = []
        blitz_data = []
        blitz_labels = []
        rapid_data = []
        rapid_labels = []
        classical_data = []
        classical_labels = []
        
        for game_type in rating_history:
            if game_type["name"] == "Bullet":
                for point in game_type["points"]:
                    bullet_labels.append(f"{str(point[2])}.{str(point[1] + 1)}.{str(point[0])}")
                    bullet_data.append(point[3])
            elif game_type["name"] == "Blitz":
                for point in game_type["points"]:
                    blitz_labels.append(f"{str(point[2])}.{str(point[1] + 1)}.{str(point[0])}")
                    blitz_data.append(point[3])
            elif game_type["name"] == "Rapid":
                for point in game_type["points"]:
                    rapid_labels.append(f"{str(point[2])}.{str(point[1] + 1)}.{str(point[0])}")
                    rapid_data.append(point[3])
            elif game_type["name"] == "Classical":
                for point in game_type["points"]:
                    classical_labels.append(f"{str(point[2])}.{str(point[1] + 1)}.{str(point[0])}")
                    classical_data.append(point[3])
        
        return render(request, "home.html", {
            "rating_history": {
                "bullet_data": bullet_data,
                "bullet_labels": bullet_labels,
                "blitz_data": blitz_data,
                "blitz_labels": blitz_labels,
                "rapid_data": rapid_data,
                "rapid_labels": rapid_labels,
                "classical_data": classical_data,
                "classical_labels": classical_labels
            },
            "user_data": user_data,
            "bullet_performance": bullet_performance,
            "blitz_performance": blitz_performance,
            "rapid_performance": rapid_performance,
            "classical_performance": classical_performance,
        })
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
