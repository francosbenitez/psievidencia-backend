from django.urls import path
from knox import views as knox_views
from apps.users import views

urlpatterns = [
    path("users", views.UsersList.as_view()),
    path("suggestions", views.SuggestionsList.as_view()),
    path("register", views.RegisterAPI.as_view()),
    path("login", views.LoginAPI.as_view()),
    path("logout", knox_views.LogoutView.as_view()),
    path("logoutall", knox_views.LogoutAllView.as_view()),
]
