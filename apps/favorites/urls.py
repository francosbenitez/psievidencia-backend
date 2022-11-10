from django.urls import path
from apps.favorites import views

urlpatterns = [
    path("favorites/<int:psychologist_id>/create", views.CreateFavorite.as_view()),
    path("favorites/<int:psychologist_id>/delete", views.DeleteFavorite.as_view()),
    path("favorites", views.FavoritesList.as_view()),
]
