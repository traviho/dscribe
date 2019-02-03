from django.shortcuts import render

from django.contrib.auth.models import User, Group
from .models import Meeting, Attendee, Profile, Sentence
from rest_framework import viewsets
from serverapp.serializers import UserSerializer, GroupSerializer, MeetingSerializer, AttendeeSerializer, ProfileSerializer, SentenceSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class MeetingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited
    """
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows profiles to be viewed or edited
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class AttendeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows attendees of a meeting to be viewed or edited
    """

    serializer_class = AttendeeSerializer

    def get_queryset(self):
        queryset = Attendee.objects.all()
        target_user = self.request.query_params.get('user', None)
        target_meeting = self.request.query_params.get('meeting', None)

        print(target_meeting)
        if target_user is not None:
            queryset = queryset.filter(user = target_user)

        if target_meeting is not None:
            queryset = queryset.filter(meeting = target_meeting)

        return queryset


class SentenceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sentences to be viewed or changed
    """
    queryset = Sentence.objects.all()
    serializer_class =  SentenceSerializer