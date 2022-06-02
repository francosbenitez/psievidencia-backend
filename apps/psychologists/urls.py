from django.urls import path

from apps.psychologists import views

urlpatterns = [
  path('latest-psychologists/', views.LatestPsychologistsList.as_view()),
  path('psychologists', views.PaginatedPsychologists.as_view())
]