from django.contrib import admin

from .models import Film, user_history
# Register your models here.
admin.site.register(Film)
admin.site.register(user_history)