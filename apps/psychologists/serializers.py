from rest_framework import serializers
from apps.psychologists.models import Psychologist, SocialNetwork
import apps.accounts.constants as constants
from apps.accounts.serializers import UserSerializer, RegisterUserSerializer


class PsychologistSerializer(UserSerializer):
    """Returned fields after registering"""

    class Meta(UserSerializer.Meta):
        model = Psychologist
        fields = UserSerializer.Meta.fields + (
            "description",
            "gender_identity",
            "education",
            "social_networks",
        )


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
            "gender_identity",
            "education",
            "social_networks",
        )

    def create(self, validated_data):
        psychologist = Psychologist.objects.create_user(**validated_data)
        psychologist.save()
        return psychologist
