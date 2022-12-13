from rest_framework import serializers

from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'display_name', 'profile_level']
        read_only_fields = ['user']