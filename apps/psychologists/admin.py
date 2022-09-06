from django.contrib import admin

from .models import (
    Psychologist,
    Specialization,
    TherapeuticModel,
    WorkPopulation,
    Education,
    WorkModality,
    Province,
    GenderIdentity,
    GenderPerspective,
)

admin.site.register(Psychologist)
admin.site.register(Specialization)
admin.site.register(TherapeuticModel)
admin.site.register(WorkPopulation)
admin.site.register(WorkModality)
admin.site.register(Province)
admin.site.register(Education)
admin.site.register(GenderIdentity)
admin.site.register(GenderPerspective)
