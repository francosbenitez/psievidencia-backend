from rest_framework import serializers
from apps.accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for users data"""

    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "role",
            "first_name",
            "last_name",
            "full_name",
            "phone_number",
            "lat",
            "lng",
            "avatar",
        )

    def get_full_name(self, obj):
        full_name = obj.first_name + " " + obj.last_name

        if full_name == "":
            full_name = obj.email

        return full_name


class RegisterUserSerializer(serializers.ModelSerializer):
    """Required fields on registering"""

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "role",
            "first_name",
            "last_name",
            "phone_number",
            "lat",
            "lng",
            "avatar",
        )

    def validate_password(self, password):
        password_minimum_length = 8

        if len(password) < password_minimum_length:
            raise serializers.ValidationError(
                f"Password minimum length allowed is {password_minimum_length}"
            )

        return password
