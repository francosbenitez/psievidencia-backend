from django.urls import path

from apps.psychologists import views

urlpatterns = [
    path("psychologists", views.PaginatedPsychologists.as_view()),
    path("psychologists/<int:psychologist_id>", views.PsychologistDetail.as_view()),
    path("psychologists/specializations", views.SpecializationsList.as_view()),
    path("psychologists/therapeutic_models", views.TherapeuticModelsList.as_view()),
    path("psychologists/work_populations", views.WorkPopulationsList.as_view()),
    path("psychologists/provinces", views.ProvincesList.as_view()),
]
