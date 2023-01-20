from django.db import models
import apps.psychologists.constants as constants
from apps.accounts.models import User


class Institution(models.Model):
    name = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255, blank=True)


class RegularHealth(models.Model):
    name = models.CharField(max_length=255, blank=True)


class PrepaidHealth(models.Model):
    name = models.CharField(max_length=255, blank=True)


class Language(models.Model):
    name = models.CharField(
        max_length=10,
        choices=constants.LANGUAGES,
        null=True,
    )


class Specialization(models.Model):
    name = models.CharField(max_length=255, null=True)


class TherapeuticModel(models.Model):
    name = models.CharField(max_length=255, null=True)


class WorkPopulation(models.Model):
    name = models.CharField(max_length=255, null=True)


class WorkModality(models.Model):
    name = models.CharField(max_length=255, null=True)


class Psychologist(User):
    description = models.TextField(max_length=255)
    gender_identity = models.CharField(
        max_length=10, choices=constants.GENDER_IDENTITIES, null=False, blank=False
    )
    education = models.CharField(
        choices=constants.EDUCATIONS, max_length=255, null=False, blank=False
    )
    instagram_profile = models.CharField(max_length=255, blank=True, null=True)
    linkedin_profile = models.CharField(max_length=255, blank=True, null=True)
    registration_name = models.CharField(
        choices=constants.REGISTRATION_NAMES, max_length=255, blank=False, null=False
    )
    registration_number = models.PositiveIntegerField(null=False)
    has_gender_perspective = models.BooleanField(default=False)
    has_work_team = models.BooleanField(default=False)
    offers_invoice = models.BooleanField(default=False)
    offers_online = models.BooleanField(default=False)
    offers_first_session_free = models.BooleanField(default=False)
    knows_sign_language = models.BooleanField(default=False)
    price_hour = models.DecimalField(decimal_places=2, max_digits=20, null=True)

    rating_average = models.FloatField(default=0)
    review_count = models.IntegerField(default=0)

    institution = models.ManyToManyField(Institution)
    regular_health = models.ManyToManyField(RegularHealth)
    prepaid_health = models.ManyToManyField(RegularHealth)
    language = models.ManyToManyField(Language)
    specialization = models.ManyToManyField(Specialization)
    therapeutic_model = models.ManyToManyField(TherapeuticModel)
    work_population = models.ManyToManyField(WorkPopulation)
    work_modality = models.ManyToManyField(WorkModality)

    was_liked = models.BooleanField(default=False)
