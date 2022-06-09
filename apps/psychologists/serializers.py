from rest_framework import serializers
from .models import Psychologist, Specialization


class PsychologistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Psychologist
        fields = (
            "id",
            "date",
            "name",
            "email",
            "gender",
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
        )


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ("id", "specialization", "psychologist_id")
