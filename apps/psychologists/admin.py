from django.contrib import admin

from .models import (
    Psychologist,
    Specialization,
    TherapeuticModel,
    WorkPopulation,
    Education,
)

admin.site.register(Psychologist)
admin.site.register(Specialization)
admin.site.register(TherapeuticModel)
admin.site.register(WorkPopulation)
admin.site.register(Education)
