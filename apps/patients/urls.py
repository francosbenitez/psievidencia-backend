from django.urls import path
from apps.patients import views

urlpatterns = [
    path("register", views.Register.as_view()),
]
