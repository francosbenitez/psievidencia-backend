from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import apps.accounts.constants as constants


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        if password is None:
            raise TypeError("Superusers must have a password")

        user = self.model(email=email)
        user.is_admin = True
        user.is_staff = True
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    username = None
    email = models.EmailField(
        unique=True, error_messages={"unique": "Este email ya está registrado."}
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    role = models.CharField(max_length=12, choices=constants.ROLE_CHOICES)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20, blank=True)
    lat = models.CharField(max_length=30, blank=True)
    lng = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to="avatars", blank=True)
    is_email_verified = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now_add=True)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
