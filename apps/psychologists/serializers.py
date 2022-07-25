from rest_framework import serializers
from .models import (
    Psychologist,
    Specialization,
    TherapeuticModel,
    WorkPopulation,
    Province,
    Liked,
)


class LikedSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation["liked"]

    class Meta:
        model = Liked
        fields = ("liked",)


class PsychologistSerializer(serializers.ModelSerializer):
    liked = LikedSerializer(source="*")

    class Meta:
        model = Psychologist
        fields = (
            "id",
            "date",
            "name",
            "email",
            "gender_identity",
            "registration_type",
            "registration_number",
            "institution",
            "team",
            "province",
            "city",
            "education",
            "therapeutic_model",
            "gender_perspective",
            "specialization",
            "work_population",
            "work_modality",
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


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ("id", "name")


class TherapeuticModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TherapeuticModel
        fields = ("id", "name")


class WorkPopulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkPopulation
        fields = ("id", "name")


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ("id", "name")
