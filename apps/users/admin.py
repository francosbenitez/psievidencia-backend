from django.contrib import admin

from .models import User, Suggestion, Favorite

admin.site.register(User)
admin.site.register(Suggestion)
admin.site.register(Favorite)
