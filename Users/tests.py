from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User

class UsersTests(APITestCase):
    def test_create_user(self):
        url = reverse('user-list')
        data = {'user_name': 'Alice', 'balance': 150.00}
        response = self.client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.get(username='Alice').balance == 150.00

    def test_add_friendship_symmetric(self):
        user_a = User.objects.create(username="Alice", balance=100)
        user_b = User.objects.create(username="Bob", balance=100)
        
        url = reverse('user-add-friend', args=[user_a.user_id])
        response = self.client.post(url, {'friend_id': user_b.user_id}, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert user_b in user_a.friends.all()
        assert user_a in user_b.friends.all()