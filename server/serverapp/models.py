from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  #voice_sample

class Meeting(models.Model):
  date = models.DateField()
  name = models.CharField(max_length = 128)
  #audio = models.FileField(upload_to='meetingaudio/')
  text = models.TextField()

  MEETING_CATEGORIES = [
    ('Brainstorming', 'Brainstorming'),
    ('Planning', 'Planning'),
    ('Training', 'Training'),
    ('Status Updating', 'Status Updating'),
    ('Decision Making', 'Decision Making'),
    ('Problem Solving', 'Problem Solving'),
    ('Reporting', 'Reporting'),
    ('Other', 'Other')
  ]
  category = models.CharField(choices = MEETING_CATEGORIES, max_length = 200)

class MeetingMember(models.Model):
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
  text = models.TextField()

# Models for results