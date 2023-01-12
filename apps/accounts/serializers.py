from rest_framework import serializers
from apps.accounts.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    """Required fields on registering"""

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "lat",
            "lng",
            "avatar",
        )
