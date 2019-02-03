from django.contrib import admin
from .models import Profile, Meeting, Attendee, Sentence

admin.site.register(Profile)
admin.site.register(Meeting)
admin.site.register(Attendee)
admin.site.register(Sentence)