from django.db import models
import apps.psychologists.constants as constants
from apps.accounts.models import User


class BaseModel(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Institution(BaseModel):
    url = models.CharField(max_length=255, blank=True)


class RegularHealth(BaseModel):
    pass


class PrepaidHealth(BaseModel):
    pass


class SessionLanguage(BaseModel):
    name = models.CharField(
        max_length=10,
        choices=constants.LANGUAGES,
        null=True,
    )


class Specialization(BaseModel):
    pass


class TherapeuticModel(BaseModel):
    pass


class WorkPopulation(BaseModel):
    pass


class WorkModality(BaseModel):
    pass


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
    institution = models.ManyToManyField(Institution, null=True)
    regular_health = models.ManyToManyField(RegularHealth, null=True)
    prepaid_health = models.ManyToManyField(RegularHealth, null=True)
    session_language = models.ManyToManyField(SessionLanguage, null=False)
    specialization = models.ManyToManyField(Specialization, null=False)
    therapeutic_model = models.ManyToManyField(TherapeuticModel, null=False)
    work_population = models.ManyToManyField(WorkPopulation, null=False)
    work_modality = models.ManyToManyField(WorkModality, null=False)

    rating_average = models.FloatField(default=0)
    review_count = models.IntegerField(default=0)
    was_liked = models.BooleanField(default=False)
