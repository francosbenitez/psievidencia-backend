from django.urls import path
from apps.psychologists import views

urlpatterns = [
    path("register", views.Register.as_view()),
]
