from rest_framework import serializers
from apps.patients.models import Patient
from apps.accounts.serializers import RegisterUserSerializer


class RegisterPatientSerializer(RegisterUserSerializer):
    class Meta(RegisterUserSerializer.Meta):
        model = Patient
        fields = RegisterUserSerializer.Meta.fields + ()

    def create(self, validated_data):
        return Patient.objects.create_user(**validated_data)


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ("id", "email", "role")
