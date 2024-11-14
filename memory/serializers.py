
from rest_framework import serializers
from .models import Memory, ProfilePic
from django.contrib.auth.models import User

class MemorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = ['id', 'user', 'media', 'description', 'date_created']



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']



class ProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePic
        fields = ['id', 'profile_image']