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
        favorites_psychologists = [
            Psychologist.objects.filter(id=item["psychologist_id"])[0]
            for item in favorites.values()
        ]

        serializer = PsychologistSerializer(favorites_psychologists, many=True)
        return Response(serializer.data)
