from django.shortcuts import render

from django.contrib.auth.models import User, Group
from .models import Meeting, MeetingMember, Profile
from rest_framework import viewsets
from serverapp.serializers import UserSerializer, GroupSerializer, MeetingSerializer, MeetingMemberSerializer, ProfileSerializer


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

class MeetingMemberViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows meeting members to be viewed or edited
    """
    queryset = MeetingMember.objects.all()
    serializer_class = MeetingMemberSerializer