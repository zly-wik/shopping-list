import pytest
from rest_framework.test import APIClient
from rest_framework import status
from model_bakery import baker

from api.models import User, UserProfile, Checklist


@pytest.mark.django_db
class TestCreateChecklist:
    def test_if_user_is_anonymous_returns_401(self):
        client = APIClient()
        
        response = client.post('/checklists/', data={'title': 'a'})
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    # Not sure if 403 is good status code, permissions will allow to post up to 3 with standard and 5 with premium profile
    # @pytest.mark.skip
    def test_if_user_is_standard_checklist_limit_returns_403(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        profile.profile_level = UserProfile.STANDARD
        baker.make(Checklist, _quantity=3, owner=profile)
        client = APIClient()
        client.force_authenticate(user=user)
        
        response = client.post('/checklists/', data={'title': 'a'})
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    # Not sure if 403 is good status code, permissions will allow to post up to 3 with standard and 5 with premium profile
    # @pytest.mark.skip
    def test_if_user_is_premium_checklist_limit_returns_403(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        profile.profile_level = UserProfile.PREMIUM
        baker.make(Checklist, _quantity=5, owner=profile)
        client = APIClient()
        client.force_authenticate(user=user)
        
        response = client.post('/checklists/', data={'title': 'a'})
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_if_user_is_authenticated_invalid_data_returns_400(self):
        user = baker.make(User, id=1)
        # profile = baker.make(UserProfile, id=1, user=user, profile_level=UserProfile.PREMIUM, checklists={})
        client = APIClient()
        client.force_authenticate(user=user)
        
        response = client.post('/checklists/', data={'title': ''})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_if_user_is_authenticated_valid_data_returns_201(self):
        user = baker.make(User, id=1)
        # profile = baker.make(UserProfile, id=1, user=user, profile_level=UserProfile.PREMIUM)
        client = APIClient()
        client.force_authenticate(user=user)
        
        response = client.post('/checklists/', data={'title': 'a'})
        
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestRetrieveChecklist:
    def test_if_user_is_anonymous_list_returns_401(self):
        client = APIClient()
        
        response = client.get('/checklists/')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_if_user_is_anonymous_detail_returns_401(self):
        client = APIClient()
        
        response = client.get(f'/checklists/1/')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_if_user_is_authenticated_list_owned_returns_200(self):
        user = baker.make(User, id=1)
        client = APIClient()
        client.force_authenticate(user=user)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, _quantity=2, owner=profile)
        
        response = client.get('/checklists/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['owner'] == profile.pk
        
    def test_if_user_is_authenticated_detail_owned_returns_200(self):
        user = baker.make(User, id=1)
        client = APIClient()
        client.force_authenticate(user=user)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        
        response = client.get(f'/checklists/{checklist.pk}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['owner'] == profile.pk
        
    def test_if_user_is_authenticated_detail_not_owned_returns_403(self):
        user = baker.make(User, id=1)
        client = APIClient()
        client.force_authenticate(user={})
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        
        response = client.get(f'/checklists/{checklist.pk}/')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_authenticated_detail_not_found_returns_404(self):
        user = baker.make(User, id=1)
        client = APIClient()
        client.force_authenticate(user=user)
        
        response = client.get(f'/checklists/1/')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateChecklist:
    def test_if_user_is_anonymous_update_returns_401(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        client = APIClient()
        
        response_put = client.put(f'/checklists/{checklist.pk}/', data={'title': 'a'})
        response_patch = client.patch(f'/checklists/{checklist.pk}/', data={'title': 'a'})
        
        assert response_put.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_patch.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_if_user_is_authenticated_not_owner_returns_403(self):
        user = baker.make(User, id=1)
        client = APIClient()
        client.force_authenticate(user={})
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        
        response_put = client.put(f'/checklists/{checklist.pk}/', data={'title': 'a'})
        response_patch = client.patch(f'/checklists/{checklist.pk}/', data={'title': 'a'})
        
        assert response_put.status_code == status.HTTP_403_FORBIDDEN
        assert response_patch.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_user_is_authenticated_owner_invalid_data_returns_400(self):
        user = baker.make(User, id=1)
        client = APIClient()
        client.force_authenticate(user=user)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        
        response_put = client.put(f'/checklists/{checklist.pk}/', data={'title': ''})
        response_patch = client.patch(f'/checklists/{checklist.pk}/', data={'title': ''})
        
        assert response_put.status_code == status.HTTP_400_BAD_REQUEST
        assert response_patch.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_if_user_is_authenticated_owner_valid_data_returns_200(self):
        user = baker.make(User, id=1)
        client = APIClient()
        client.force_authenticate(user=user)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        
        response_put = client.put(f'/checklists/{checklist.pk}/', data={'title': 'a'})
        response_patch = client.patch(f'/checklists/{checklist.pk}/', data={'title': 'a'})
        
        assert response_put.status_code == status.HTTP_200_OK
        assert response_patch.status_code == status.HTTP_200_OK

    def test_if_user_is_authenticated_detail_not_found_returns_404(self):
        user = baker.make(User, id=1)
        client = APIClient()
        client.force_authenticate(user=user)
        
        response_put = client.put(f'/checklists/1/')
        response_patch = client.put(f'/checklists/1/')
        
        assert response_put.status_code == status.HTTP_404_NOT_FOUND
        assert response_patch.status_code == status.HTTP_404_NOT_FOUND
        
        
@pytest.mark.django_db
class TestDeleteChecklist:
    def test_if_user_is_anonymous_list_returns_401(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        client = APIClient()
        
        response = client.delete(f'/checklists/{checklist.pk}/')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_if_user_is_authenticated_owner_returns_204(self):
        user = baker.make(User, id=1)
        client = APIClient()
        client.force_authenticate(user=user)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        
        response = client.delete(f'/checklists/{checklist.pk}/')
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
    def test_if_user_is_authenticated_detail_not_owned_returns_403(self):
        user = baker.make(User, id=1)
        profile = UserProfile.objects.filter(user=user).first()
        checklist = baker.make(Checklist, owner=profile)
        client = APIClient()
        client.force_authenticate(user={})
        
        response = client.delete(f'/checklists/{checklist.pk}/')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_authenticated_not_found_returns_404(self):
        user = baker.make(User, id=1)
        client = APIClient()
        client.force_authenticate(user=user)
        
        response = client.get(f'/checklists/1/')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND