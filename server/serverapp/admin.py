from django.contrib import admin
from django.contrib.auth.models import User
from .models import Meeting, Attendee, Sentence, Profile

#admin.site.register(User)
admin.site.register(Meeting)
admin.site.register(Attendee)
admin.site.register(Sentence)
admin.site.register(Profile)
