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


class Psychologist(User):
    base_role = User.Role.PSYCHOLOGIST

    # id = models.IntegerField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=1000, default="")
    # email = models.EmailField(unique=True)
    gender_identity = models.CharField(max_length=1000, default="")
    registration_type = models.CharField(max_length=1000, default="")
    registration_number = models.CharField(max_length=1000, default="")
    institution = models.CharField(max_length=1000, default="")
    team = models.CharField(max_length=1000, default="")
    province = models.CharField(max_length=1000, default="")
    city = models.CharField(max_length=1000, default="")
    education = models.CharField(max_length=1000, default="")
    therapeutic_model = models.CharField(max_length=1000, default="")
    gender_perspective = models.CharField(max_length=1000, default="")
    specialization = models.CharField(max_length=1000, default="")
    work_population = models.CharField(max_length=1000, default="")
    work_modality = models.CharField(max_length=1000, default="")
    online = models.CharField(max_length=1000, default="")
    prepaid = models.CharField(max_length=1000, default="")
    prepaid_type = models.CharField(max_length=1000, default="")
    invoice = models.CharField(max_length=1000, default="")
    sign_language = models.CharField(max_length=1000, default="")
    session_languages = models.CharField(max_length=1000, default="")
    social_networks = models.CharField(max_length=1000, default="")
    phone_number = models.CharField(max_length=1000, default="")
    additional_data = models.CharField(max_length=1000, default="")
    name_2 = models.CharField(max_length=1000, default="")
    liked = models.BooleanField(default=False)
