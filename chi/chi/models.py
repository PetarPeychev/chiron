from __future__ import annotations

from django.contrib.auth.models import User
from django.db import models

class LichessAccount(models.Model):
    id = models.AutoField(primary_key=True)
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    username: str = models.CharField(max_length=20, null=False, blank=False)