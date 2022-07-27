from django.urls import path
from knox import views as knox_views
from apps.users import views

urlpatterns = [
    path("users", views.UsersList.as_view()),
    path("suggestions", views.SuggestionsList.as_view()),
    path("suggestions/create", views.CreateSuggestion.as_view()),
    path("favorites/<int:psychologist_id>/create", views.CreateFavorite.as_view()),
    path("favorites/<int:psychologist_id>/delete", views.DeleteFavorite.as_view()),
    path("favorites", views.FavoritesList.as_view()),
    path("register", views.RegisterAPI.as_view()),
    path("login", views.LoginAPI.as_view()),
    path("logout", knox_views.LogoutView.as_view()),
    path("logoutall", knox_views.LogoutAllView.as_view()),
    path("activate-user/<uidb64>/<token>", views.activate_user, name="activate"),
]
