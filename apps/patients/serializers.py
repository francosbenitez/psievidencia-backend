from rest_framework import serializers
from apps.patients.models import Patient
from apps.accounts.serializers import UserSerializer, RegisterUserSerializer


class PatientSerializer(UserSerializer):
    """Returned fields after registering"""

    class Meta(UserSerializer.Meta):
        model = Patient


class RegisterPatientSerializer(RegisterUserSerializer):
    """Required fields on registering"""

    class Meta(RegisterUserSerializer.Meta):
        model = Patient
        fields = RegisterUserSerializer.Meta.fields

    def create(self, validated_data):
        patient = Patient.objects.create_user(**validated_data)
        return patient
