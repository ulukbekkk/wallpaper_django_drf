from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .helpers import OwnerMyRoomPermission

from .serializers import MyRoomSerializer
from .models import MyRoom


class MyRoomViewSet(ModelViewSet):
    serializer_class = MyRoomSerializer
    queryset = MyRoom.objects.all()
    permission_classes = (OwnerMyRoomPermission,)

