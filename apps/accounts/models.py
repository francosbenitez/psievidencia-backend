from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        PATIENT = "PATIENT", "Patient"
        PSYCHOLOGIST = "PSYCHOLOGIST", "Psychologist"

    base_role = Role.PATIENT
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.PATIENT)

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=32, blank=True)
    lat = models.CharField(max_length=30, blank=True, null=True)
    lng = models.CharField(max_length=30, blank=True, null=True)
    avatar = models.ImageField(upload_to="media/avatars")

    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
