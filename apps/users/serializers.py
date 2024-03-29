from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import User, Authenticated
from apps.psychologists.models import Psychologist


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "role")


class AuthenticatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authenticated
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


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "role")
        extra_kwargs = {
            "password": {"write_only": True},
            "role": {"required": True, "allow_blank": False},
            "email": {"required": True, "allow_blank": False},
        }

    def create(self, validated_data):
        role = validated_data["role"]

        def create_usr(Model):
            created_user = Model.objects.create_user(
                validated_data["username"],
                validated_data["email"],
                validated_data["password"],
                role=role,
            )
            return created_user

        if role == "AUTHENTICATED":
            return create_usr(Authenticated)

        return create_usr(Psychologist)


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ["email"]


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ["password", "token", "uidb64"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("The reset link is invalid", 401)

            user.set_password(password)
            user.save()

            return user
        except Exception as e:
            raise AuthenticationFailed("The reset link is invalid", 401)
        return super().validate(attrs)


class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=1, write_only=True)
    from_email = serializers.CharField(min_length=1, write_only=True)
    message = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ["name", "from_email", "message"]
