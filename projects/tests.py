from django.test import TestCase, Client
from django.urls import reverse
from .models import Project

# Create your tests here


class ProjectTests(TestCase):

    def setUp(self):
        self.project = Project.objects.create(
            project_name='Moon Landing',
            project_manager='Neil Armstrong',
            project_number='abc123'
        )

    def test_project_listing(self):
        self.assertEqual(f'{self.project.project_name}', 'Moon Landing')
        self.assertEqual(f'{self.project.project_manager}', 'Neil Armstrong')
        self.assertEqual(f'{self.project.project_number}', 'abc123')

    def test_project_list_view(self):
        response = self.client.get(reverse('project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Moon Landing')
        self.assertTemplateUsed(response, 'projects/project_list.html')

    def test_project_detail_view(self):
        response = self.client.get(self.project.get_absolute_url())
        no_response = self.client.get('/projects/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Moon Landing')
        self.assertTemplateUsed(response, 'projects/project_detail.html')
