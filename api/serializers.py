from rest_framework import serializers

from .models import UserProfile, Checklist, Item

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'display_name', 'profile_level']
        read_only_fields = ['user']
        

class ChecklistSerializer(serializers.ModelSerializer):
    items = serializers.StringRelatedField(read_only=True, many=True)
    class Meta:
        model = Checklist
        fields = ['id', 'title', 'owner', 'items']
        read_only_fields = ['owner']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'text', 'done']