from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from .models import Suggestion, Favorite
from apps.psychologists.models import Psychologist
from .serializers import SuggestionSerializer, FavoriteSerializer
from apps.psychologists.serializers import PsychologistSerializer
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from .utils import generate_token
from django.utils.encoding import force_str, force_bytes, smart_bytes
from django.shortcuts import redirect
from django.template.loader import render_to_string


def send_activation_email(user, request):
    current_site = get_current_site(request)

    email_subject = "Activá tu cuenta"

    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = generate_token.make_token(user)

    email_body = render_to_string(
        "activate.html",
        {"user": user, "domain": current_site, "uid": uidb64, "token": token},
    )

    send_mail(
        email_subject,
        email_body,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )


def activate_user(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        # user.is_email_verified = True
        user.first_name = "I was activated"
        user.save()

        return render(request, "successful.html", {"user": user})
        # return redirect("https://www.psievidencia.com/")
    return render(request, "failed.html", {"user": user})


class UsersList(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_activation_email(user, request)

        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class SuggestionsList(APIView):
    def get(self, request, format=None):
        suggestions = Suggestion.objects.all()
        serializer = SuggestionSerializer(suggestions, many=True)
        return Response(serializer.data)


class CreateSuggestion(APIView):
    def post(self, request, format=None):
        serializer = SuggestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateFavorite(APIView):
    def post(self, request, psychologist_id, format=None):
        user_id = request.user.id

        if user_id == None:
            return Response(
                {"detail": "You are not logged in. Please log in and try again."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        favorites = list(Favorite.objects.filter(user_id=user_id).values())

        for item in favorites:
            if psychologist_id == item["psychologist_id"]:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        favorite = Favorite.objects.create(
            psychologist_id=psychologist_id, user_id=user_id
        )

        # psychologist = Psychologist.objects.get(id=psychologist_id)
        # psychologist.liked = True
        # psychologist.save()

        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data)


class DeleteFavorite(APIView):
    def delete(self, request, psychologist_id, format=None):
        user_id = request.user.id
        favorite = Favorite.objects.filter(
            psychologist_id=psychologist_id, user_id=user_id
        ).delete()

        # psychologist = Psychologist.objects.get(id=psychologist_id)
        # psychologist.liked = False
        # psychologist.save()

        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data)


class FavoritesList(APIView):
    def get(self, request, format=None):
        user_id = request.user.id
        favorites = Favorite.objects.filter(user_id=user_id)
        favorites_psychologists = []

        for item in favorites.values():
            favorite = Psychologist.objects.filter(id=item["psychologist_id"]).values()
            favorites_psychologists.append(favorite[0])

        for item in favorites_psychologists:
            item["liked"] = True

        serializer = PsychologistSerializer(favorites_psychologists, many=True)
        return Response(serializer.data)
