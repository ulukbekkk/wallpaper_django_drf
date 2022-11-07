from rest_framework import serializers

from .models import MyRoom


class MyRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyRoom
        fields = '__all__'