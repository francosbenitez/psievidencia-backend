from django.db import models
from apps.users.models import Authenticated
from apps.psychologists.models import Psychologist


class Favorite(models.Model):

    authenticated = models.ForeignKey(
        Authenticated, related_name="favorites", on_delete=models.CASCADE
    )
    psychologist = models.ForeignKey(
        Psychologist, related_name="favorites", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.psychologist
