from django.shortcuts import render

from django.contrib.auth.models import User, Group
from .models import Meeting, Attendee, Sentence
from rest_framework import viewsets
from serverapp.serializers import UserSerializer, GroupSerializer, MeetingSerializer, AttendeeSerializer, SentenceSerializer


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

class AttendeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows attendees of a meeting to be viewed or edited
    """

    serializer_class = AttendeeSerializer

    def get_queryset(self):
        queryset = Attendee.objects.all()
        target_user = self.request.query_params.get('user', None)
        target_meeting = self.request.query_params.get('meeting', None)

        if target_user is not None:
            queryset = queryset.filter(user = target_user)

        if target_meeting is not None:
            queryset = queryset.filter(meeting = target_meeting)

        return queryset


class SentenceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sentences to be viewed or changed
    """

    serializer_class = SentenceSerializer

    def get_queryset(self):
        queryset = Sentence.objects.all()
        target_attendee = self.request.query_params.get('attendee', None)

        if target_attendee is not None:
            queryset = queryset.filter(attendee = target_attendee)

        return queryset

