from django.test import TestCase
from django.contrib.auth.models import User
from .models import Book
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class BookModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            description='Test Description',
            owner=self.user
        )
    def test_book_creation(self):
        self.assertEqual(str(self.book), 'Test Book')

    def test_book_owner(self):
        self.assertEqual(self.book.owner.username, 'testuser')

class BookAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.book = Book.objects.create(
            title='API Book',
            author='API Author',
            description='API Description',
            owner=self.user
        )

        # Get JWT token
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass'
        }, format='json')
        self.access_token = response.data['access']

    def test_get_books(self):
        url = reverse('book-list')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'API Book')
