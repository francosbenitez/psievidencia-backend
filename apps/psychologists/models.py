from django.db import models
from apps.users.models import Psychologist


class Specialization(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1000, default="")
    psychologists = models.ManyToManyField(Psychologist, related_name="specializations")

    def __str__(self):
        return self.name


class TherapeuticModel(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1000, default="")
    psychologists = models.ManyToManyField(
        Psychologist, related_name="therapeutic_models"
    )

    def __str__(self):
        return self.name


class WorkPopulation(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1000, default="")
    psychologists = models.ManyToManyField(
        Psychologist, related_name="work_populations"
    )

    def __str__(self):
        return self.name


class WorkModality(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1000, default="")
    psychologists = models.ManyToManyField(Psychologist, related_name="work_modalities")

    def __str__(self):
        return self.name


class Province(models.Model):
    psychologists = models.ForeignKey(
        Psychologist, related_name="provinces", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=1000, default="")
    slug = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.name


class Education(models.Model):
    psychologists = models.ForeignKey(
        Psychologist, related_name="educations", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.name


class GenderPerspective(models.Model):
    psychologists = models.ForeignKey(
        Psychologist,
        related_name="gender_perspectives",
        on_delete=models.CASCADE,
    )
    has_perspective = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.has_perspective


class Prepaid(models.Model):
    psychologists = models.ForeignKey(
        Psychologist, related_name="prepaids", on_delete=models.CASCADE
    )
    has_prepaid = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.has_prepaid


class GenderIdentity(models.Model):
    psychologists = models.ForeignKey(
        Psychologist, related_name="gender_identities", on_delete=models.CASCADE
    )
    gender_identity = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.gender_identity
