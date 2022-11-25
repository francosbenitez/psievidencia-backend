from django.urls import path
from apps.accounts.views import views

urlpatterns = [
    path("register", views.Register.as_view()),
]
