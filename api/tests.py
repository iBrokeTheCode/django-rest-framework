from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from rest_framework.test import APITestCase

from api.models import User, Order, Product


class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', password='password', email='')
        self.normal_user = User.objects.create_user(
            username='user', password='password', email='')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=10.0,
            stock=100,
        )
        self.url = reverse('api:product_detail', kwargs={
                           'pk': self.product.pk})

    def test_get_product(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], self.product.name)

    def test_unauthorized_update_product(self):
        data = {'name': 'Updated Product'}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_delete_product(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
