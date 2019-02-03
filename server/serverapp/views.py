from django.shortcuts import render

from django.contrib.auth.models import User, Group
from .models import Meeting, Attendee, Sentence
from rest_framework import viewsets
from serverapp.serializers import UserSerializer, GroupSerializer, MeetingSerializer, AttendeeSerializer, SentenceSerializer
from rest_framework.views import APIView

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

    takes in the query meetings=(ids of meetings desired)
    example: localhost:8000/meeting/?meetings=1,2,3

    The way to get the words/text specific to individual attendees given a meeting is to
    take the returned ids of attendees, and then use that to query from localhost:8000/attendee/?insertqueryhere

    A way to get the percentage of words spoken by an attendee is to divide the attendee's total text count by the
    meeting's text count

    ex: i query form localhost:8000/attendee/1,2,3,4 and get the json representing what was said by attendees 1,2,3,4
    for a given meeting

    each attendee has data for how many words they spoke, so that can just be divided by total word counts of the meeting
    """

    serializer_class = MeetingSerializer

    def get_queryset(self):
        queryset = Meeting.objects.all()
        target_meetings = self.request.query_params.get('meetings',None)

        if target_meetings is not None:
            target_meetings = target_meetings.split(',')
            queryset = queryset.filter(pk__in=target_meetings)

        return queryset

class AttendeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows attendees of a meeting to be viewed or edited

    takes in the query user= and meeting=
    example: localhost:8000/attendee/?user=1,2,3&meeting=1,2 will return
    json where foreign keys match 1,2,3 and where foreign key matches 1 and 2

    to mix meetings and different users (i.e user 1 for meeting 1 and user 2 for meeting 2),
    multiple api calls will have to be made. one call for user=1 and meeting=1 and another
    for user=2 and meeting=2


    """

    serializer_class = AttendeeSerializer

    def get_queryset(self):
        queryset = Attendee.objects.all()
        target_user = self.request.query_params.get('user', None)

        target_meeting = self.request.query_params.get('meeting', None)


        if target_user is not None:
            target_user = target_user.split(',')
            queryset = queryset.filter(user__in = target_user)

        if target_meeting is not None:
            target_meeting = target_meeting.split(',')
            queryset = queryset.filter(meeting__in = target_meeting)

        return queryset


class SentenceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sentences to be viewed or changed

    queries for attendees
    example: localhost:9000/sentence/?attendee=1,2 will return json
    representing the sentences that have a foreign keys matching with attendees
    1 and 2.
    """

    serializer_class = SentenceSerializer

    def get_queryset(self):
        queryset = Sentence.objects.all()
        target_attendee = self.request.query_params.get('attendee', None)

        if target_attendee is not None:
            target_attendee = target_attendee.split(',')
            queryset = queryset.filter(attendee__in = target_attendee)

        return queryset

