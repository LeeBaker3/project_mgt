from django.test import TestCase, Client
from django.urls import reverse
from .models import Person
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

# Create your tests here.


class ProjectTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )

        self.person = Person.objects.create(
            title='Mr',
            first_name='Buzz',
            last_name='Aldrin'

        )

    def test_person_listing(self):
        self.assertEqual(f'{self.person.title}', 'Mr')
        self.assertEqual(f'{self.person.first_name}', 'Buzz')
        self.assertEqual(f'{self.person.last_name}', 'Aldrin')

    def test_person_list_view_for_logged_in_user(self):
        self.client.login(email='testuser@email.com',
                          password='testpass123')
        response = self.client.get(reverse('person_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Aldrin')
        self.assertTemplateUsed(response, 'persons/person_list.html')

    def test_person_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('person_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '%s?next=/persons/' % (reverse('account_login'))
        )
        response = self.client.get(
            '%s?next=/persons/' % (reverse('account_login'))
        )
        self.assertContains(response, 'Log In')

    def test_person_detail_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(self.person.get_absolute_url())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '%s?next=/persons/%s' % (
                (reverse('account_login')), self.person.id)
        )
        response = self.client.get(
            '%s?next=/persons/%s' % (reverse('account_login'),
                                     self.person.id)
        )
        self.assertContains(response, 'Log In')
