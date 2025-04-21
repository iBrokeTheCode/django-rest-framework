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
