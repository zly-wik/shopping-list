from rest_framework import serializers

from .models import UserProfile, Checklist, Item

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.SlugRelatedField(many=False, read_only=True, slug_field='user__email')
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'email', 'display_name', 'profile_level']
        read_only_fields = ['user', 'email']
        

class ChecklistSerializer(serializers.ModelSerializer):
    items = serializers.StringRelatedField(read_only=True, many=True)
    class Meta:
        model = Checklist
        fields = ['id', 'title', 'owner', 'background_image', 'items']
        read_only_fields = ['owner']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'text', 'done']