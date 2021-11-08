from django.test import TestCase
from authentication.models import User
from rest_framework.test import APITestCase


class TestModel(APITestCase):
    def test_creates_user(self):
        user = User.objects.create_user(
            username='testuser', email='test@gmail.com', password='testpass123'
        )
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertFalse(user.is_staff, False)
        self.assertTrue(user.is_active, True)
        self.assertFalse(user.is_admin, False)
        self.assertEqual(user.username, 'testuser')

    def test_creates_super_user(self):
        user = User.objects.create_superuser(
            username="testsuper",
            email='testsuper@gmail.com',
            password='testsuper1234'
        )
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'testsuper@gmail.com')
        self.assertEqual(user.username, 'testsuper')
        self.assertTrue(user.is_admin, True)
        self.assertTrue(user.is_active, True)
        self.assertTrue(user.is_staff, True)

    def test_create_staff_user(self):
        user = User.objects.create_staff(
            username="teststaff",
            email="teststaff@gmail.com",
            password="teststaff123"
        )
        self.assertIsInstance(user, User)
        self.assertEqual(user.first_name, "")
        self.assertEqual(user.username, 'teststaff')
        self.assertEqual(user.email, 'teststaff@gmail.com')
        self.assertTrue(user.is_staff, True)
        self.assertFalse(user.is_admin, False)
        self.assertTrue(user.is_active, True)
        self.assertFalse(user.email_verified, False)

    def test_raises_error_when_no_username_is_supplied(self):
        self.assertRaises(
            ValueError,
            User.objects.create_user,
            username="",
            email="testuser@gmail.com",
            password="testpass1234"
        )

    def test_raises_errors_when_no_email_is_supplied(self):
        self.assertRaises(
            ValueError,
            User.objects.create_user,
            username="testuser",
            email="",
            password="testpass1234"
        )

    def test_raises_errors_when_no_password_is_supplied(self):
        self.assertRaises(
            ValueError, User.objects.create_user,
            username="testuser",
            email="testpass@gmail.com",
            password=""
        )

    def test_raises_error_with_message_when_no_username_is_suppliered(self):
        with self.assertRaisesMessage(
                ValueError, "Users must have  a username!"):
            User.objects.create_user(
                username="",
                email="testuser@gmail.com",
                password="testpass1234")

    def test_raises_errors_with_message_when_no_email_is_suppliered(self):
        with self.assertRaisesMessage(
                ValueError, "Users must have an email!"):
            User.objects.create_user(
                username="testuser",
                email="",
                password="testpass1234"
            )

    def test_raises_errors_with_message_when_no_password_is_suppliered(self):
        with self.assertRaisesMessage(
                ValueError, "Users must have a password!"):
            User.objects.create_user(
                username="testuser",
                email="testuser@gmail.com",
                password=""
            )
