from django.db import models
from django.contrib.auth.models import User
from apps.psychologists.models import Psychologist


class Suggestion(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000, default="")
    description = models.CharField(max_length=1000, default="")
    users = models.ManyToManyField(User, related_name="suggestions")

    def __str__(self):
        return self.name


class Favorite(models.Model):

    user = models.ForeignKey(User, related_name="favorites", on_delete=models.CASCADE)
    psychologist = models.ForeignKey(
        Psychologist, related_name="favorites", on_delete=models.CASCADE
    )
