from rest_framework import serializers
from apps.accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for users data"""

    name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        read_only_fields = ["name"]

    def get_name(self, obj):
        name = obj.first_name + " " + obj.last_name
        if name == "":
            name = obj.email
        return name


class RegisterUserSerializer(serializers.ModelSerializer):
    """Required fields on registering users"""

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

    def create(self, validated_data):
        validated_user = {
            "email": validated_data["email"],
            "password": validated_data["password"],
        }

        user = User.objects.create_user(**validated_user)

        print("validated_data", validated_data)

        return user
