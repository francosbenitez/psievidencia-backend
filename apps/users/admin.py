from django.contrib import admin

from .models import User, Authenticated

admin.site.register(User)
admin.site.register(Authenticated)
