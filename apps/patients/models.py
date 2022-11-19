from django.db import models
from apps.users.models import User
from django.utils.timezone import now


class Patient(User):
    base_role = User.Role.PATIENT
    date = models.DateTimeField(default=now, editable=False)
    name = models.CharField(max_length=1000, default="")
    gender_identity = models.CharField(max_length=1000, default="")
    phone_number = models.CharField(max_length=1000, default="")
    additional_data = models.CharField(max_length=1000, default="")
