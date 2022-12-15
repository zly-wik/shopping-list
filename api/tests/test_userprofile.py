import pytest
from rest_framework.test import APIClient
from rest_framework import status
from model_bakery import baker

from api.models import User

@pytest.mark.django_db
class TestRetrieveMeEndpoint:
    def test_if_user_is_anonymous_returns_401(self):
        client = APIClient()
        
        response = client.get('/me/')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_if_user_is_authenticated_returns_200(self):
        user = baker.make(User)
        client = APIClient()
        client.force_authenticate(user=user)
        
        response = client.get('/me/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['user'] == user.pk
        

@pytest.mark.django_db
class TestUpdateMeEndpoint:
    def test_if_user_is_anonymous_returns_401(self):
        client = APIClient()
        
        response_put = client.put('/me/', data={'display_name': 'a'})
        response_patch = client.put('/me/', data={'display_name': 'a'})
        
        assert response_put.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_patch.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_if_user_is_authenticated_invalid_data_returns_400(self):
        user = baker.make(User)
        client = APIClient()
        client.force_authenticate(user=user)
        
        response_put = client.put('/me/', data={'display_name': ''})
        response_patch = client.put('/me/', data={'display_name': ''})
        
        assert response_put.status_code == status.HTTP_400_BAD_REQUEST
        assert response_patch.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_if_user_is_authenticated_valid_data_returns_200(self):
        user = baker.make(User)
        client = APIClient()
        client.force_authenticate(user=user)
        
        response_put = client.put('/me/', data={'display_name': 'a'})
        response_patch = client.put('/me/', data={'display_name': 'a'})
        
        assert response_put.status_code == status.HTTP_200_OK
        assert response_patch.status_code == status.HTTP_200_OK
        
