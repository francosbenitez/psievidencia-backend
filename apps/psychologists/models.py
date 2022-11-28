from django.db import models
import apps.psychologists.constants as constants
from apps.accounts.models import User


class SocialNetwork(models.Model):
    facebook = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    whatsapp = models.CharField(max_length=255, blank=True, null=True)


class Prepaid(models.Model):
    """
    Represents if the psychologist works affiliated to a prepaid and/or social work.
    """

    has = models.BooleanField(default=False)
    name = models.CharField(max_length=255, blank=True)


class Institution(models.Model):
    has = models.BooleanField(default=False)
    name = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255, blank=True)


class Registration(models.Model):
    name = models.CharField(
        choices=constants.REGISTRATION_NAMES, max_length=255, default=constants.P
    )
    number = models.IntegerField()


class Psychologist(User):
    description = models.TextField(max_length=255)
    gender_identity = models.CharField(
        max_length=10,
        choices=constants.GENDER_IDENTITIES,
        default=constants.WOMAN,
    )
    education = models.CharField(
        choices=constants.EDUCATIONS, max_length=255, default=constants.LICENSURE
    )
    social_networks = models.ForeignKey(
        SocialNetwork, on_delete=models.CASCADE, null=True
    )
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True)
    prepaid = models.ForeignKey(Prepaid, on_delete=models.CASCADE, null=True)
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True)
    has_perspective = models.BooleanField(default=False)
    has_team = models.BooleanField(default=False)
    offers_invoice = models.BooleanField(default=False)
    offers_online = models.BooleanField(default=False)
    knows_sign_language = models.BooleanField(default=False)
    price_hour = models.DecimalField(
        decimal_places=2, max_digits=20, blank=True, null=True
    )
    liked = models.BooleanField(default=False)


class Language(models.Model):
    name = models.CharField(max_length=255, null=True)
    psychologists = models.ManyToManyField(Psychologist)


class Specialization(models.Model):
    name = models.CharField(max_length=255, null=True)
    psychologists = models.ManyToManyField(Psychologist)


class TherapeuticModel(models.Model):
    name = models.CharField(max_length=255, null=True)
    psychologists = models.ManyToManyField(Psychologist)


class WorkPopulation(models.Model):
    name = models.CharField(max_length=255, null=True)
    psychologists = models.ManyToManyField(Psychologist, blank=True)


class WorkModality(models.Model):
    name = models.CharField(max_length=255, null=True)
    psychologists = models.ManyToManyField(Psychologist)
