from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from users.models import User
from school.models import School
from classroom.models import Classroom


class AuthAPITestCase(TestCase):
    """Тесты для аутентификации через API."""

    def setUp(self):
        self.client = APIClient()
        self.school = School.objects.create(name='Test School')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com',
            school=self.school
        )
        self.token_url = reverse('users:token_obtain_pair')

    def test_valid_login(self):
        """Тест: успешный вход с правильными учетными данными."""
        response = self.client.post(self.token_url, {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_login(self):
        """Тест: вход с неверными учетными данными."""
        response = self.client.post(self.token_url, {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateUserAPITestCase(TestCase):
    """Тесты для создания пользователей через API."""

    def setUp(self):
        self.client = APIClient()
        self.school = School.objects.create(name='Test School')
        self.admin = User.objects.create_user(
            username='admin',
            password='adminpassword',
            is_admin=True,
            school=self.school
        )
        self.create_teacher_url = reverse('user-create-teacher')
        self.create_child_url = reverse('user-create-child')
        self.create_admin_url = reverse('user-create-admin')

    def authenticate_admin(self):
        """Аутентификация администратора."""
        response = self.client.post(reverse('users:token_obtain_pair'), {
            'username': 'admin',
            'password': 'adminpassword'
        })
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_create_teacher(self):
        """Тест: создание учителя."""
        self.authenticate_admin()
        response = self.client.post(self.create_teacher_url, {
            'username': 'new_teacher',
            'password': 'password123',
            'first_name': 'Teacher',
            'last_name': 'User',
            'gender': 'F',
            'school': self.school.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='new_teacher', is_teacher=True).exists())

    def test_create_child(self):
        """Тест: создание ученика."""
        self.authenticate_admin()
        response = self.client.post(self.create_child_url, {
            'username': 'new_child',
            'password': 'password123',
            'first_name': 'Child',
            'last_name': 'User',
            'gender': 'M',
            'school': self.school.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='new_child', is_child=True).exists())


class UserListAPITestCase(TestCase):
    """Тесты для получения списков пользователей."""

    def setUp(self):
        self.client = APIClient()
        self.school = School.objects.create(name='Test School')
        self.admin = User.objects.create_user(
            username='admin',
            password='adminpassword',
            is_admin=True,
            school=self.school
        )
        self.teacher = User.objects.create_user(
            username='teacher',
            password='password123',
            is_teacher=True,
            school=self.school
        )
        self.teachers_url = reverse('user-teachers')
        self.admins_url = reverse('user-admins')

    def authenticate_admin(self):
        """Аутентификация администратора."""
        response = self.client.post(reverse('users:token_obtain_pair'), {
            'username': 'admin',
            'password': 'adminpassword'
        })
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_get_teachers(self):
        """Тест: получение списка учителей."""
        self.authenticate_admin()
        response = self.client.get(self.teachers_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'teacher')

    def test_get_admins(self):
        """Тест: получение списка администраторов."""
        self.authenticate_admin()
        response = self.client.get(self.admins_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'admin')


class UserProfileAPITestCase(TestCase):
    """Тесты для работы с профилем пользователя."""

    def setUp(self):
        self.client = APIClient()
        self.school = School.objects.create(name='Test School')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com',
            school=self.school
        )
        self.profile_url = reverse('user-profile', kwargs={'pk': self.user.id})

    def authenticate_user(self):
        """Аутентификация пользователя."""
        response = self.client.post(reverse('users:token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_get_profile(self):
        """Тест: получение профиля пользователя."""
        self.authenticate_user()
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_update_profile(self):
        """Тест: обновление профиля пользователя."""
        self.authenticate_user()
        response = self.client.patch(self.profile_url, {
            'email': 'newemail@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'newemail@example.com')
