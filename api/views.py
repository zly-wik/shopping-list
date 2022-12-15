from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import UserProfile, Checklist, Item
from .serializers import UserProfileSerializer, ChecklistSerializer, ItemSerializer


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
            

class ChecklistViewSet(ModelViewSet):
    queryset = None
    serializer_class = ChecklistSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user and self.request.user.is_authenticated:
            qs = Checklist.objects.select_related('owner').prefetch_related('items').filter(owner__user=self.request.user)
            self.queryset = qs
            return qs
        return None
    

    def check_permissions(self, request):
        if request.user and request.user.is_authenticated:
            if request.method == 'POST':
                qs = self.get_queryset()
                if qs and qs.count() >= 3:
                    profile_level = qs.first().owner.profile_level
                    if profile_level == UserProfile.STANDARD:
                        self.permission_denied(self.request, 'You have reached the checklists limit for your account type', 403)
                    elif qs.count() >= 5 and profile_level == UserProfile.PREMIUM:
                        self.permission_denied(self.request, 'You have reached the checklists limit for your account type', 403)
        else:
            self.permission_denied(self.request, 'You have to be logged in order to create checklist', 401)
        
    def perform_create(self, serializer):
        owner = UserProfile.objects.filter(user=self.request.user).first()
        serializer.save(owner=owner)
        
        
class ItemViewSet(ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if 'checklist_pk' in self.kwargs:
            return Item.objects.select_related('checklist').filter(checklist__id=self.kwargs['checklist_pk'])
        return None
    
    def perform_create(self, serializer):
        checklist = Checklist.objects.get(id=self.kwargs['checklist_pk'])
        serializer.save(checklist=checklist)