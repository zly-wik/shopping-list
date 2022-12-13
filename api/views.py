from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request, **kwargs):
        if request.method == 'GET':
            profile = self.get_queryset().first()
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        
        
        
        elif request.method in ['PUT', 'PATCH']:
            instance = self.get_queryset().first()
            serializer = UserProfileSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, 200)
            else:
                return Response(serializer.errors, 400)
            