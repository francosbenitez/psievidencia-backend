from django.urls import path

from apps.psychologists import views

urlpatterns = [
  path('psychologists', views.PaginatedPsychologists.as_view()),
  path('latest-psychologists/', views.LatestPsychologistsList.as_view())
]