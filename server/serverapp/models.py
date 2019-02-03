from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  #voice_sample

class Meeting(models.Model):
  date = models.DateField()
  name = models.CharField(max_length = 128)

  MEETING_CATEGORIES = (
    'Brainstorming',
    'Planning',
    'Training',
    'Status Updating',
    'Decision Making',
    'Problem Solving',
    'Reporting',
    'Other'
  )
  category = models.CharField(choices = MEETING_CATEGORIES)

