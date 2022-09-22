from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    is_email_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        AUTHENTICATED = "AUTHENTICATED", "Authenticated"
        PSYCHOLOGIST = "PSYCHOLOGIST", "Psychologist"

    base_role = Role.AUTHENTICATED

    role = models.CharField(max_length=50, choices=Role.choices, default="")

    # def save(self, *args, **kwargs):
    # if not self.pk:
    #     self.role = self.base_role
    #     return super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class Authenticated(User):
    base_role = User.Role.AUTHENTICATED
