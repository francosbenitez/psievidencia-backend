from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer, RegisterSerializer
from apps.users.models import User
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
from django.contrib.auth import authenticate
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from googleapiclient.errors import HttpError
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from .tasks import activate_user, send_activation_email


class UsersList(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_activation_email(user, request)

        return Response(
            UserSerializer(user, context=self.get_serializer_context()).data
        )


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        username = request.data["username"]
        password = request.data["password"]

        authentication = authenticate(
            request.data, username=username, password=password
        )

        if authentication and not authentication.is_email_verified:
            return Response(
                {
                    "detail": "Tu email no está verificado. Por favor, verificá tu correo."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        login(request, user)

        x = super(LoginAPI, self).post(request, format=None).data

        y = {"user": UserSerializer(user).data}

        z = dict(list(x.items()) + list(y.items()))

        return Response(z)


class VerifyToken(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content = {"valid": True}
        return Response(content)


class SuggestionsList(APIView):
    def get(self, request, format=None):
        suggestions = Suggestion.objects.all()
        serializer = SuggestionSerializer(suggestions, many=True)
        return Response(serializer.data)


class CreateSuggestion(APIView):
    def post(self, request, format=None):

        try:
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive.file",
                "https://www.googleapis.com/auth/drive",
            ]

            creds = ServiceAccountCredentials.from_json_keyfile_name(
                "gcp_key.json", scope
            )
            client = gspread.authorize(creds)
            gsheet = client.open("Psievidencia feedback").worksheet("Main")

            time = datetime.datetime.now()
            time = time.strftime("%m/%d/%Y %H:%M:%S")
            row = [time, request.data["title"], request.data["description"]]
            gsheet.append_row(row, 2)
        except HttpError as error:
            print(f"An error occurred: {error}")

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

        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data)


class DeleteFavorite(APIView):
    def delete(self, request, psychologist_id, format=None):
        user_id = request.user.id
        favorite = Favorite.objects.filter(
            psychologist_id=psychologist_id, user_id=user_id
        ).delete()

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


class PasswordResetView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, *args, **kwargs):
        data = self.request.data
        email = data.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            print("user", user)
        return Response(
            {"message": "Please do check your email for further instructions!"},
            status=status.HTTP_200_OK,
        )
