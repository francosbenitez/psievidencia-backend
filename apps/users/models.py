from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager
from apps.psychologists.models import Psychologist


class User(AbstractUser):
    is_email_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        AUTHENTICATED = "AUTHENTICATED", "Authenticated"
        PSYCHOLOGIST = "PSYCHOLOGIST", "Psychologist"

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices, default="")

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class AuthenticatedManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.AUTHENTICATED)


class Authenticated(User):
    base_role = User.Role.AUTHENTICATED

    authenticated = AuthenticatedManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for authenticated users"


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

    def __str__(self):
        return self.psychologist
