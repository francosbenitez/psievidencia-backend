from django.urls import path, include

from apps.psychologists import views

from rest_framework.routers import DefaultRouter
from rest_framework import routers

router = DefaultRouter()
router.register(r'authors', views.TherapeuticModelViewSet, basename='therapeutic_model')
router.register(r'books', views.PsychologistViewSet, basename='psychologist')

urlpatterns = [
    path("psychologists", views.PaginatedPsychologists.as_view()),
    path("psychologists/<int:psychologist_id>", views.PsychologistDetail.as_view()),
    path("psychologists/<int:psychologist_id>/edit", views.UpdatePsychologist.as_view()),
    path("psychologists/specializations", views.SpecializationsList.as_view()),
    path("psychologists/therapeutic_models", views.TherapeuticModelsList.as_view()),
    path("psychologists/work_populations", views.WorkPopulationsList.as_view()),
    path("psychologists/provinces", views.ProvincesList.as_view()),

    path(r'test/', include(router.urls)),

]
