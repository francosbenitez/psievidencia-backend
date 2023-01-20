import inspect
from django.contrib import admin
import apps.psychologists.models as models

for name, obj in inspect.getmembers(models):
    if name != "BaseModel":
        if inspect.isclass(obj):
            try:
                admin.site.register(obj)
            except admin.sites.AlreadyRegistered:
                pass
