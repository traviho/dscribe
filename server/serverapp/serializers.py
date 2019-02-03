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
        fields = ('url', 'name', 'date', 'category', 'description', 'text', 'key_text', 'word_count', 'key_word_count','sentiment_score', 'sentiment_magnitude')

    def to_representation(self, meeting):
        data = super().to_representation(meeting)
        key_word_dict = {}
        text_dict = {}

        for word in meeting.key_text.split(' '):
            key_word_dict[word] = key_word_dict.get(word,0) + 1

        for word in meeting.text.split(' '):
            text_dict[word] = text_dict.get(word,0) + 1

        attendee_ids = []

        attendees = Attendee.objects.all()
        for attendee in attendees:
            print(attendee.pk)
            if attendee.pk == meeting.id:
                attendee_ids.append(attendee.id)

        return {
            'name': meeting.name,
            'text': meeting.text,
            'text_dict': text_dict,
            'key_text': meeting.key_text,
            'key_word_dict': key_word_dict,
            'total_key_words': meeting.key_word_count,
            'total_words': meeting.word_count,
            'sentiment_score': meeting.sentiment_score,
            'sentiment_magnitude': meeting.sentiment_magnitude,
            'attendee_ids': attendee_ids,
            'date': meeting.date
            }


class AttendeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attendee
        fields = ('url', 'user', 'meeting', 'text', 'key_text', 'word_count', 'key_word_count', 'sentiment_score', 'sentiment_magnitude', 'num_questions')

class SentenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sentence
        fields = ('url', 'text', 'key_text', 'begin_offset', 'word_count', 'keyWord_count', 'sentiment_score',
                  'sentiment_magnitude', 'question')
