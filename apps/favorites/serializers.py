from .models import Favorite
from rest_framework import serializers


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ("id", "psychologist_id", "authenticated_id")
