from rest_framework import serializers
from apps.patients.models import Patient
from apps.accounts.serializers import RegisterUserSerializer


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ("id", "email", "role")


class RegisterPatientSerializer(RegisterUserSerializer):
    class Meta(RegisterUserSerializer.Meta):
        model = Patient
        fields = RegisterUserSerializer.Meta.fields

    def create(self, validated_data):
        return super().create(validated_data)
