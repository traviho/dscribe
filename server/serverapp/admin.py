from django.contrib import admin
from .models import Profile, Meeting

admin.site.register(Profile, Meeting)
