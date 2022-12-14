from rest_framework import serializers

from .models import UserProfile, Checklist

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'display_name', 'profile_level']
        read_only_fields = ['user']
        

class ChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklist
        fields = ['id', 'title', 'owner']
        read_only_fields = ['owner']
        