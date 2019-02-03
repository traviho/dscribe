from django.contrib.auth.models import User, Group
from .models import Meeting, Attendee, Sentence
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class MeetingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Meeting
        fields = ('url', 'name', 'date', 'category')

class AttendeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attendee
        fields = ('url', 'user', 'meeting', 'text', 'key_text', 'word_count', 'key_word_count', 'sentiment_score', 'sentiment_magnitude', 'num_questions')

class SentenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sentence
        fields = ('url', 'text', 'key_text', 'begin_offset', 'word_count', 'keyWord_count', 'sentiment_score', 'sentiment_magnitude', 'question')
