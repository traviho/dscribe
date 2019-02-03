from django.shortcuts import render

from django.contrib.auth.models import User, Group
from .models import Meeting
from rest_framework import viewsets
from serverapp.serializers import UserSerializer, GroupSerializer, MeetingSerializer


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
