from .models import Favorite
from .serializers import FavoriteSerializer
from apps.psychologists.serializers import PsychologistSerializer
from apps.users.models import Psychologist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CreateFavorite(APIView):
    def post(self, request, psychologist_id, format=None):
        user_id = request.user.id

        if user_id == None:
            return Response(
                {
                    "detail": "No iniciaste sesión. Por favor, iniciá sesión e intentá de nuevo."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        favorites = list(Favorite.objects.filter(authenticated_id=user_id).values())

        for item in favorites:
            if psychologist_id == item["psychologist_id"]:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        favorite = Favorite.objects.create(
            psychologist_id=psychologist_id, authenticated_id=user_id
        )

        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data)


class DeleteFavorite(APIView):
    def delete(self, request, psychologist_id, format=None):
        user_id = request.user.id

        favorite = Favorite.objects.filter(
            psychologist_id=psychologist_id, authenticated_id=user_id
        ).delete()

        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data)


class FavoritesList(APIView):
    def get(self, request, format=None):
        user_id = request.user.id

        favorites = Favorite.objects.filter(authenticated_id=user_id)
        favorites_psychologists = []

        for item in favorites.values():
            favorite = Psychologist.objects.filter(id=item["psychologist_id"]).values()
            favorites_psychologists.append(favorite[0])

        for item in favorites_psychologists:
            item["liked"] = True

        serializer = PsychologistSerializer(favorites_psychologists, many=True)
        return Response(serializer.data)
