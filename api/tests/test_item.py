import pytest
from rest_framework.test import APIClient
from rest_framework import status
from model_bakery import baker

from api.models import User, UserProfile, Checklist, Item


@pytest.mark.django_db
class TestCreateItem:
    def test_if_user_is_anonymous_returns_401(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        client = APIClient()
        
        response = client.post(f'/checklists/{checklist.pk}/items/', data={'text': 'a'})
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_if_user_is_authenticated_not_owner_returns_403(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        client = APIClient()
        client.force_authenticate(user={})
        
        response = client.post(f'/checklists/{checklist.pk}/items/', data={'text': 'a'})
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_if_user_is_authenticated_owner_invalid_data_returns_400(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        client = APIClient()
        client.force_authenticate(user=user)
        
        response = client.post(f'/checklists/{checklist.pk}/items/', data={'text': ''})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_if_user_is_authenticated_owner_valid_data_returns_201(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        client = APIClient()
        client.force_authenticate(user=user)
        
        response = client.post(f'/checklists/{checklist.pk}/items/', data={'text': 'a'})
        
        assert response.status_code == status.HTTP_201_CREATED
    
    @pytest.mark.xfail
    def test_if_user_is_authenticated_checklist_not_found_returns_404(self):
        user = baker.make(User, id=1)
        client = APIClient()
        client.force_authenticate(user=user)
        
        response = client.post(f'/checklists/1/items/', data={'text': 'a'})
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    

@pytest.mark.django_db
class TestRetrieveItem:
    def test_if_user_is_anonymous_list_returns_401(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        client = APIClient()
        
        response = client.get(f'/checklists/{checklist.pk}/items/')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_if_user_is_anonymous_detail_returns_401(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        item = baker.make(Item, checklist=checklist)
        client = APIClient()
        
        response = client.get(f'/checklists/{checklist.pk}/items/{item.pk}/')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_if_user_is_authenticated_not_owner_list_returns_403(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        client = APIClient()
        client.force_authenticate(user={})
        
        response = client.get(f'/checklists/{checklist.pk}/items/')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_user_is_authenticated_not_owner_detail_returns_403(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        item = baker.make(Item, checklist=checklist)
        client = APIClient()
        client.force_authenticate(user={})
        
        response = client.get(f'/checklists/{checklist.pk}/items/{item.pk}/')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_if_user_is_authenticated_owner_list_returns_200(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        client = APIClient()
        client.force_authenticate(user=user)
        
        response = client.get(f'/checklists/{checklist.pk}/items/')
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_if_user_is_authenticated_owner_detail_returns_200(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        item = baker.make(Item, checklist=checklist)
        client = APIClient()
        client.force_authenticate(user=user)
        
        response = client.get(f'/checklists/{checklist.pk}/items/{item.pk}/')
        
        assert response.status_code == status.HTTP_200_OK
        
    @pytest.mark.xfail
    def test_if_user_is_authenticated_item_not_found_returns_404(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        client = APIClient()
        client.force_authenticate(user=user)
        
        response = client.post(f'/checklists/{checklist.pk}/items/1', data={'text': 'a'})
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        

@pytest.mark.django_db
class TestUpdateItem:
    def test_if_user_is_anonymous_returns_401(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        item = baker.make(Item, checklist=checklist)
        client = APIClient()
        
        response_put = client.put(f'/checklists/{checklist.pk}/items/{item.pk}/', data={'text': 'a'})
        response_patch = client.patch(f'/checklists/{checklist.pk}/items/{item.pk}/', data={'text': 'a'})
        
        assert response_put.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_patch.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_if_user_is_authenticated_not_owner_returns_403(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        item = baker.make(Item, checklist=checklist)
        client = APIClient()
        client.force_authenticate(user={})
        
        response_put = client.put(f'/checklists/{checklist.pk}/items/{item.pk}/', data={'text': 'a'})
        response_patch = client.patch(f'/checklists/{checklist.pk}/items/{item.pk}/', data={'text': 'a'})
        
        assert response_put.status_code == status.HTTP_403_FORBIDDEN
        assert response_patch.status_code == status.HTTP_403_FORBIDDEN
        
    def test_if_user_is_authenticated_owner_invalid_data_returns_400(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        item = baker.make(Item, checklist=checklist)
        client = APIClient()
        client.force_authenticate(user=user)
        
        response_put = client.put(f'/checklists/{checklist.pk}/items/{item.pk}/', data={'text': ''})
        response_patch = client.patch(f'/checklists/{checklist.pk}/items/{item.pk}/', data={'text': ''})
        
        assert response_put.status_code == status.HTTP_400_BAD_REQUEST
        assert response_patch.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_if_user_is_authenticated_owner_valid_data_returns_200(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        item = baker.make(Item, checklist=checklist)
        client = APIClient()
        client.force_authenticate(user=user)
        
        response_put = client.put(f'/checklists/{checklist.pk}/items/{item.pk}/', data={'text': 'a'})
        response_patch = client.patch(f'/checklists/{checklist.pk}/items/{item.pk}/', data={'text': 'a'})
        
        assert response_put.status_code == status.HTTP_200_OK
        assert response_patch.status_code == status.HTTP_200_OK

    @pytest.mark.xfail
    def test_if_user_is_authenticated_checklist_not_found_returns_404(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        item = baker.make(Item, checklist=checklist)
        client = APIClient()
        client.force_authenticate(user=user)
        
        response_put = client.put(f'/checklists/{checklist.pk}/items/1/', data={'text': 'a'})
        response_patch = client.patch(f'/checklists/{checklist.pk}/items/1/', data={'text': 'a'})
        
        assert response_put.status_code == status.HTTP_404_NOT_FOUND
        assert response_patch.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteItem:
    def test_if_user_is_anonymous_returns_401(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        item = baker.make(Item, checklist=checklist)
        client = APIClient()
        
        response = client.delete(f'/checklists/{checklist.pk}/items/{item.pk}/')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_if_user_is_authenticated_not_owner_returns_403(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        item = baker.make(Item, checklist=checklist)
        client = APIClient()
        client.force_authenticate(user={})
        
        response = client.delete(f'/checklists/{checklist.pk}/items/{item.pk}/')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_user_is_authenticated_owner_returns_204(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        item = baker.make(Item, checklist=checklist)
        client = APIClient()
        client.force_authenticate(user=user)
        
        response = client.delete(f'/checklists/{checklist.pk}/items/{item.pk}/')
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    @pytest.mark.xfail
    def test_if_user_is_authenticated_checklist_not_found_returns_404(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        client = APIClient()
        client.force_authenticate(user=user)
        
        response = client.delete(f'/checklists/{checklist.pk}/items/')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
