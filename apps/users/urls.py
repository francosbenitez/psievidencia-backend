from django.urls import path
from knox import views as knox_views
from apps.users import views

urlpatterns = [
    path("register", views.RegisterAPI.as_view()),
    path("login", views.LoginAPI.as_view()),
    path("logout", knox_views.LogoutView.as_view()),
    path("logoutall", knox_views.LogoutAllView.as_view()),
    path("activate-user/<uidb64>/<token>", views.activate_user, name="activate"),
    path("verify-token", views.VerifyToken.as_view()),
    path("profile", views.ProfileView.as_view()),
    path(
        "request-reset-email",
        views.RequestPasswordResetEmail.as_view(),
        name="request-reset-email",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        views.PasswordTokenCheckAPI.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "password-reset-complete",
        views.SetNewPasswordAPIView.as_view(),
        name="password-reset-complete",
    ),
]
