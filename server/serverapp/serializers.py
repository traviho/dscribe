from django.contrib.auth.models import User, Group
from .models import Meeting, MeetingMember, Profile
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

class MeetingMemberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MeetingMember
        fields = ('url', 'profile', 'meeting', 'text')

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('url', 'user')
