from django.contrib import admin
from .models import Profile, Meeting, MeetingMember

admin.site.register(Profile)
admin.site.register(Meeting)
admin.site.register(MeetingMember)