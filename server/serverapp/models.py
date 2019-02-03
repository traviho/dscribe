from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  #voice_sample

class Meeting(models.Model):
  date = models.DateField()
  name = models.CharField(max_length = 256)
  description = models.TextField()
  #audio = models.FileField(upload_to='meetingaudio/')
  text = models.TextField()
  keyText = models.TextField()
  sentimentScore = models.DecimalField(max_digits = 2, decimal_places = 1)
  sentimentMagnitude = models.DecimalField(max_digits = 2, decimal_places = 1)
  wordCount = models.PositiveSmallIntegerField()
  keyWordCount = models.PositiveSmallIntegerField()

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

class Attendee(models.Model):
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
  text = models.TextField()
  keyText = models.TextField()
  wordCount = models.PositiveSmallIntegerField()
  keyWordCount = models.PositiveSmallIntegerField()
  numQuestions = models.PositiveSmallIntegerField()

class Sentence(models.Model):
  attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
  text = models.TextField()
  keyText = models.TextField()
  beginOffset = models.PositiveSmallIntegerField()
  sentimentScore = models.DecimalField(max_digits = 2, decimal_places = 1)
  sentimentMagnitude = models.DecimalField(max_digits = 2, decimal_places = 1)
  wordCount = models.PositiveSmallIntegerField()
  keyWordCount = models.PositiveSmallIntegerField()
  question = models.BooleanField()
