from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class TestListCreateTodos(APITestCase):
    def test_create_todo(self):
        sample_todo = {'title': 'hello',
                       'description': 'test'
                       }
        response = self.client.post(
            reverse('todos:todo-create'), sample_todo)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
