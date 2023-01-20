from apps.psychologists.models import Psychologist
from apps.accounts.serializers import UserSerializer, RegisterUserSerializer
from apps.psychologists.utils import validate_profile


class PsychologistSerializer(UserSerializer):
    """Returned fields after registering"""

    class Meta(UserSerializer.Meta):
        model = Psychologist
        fields = UserSerializer.Meta.fields + (
            "description",
            "gender_identity",
            "education",
            "instagram_profile",
            "linkedin_profile",
            "registration_name",
            "registration_number",
        )


class RegisterPsychologistSerializer(RegisterUserSerializer):
    """Required fields on registering"""

    class Meta(RegisterUserSerializer.Meta):
        model = Psychologist
        fields = RegisterUserSerializer.Meta.fields + (
            "description",
            "gender_identity",
            "education",
            "instagram_profile",
            "linkedin_profile",
            "registration_name",
            "registration_number",
        )

    def validate_linkedin_profile(self, linkedin_profile):
        return validate_profile(linkedin_profile)

    def validate_instagram_profile(self, instagram_profile):
        return validate_profile(instagram_profile)

    def create(self, validated_data):
        psychologist = Psychologist.objects.create_user(**validated_data)
        psychologist.save()
        return psychologist
