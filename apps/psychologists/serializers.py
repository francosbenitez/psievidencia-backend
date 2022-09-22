from rest_framework import serializers
from .models import (
    Psychologist,
    Specialization,
    TherapeuticModel,
    WorkPopulation,
    WorkModality,
    Province,
)


class TherapeuticModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TherapeuticModel
        fields = ("id", "name")


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ("id", "name")


class WorkModalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkModality
        fields = ("id", "name")


class WorkPopulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkPopulation
        fields = ("id", "name")


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ("id", "name", "slug")


class PsychologistSerializer(serializers.ModelSerializer):
    therapeutic_models = TherapeuticModelSerializer(many=True)
    # specialization = SpecializationSerializer(many=True)
    # work_population = WorkPopulationSerializer(many=True)
    # work_modality = WorkModalitySerializer(many=True)

    class Meta:
        model = Psychologist
        fields = (
            "id",
            "date",
            "name",
            "gender_identity",
            "registration_type",
            "registration_number",
            "institution",
            "team",
            "province",
            "city",
            "education",
            "therapeutic_models",
            "gender_perspective",
            # "specialization",
            # "work_population",
            # "work_modality",
            "online",
            "prepaid",
            "prepaid_type",
            "invoice",
            "sign_language",
            "session_languages",
            "social_networks",
            "phone_number",
            "additional_data",
            "name_2",
            "liked",
        )

