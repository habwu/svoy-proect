from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from school.models import School
from classroom.models import Classroom
from django.contrib import messages

class ClassroomViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.school = School.objects.create(name="Test School")
        self.teacher = User.objects.create_user(username="teacher", password="pass", is_teacher=True, school=self.school)
        self.admin = User.objects.create_user(username="admin", password="adminpass", is_admin=True, school=self.school)
        self.child = User.objects.create_user(username="child", password="pass", is_child=True, school=self.school)
        self.classroom = Classroom.objects.create(number=1, letter='A', teacher=self.teacher, school=self.school)
        self.classroom.child.add(self.child)

    def test_children_list_teacher(self):
        self.client.login(username='teacher', password='pass')
        response = self.client.get(reverse('classroom:children_list_teacher', args=[self.classroom.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'children_list_teacher/children_list_teacher.html')

    def test_teacher_classroom_guide(self):
        self.client.login(username='teacher', password='pass')
        response = self.client.get(reverse('classroom:teacher_classroom_guide'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_classroom_teacher/list_classroom.html')

    def test_classroom_list_view(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('classroom:list_classroom'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_classroom/list_classroom.html')

    def test_child_expel_admin(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('classroom:child_expel_admin', args=[self.child.id]))
        self.assertEqual(response.status_code, 302)
        self.child.refresh_from_db()
        self.assertTrue(self.child.is_expelled)

    def test_child_reinstate_admin(self):
        self.client.login(username='admin', password='adminpass')
        self.child.is_expelled = True
        self.child.save()
        response = self.client.post(reverse('classroom:child_reinstate_admin', args=[self.child.id]))
        self.assertEqual(response.status_code, 302)
        self.child.refresh_from_db()
        self.assertFalse(self.child.is_expelled)

    def test_classroom_create_view(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('classroom:classroom_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'classroom_add/classroom_form.html')

        response = self.client.post(reverse('classroom:classroom_create'), {
            'number': 2,
            'letter': 'B',
            'teacher': self.teacher.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Classroom.objects.filter(number=2, letter='B').exists())

    def test_classroom_update_view(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('classroom:classroom_update', args=[self.classroom.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'classroom_add/classroom_form.html')

        response = self.client.post(reverse('classroom:classroom_update', args=[self.classroom.id]), {
            'number': 3,
            'letter': 'C',
            'teacher': self.teacher.id
        })
        self.assertEqual(response.status_code, 302)
        self.classroom.refresh_from_db()
        self.assertEqual(self.classroom.number, 3)
        self.assertEqual(self.classroom.letter, 'C')

    def test_classroom_delete_view(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('classroom:classroom_delete', args=[self.classroom.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'classroom_add/classroom_confirm_delete.html')

        response = self.client.post(reverse('classroom:classroom_delete', args=[self.classroom.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Classroom.objects.filter(id=self.classroom.id).exists())

    def test_promote_all_classrooms_view(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('classroom:promote_all_classrooms'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_classroom/promote_all_classrooms_confirm.html')

        response = self.client.post(reverse('classroom:promote_all_classrooms'))
        self.assertEqual(response.status_code, 302)
        self.classroom.refresh_from_db()
        self.assertEqual(self.classroom.number, 2)
