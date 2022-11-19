from .models import Patient
from rest_framework import serializers


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = (
            "id",
            "date",
            "name",
            "email",
            "username",
            "gender_identity",
            "phone_number",
            "additional_data",
        )
