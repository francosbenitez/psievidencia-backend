from django.urls import path

from apps.users import views

urlpatterns = [
    path("users", views.UsersList.as_view()),
]
