from django.db import models


class Psychologist(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField(auto_now=True)
    name = models.CharField(max_length=1000, default="")
    email = models.CharField(max_length=1000, default="")
    gender = models.CharField(max_length=1000, default="")
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

    def __str__(self):
        return self.name


class Specialization(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1000, default="")
    psychologists = models.ManyToManyField(Psychologist, related_name="specializations")


class TherapeuticModel(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1000, default="")
    psychologists = models.ManyToManyField(
        Psychologist, related_name="therapeutic_models"
    )
