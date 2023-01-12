from rest_framework import serializers
from apps.psychologists.models import Psychologist, SocialNetwork
import apps.accounts.constants as constants


class SocialNetworkSerializer(serializers.ModelSerializer):
    """Serializer for the SocialNetwork model"""

    class Meta:
        model = SocialNetwork
        fields = ("facebook", "twitter", "instagram", "whatsapp")


class RegisterPsychologistSerializer(serializers.ModelSerializer):
    """Required fields on registering"""

    social_networks = SocialNetworkSerializer(required=False)

    class Meta:
        model = Psychologist
        fields = ("email", "password", "avatar", "social_networks")
        extra_kwargs = {
            "email": {"required": True, "allow_blank": False},
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        psychologist = Psychologist.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
        )
        psychologist.role = constants.PSYCHOLOGIST

        if "social_networks" in validated_data:
            social_networks = validated_data["social_networks"]
            social_networks = SocialNetwork.objects.create(**social_networks)
            social_networks.save()
            psychologist.social_networks = social_networks

        psychologist.avatar = validated_data["avatar"]
        psychologist.save()
        return psychologist


class PsychologistSerializer(serializers.ModelSerializer):
    """Returned fields after registering"""

    class Meta:
        model = Psychologist
        fields = ("id", "email", "role")
