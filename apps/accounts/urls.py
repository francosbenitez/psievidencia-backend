from django.urls import path
from apps.accounts import views

urlpatterns = [
    path("register", views.Register.as_view()),
]
