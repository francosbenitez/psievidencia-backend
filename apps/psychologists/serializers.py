from rest_framework import serializers
from apps.psychologists.models import Psychologist, SocialNetwork
import apps.accounts.constants as constants
from apps.accounts.serializers import RegisterUserSerializer


class PsychologistSerializer(serializers.ModelSerializer):
    """Returned fields after registering psychologists"""

    class Meta:
        model = Psychologist
        fields = ("id", "email", "role")


class SocialNetworkSerializer(serializers.ModelSerializer):
    """Serializer for the SocialNetwork model"""

    class Meta:
        model = SocialNetwork
        fields = ("facebook", "twitter", "instagram", "whatsapp")


class RegisterPsychologistSerializer(RegisterUserSerializer):
    """Required fields on registering"""

    social_networks = SocialNetworkSerializer(required=False)

    class Meta(RegisterUserSerializer.Meta):
        model = Psychologist
        fields = RegisterUserSerializer.Meta.fields + (
            "description",
            "social_networks",
        )

    def create(self, validated_data):
        validated_user = {
            "email": validated_data["email"],
            "password": validated_data["password"],
        }

        psychologist = Psychologist.objects.create_user(**validated_user)
        psychologist.role = constants.PSYCHOLOGIST

        if "social_networks" in validated_data:
            social_networks = validated_data["social_networks"]
            social_networks = SocialNetwork.objects.create(**social_networks)
            social_networks.save()
            psychologist.social_networks = social_networks

        if "avatar" in validated_data:
            psychologist.avatar = validated_data["avatar"]

        psychologist.save()
        return psychologist
