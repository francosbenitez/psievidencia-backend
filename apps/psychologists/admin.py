import inspect
import apps.psychologists.models as models
from django.contrib import admin

for name, obj in inspect.getmembers(models):
    if inspect.isclass(obj):
        try:
            admin.site.register(obj)
        except admin.sites.AlreadyRegistered:
            pass
