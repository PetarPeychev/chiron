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
        lichess_username = LichessAccount.objects.filter(user=request.user).first().username
        rating_history = LichessClient.get_user_rating_history(lichess_username)
        user_data = LichessClient.get_user_data(lichess_username)
        bullet_performance = LichessClient.get_performance_statistics(lichess_username, "bullet")
        blitz_performance = LichessClient.get_performance_statistics(lichess_username, "blitz")
        rapid_performance = LichessClient.get_performance_statistics(lichess_username, "rapid")
        classical_performance = LichessClient.get_performance_statistics(lichess_username, "classical")
        
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
        
        bullet_data = [
            bullet_data[index] 
            for index 
            in range(0, len(bullet_data), int(max(1, len(bullet_data) / 100)))
        ]
        bullet_labels = [
            bullet_labels[index] 
            for index 
            in range(0, len(bullet_labels), int(max(1, len(bullet_labels) / 100)))
        ]
        
        blitz_data = [
            blitz_data[index] 
            for index 
            in range(0, len(blitz_data), int(max(1, len(blitz_data) / 100)))
        ]
        blitz_labels = [
            blitz_labels[index] 
            for index 
            in range(0, len(blitz_labels), int(max(1, len(blitz_labels) / 100)))
        ]
        
        rapid_data = [
            rapid_data[index] 
            for index 
            in range(0, len(rapid_data), int(max(1, len(rapid_data) / 100)))
        ]
        rapid_labels = [
            rapid_labels[index] 
            for index 
            in range(0, len(rapid_labels), int(max(1, len(rapid_labels) / 100)))
        ]
        
        classical_data = [
            classical_data[index] 
            for index 
            in range(0, len(classical_data), int(max(1, len(classical_data) / 100)))
        ]
        classical_labels = [
            classical_labels[index] 
            for index 
            in range(0, len(classical_labels), int(max(1, len(classical_labels) / 100)))
        ]
        
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

def openings(request):
    return render(request, "openings.html")

def blunders(request):
    return render(request, "blunders.html")

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
