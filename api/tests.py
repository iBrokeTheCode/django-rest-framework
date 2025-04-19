from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from api.models import User, Order


class UserOrderTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', password='password1')
        self.user2 = User.objects.create_user(
            username='user2', password='password2')

        Order.objects.create(user=self.user1)
        Order.objects.create(user=self.user1)
        Order.objects.create(user=self.user2)
        Order.objects.create(user=self.user2)

    def test_user_order_endpoint_retrieves_only_the_authenticated_user_orders(self):
        user = User.objects.get(username='user2')
        self.client.force_login(user)
        response = self.client.get(reverse('api:user_orders'))

        assert response.status_code == 200

        orders = response.json()
        self.assertTrue(all(order['user'] == user.pk for order in orders))

    def test_user_order_list_unauthenticated(self):
        response = self.client.get(reverse('api:user_orders'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # 403 forbidden for normal authentication | 401 for JWT
