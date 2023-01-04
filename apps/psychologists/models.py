from django.db import models
from apps.users.models import User


class Psychologist(User):
    base_role = User.Role.PSYCHOLOGIST
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=1000, default="")
    registration_type = models.CharField(max_length=1000, default="")
    registration_number = models.CharField(max_length=1000, default="")
    institution = models.CharField(max_length=1000, default="")
    team = models.CharField(max_length=1000, default="")
    city = models.CharField(max_length=1000, default="")
    online = models.CharField(max_length=1000, default="")
    prepaid_type = models.CharField(max_length=1000, default="")
    invoice = models.CharField(max_length=1000, default="")
    sign_language = models.CharField(max_length=1000, default="")
    session_languages = models.CharField(max_length=1000, default="")
    social_networks = models.CharField(max_length=1000, default="")
    phone_number = models.CharField(max_length=1000, default="")
    additional_data = models.CharField(max_length=1000, default="")
    name_2 = models.CharField(max_length=1000, default="")
    liked = models.BooleanField(default=False)


class Specialization(models.Model):
    name = models.CharField(max_length=1000, default="")
    psychologists = models.ManyToManyField(Psychologist, related_name="specializations")

    def __str__(self):
        return self.name


class TherapeuticModel(models.Model):
    name = models.CharField(max_length=1000, default="")
    psychologists = models.ManyToManyField(
        "Psychologist", related_name="therapeutic_models"
    )

    def __str__(self):
        return self.name


class WorkPopulation(models.Model):
    name = models.CharField(max_length=1000, default="")
    psychologists = models.ManyToManyField(
        Psychologist, related_name="work_populations"
    )

    def __str__(self):
        return self.name


class WorkModality(models.Model):
    name = models.CharField(max_length=1000, default="")
    psychologists = models.ManyToManyField(Psychologist, related_name="work_modalities")

    def __str__(self):
        return self.name


class Province(models.Model):
    psychologists = models.ForeignKey(
        Psychologist, related_name="province", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=1000, default="")
    slug = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.name


class Education(models.Model):
    psychologists = models.ForeignKey(
        Psychologist, related_name="education", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.name


class GenderPerspective(models.Model):
    psychologists = models.ForeignKey(
        Psychologist,
        related_name="gender_perspective",
        on_delete=models.CASCADE,
    )
    has_perspective = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.has_perspective


class Prepaid(models.Model):
    psychologists = models.ForeignKey(
        Psychologist, related_name="prepaid", on_delete=models.CASCADE
    )
    has_prepaid = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.has_prepaid


class GenderIdentity(models.Model):
    psychologists = models.ForeignKey(
        Psychologist, related_name="gender_identity", on_delete=models.CASCADE
    )
    gender_identity = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.gender_identity
