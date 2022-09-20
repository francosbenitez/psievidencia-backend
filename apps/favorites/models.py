from django.db import models
from apps.users.models import Authenticated, Psychologist


class Favorite(models.Model):

    authenticated = models.ForeignKey(
        Authenticated, related_name="authenticad", on_delete=models.CASCADE
    )
    psychologist = models.ForeignKey(
        Psychologist, related_name="psychologist", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.psychologist
