from django.db import models
from django.contrib.auth.models import User


class Suggestion(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000, default="")
    description = models.CharField(max_length=1000, default="")
    users = models.ManyToManyField(User, related_name="suggestions")

    def __str__(self):
        return self.name
