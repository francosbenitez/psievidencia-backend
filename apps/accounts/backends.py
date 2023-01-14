from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed


class CustomBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            raise AuthenticationFailed("Email o contraseña inválidos")
        if not user.check_password(password):
            raise AuthenticationFailed("Email o contraseña inválidos")
        if not user.is_active:
            raise AuthenticationFailed("El usuario no está activo")
        return user
