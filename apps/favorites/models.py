from django.db import models
from apps.users.models import User
from apps.psychologists.models import Psychologist


class Favorite(models.Model):

    user = models.ForeignKey(
        User, related_name="favorites_user", on_delete=models.CASCADE, default=""
    )
    psychologist = models.ForeignKey(
        Psychologist, related_name="favorites_psychologist", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.psychologist
