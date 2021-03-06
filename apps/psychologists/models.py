from django.db import models


class Psychologist(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField(auto_now=True)
    name = models.CharField(max_length=1000, default="")
    email = models.CharField(max_length=1000, default="")
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

    def __str__(self):
        return self.name


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
        Psychologist, related_name="gender_perspectives", on_delete=models.CASCADE
    )
    has_perspective = models.CharField(max_length=1000, default="")


class GenderIdentity(models.Model):
    psychologists = models.ForeignKey(
        Psychologist, related_name="gender_identities", on_delete=models.CASCADE
    )
    gender_identity = models.CharField(max_length=1000, default="")
