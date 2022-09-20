from django.urls import path
from apps.suggestions import views

urlpatterns = [
    path("suggestions", views.SuggestionsList.as_view()),
    path("suggestions/create", views.CreateSuggestion.as_view()),
]
