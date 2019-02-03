from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  #voice_sample

class Meeting(models.Model):
  date = models.DateField()
  name = models.CharField(max_length = 256)
  description = models.TextField()
  text = models.TextField()
  key_text = models.TextField()
  word_count = models.PositiveSmallIntegerField()
  key_word_count = models.PositiveSmallIntegerField()
  sentiment_score = models.DecimalField(max_digits = 2, decimal_places = 1)
  sentiment_magnitude = models.DecimalField(max_digits = 2, decimal_places = 1)

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
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
  text = models.TextField()
  key_text = models.TextField()
  word_count = models.PositiveSmallIntegerField()
  key_word_count = models.PositiveSmallIntegerField()
  sentiment_score = models.DecimalField(max_digits = 2, decimal_places = 1)
  sentiment_magnitude = models.DecimalField(max_digits = 2, decimal_places = 1)
  num_questions = models.PositiveSmallIntegerField()

class Sentence(models.Model):
  attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
  text = models.TextField()
  key_text = models.TextField()
  begin_offset = models.PositiveSmallIntegerField()
  word_count = models.PositiveSmallIntegerField()
  keyWord_count = models.PositiveSmallIntegerField()
  sentiment_score = models.DecimalField(max_digits = 2, decimal_places = 1)
  sentiment_magnitude = models.DecimalField(max_digits = 2, decimal_places = 1)
  question = models.BooleanField()
