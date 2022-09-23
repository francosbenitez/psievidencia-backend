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
    def to_representation(self, value):
        return value.name

    class Meta:
        model = TherapeuticModel
        fields = ("id", "name")


class SpecializationSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        return value.name

    class Meta:
        model = Specialization
        fields = ("id", "name")


class WorkModalitySerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        return value.name

    class Meta:
        model = WorkModality
        fields = ("id", "name")


class WorkPopulationSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        return value.name
        
    class Meta:
        model = WorkPopulation
        fields = ("id", "name")


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ("id", "name", "slug")

class PsychologistsSerializer(serializers.ModelSerializer):
    therapeutic_models = TherapeuticModelSerializer(many=True)
    specializations = SpecializationSerializer(many=True)
    work_populations = WorkPopulationSerializer(many=True)
    work_modalities = WorkModalitySerializer(many=True)
    # liked = serializers.SerializerMethodField()

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
            "specializations",
            "work_populations",
            "work_modalities",
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

    # def get_liked(self, obj):
    #     liked = self.context['liked']
    #     return liked

class PsychologistSerializer(serializers.ModelSerializer):
    therapeutic_models = TherapeuticModelSerializer(many=True)
    specializations = SpecializationSerializer(many=True)
    work_populations = WorkPopulationSerializer(many=True)
    work_modalities = WorkModalitySerializer(many=True)
    liked = serializers.SerializerMethodField()

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
            "specializations",
            "work_populations",
            "work_modalities",
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

    def get_liked(self, obj):
        liked = self.context['liked']
        return liked

    # def __init__(self, *args, **kwargs):
    #     print("kwargs['context']", kwargs['context'])
    #     if kwargs['context']['view'].action == 'get':
    #         del self.fields['liked']
    #     super().__init__(*args, **kwargs)