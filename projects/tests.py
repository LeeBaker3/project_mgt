from django.test import TestCase, Client
from django.urls import reverse
from .models import Project, Deliverable
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

# Create your tests here


class ProjectTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )

        self.project = Project.objects.create(
            project_name='Moon Landing',
            project_manager='Neil Armstrong',
            project_number='abc123'
        )

        self.deliverable = Deliverable.objects.create(
            project=self.project,
            deliverable_name='Engine',
            deliverable_description='Rocket for stage 1'
        )

    def test_project_listing(self):
        self.assertEqual(f'{self.project.project_name}', 'Moon Landing')
        self.assertEqual(f'{self.project.project_manager}', 'Neil Armstrong')
        self.assertEqual(f'{self.project.project_number}', 'abc123')

    def test_project_list_view_for_logged_in_user(self):
        self.client.login(email='testuser@email.com',
                          password='testpass123')
        response = self.client.get(reverse('project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Moon Landing')
        self.assertTemplateUsed(response, 'projects/project_list.html')

    def test_project_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('project_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '%s?next=/projects/' % (reverse('account_login'))
        )
        response = self.client.get(
            '%s?next=/projects/' % (reverse('account_login'))
        )
        self.assertContains(response, 'Log In')
