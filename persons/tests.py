from django.test import TestCase, Client
from django.urls import reverse
from .models import Person
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

# Create your tests here.


class PersonsTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )

        self.person = Person.objects.create(
            title='Astronaut',
            first_name='Buzz',
            last_name='Aldrin'

        )

    def test_person_listing(self):
        self.assertEqual(f'{self.person.title}', 'Astronaut')
        self.assertEqual(f'{self.person.first_name}', 'Buzz')
        self.assertEqual(f'{self.person.last_name}', 'Aldrin')

    def test_person_list_view_for_logged_in_user(self):
        self.client.login(email='testuser@email.com',
                          password='testpass123')
        response = self.client.get(reverse('person_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Buzz')
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

    def test_person_create_view_for_logged_in_user(self):
        self.client.login(email='testuser@email.com',
                          password='testpass123')

    def test_person_detail_view_for_logged_in_user(self):
        self.client.login(email='testuser@email.com',
                          password='testpass123')
        response = self.client.get(self.person.get_absolute_url())
        no_response = self.client.get('/persons/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Astronaut')
        self.assertContains(response, 'Buzz')
        self.assertContains(response, 'Aldrin')
        self.assertTemplateUsed(response, 'persons/person_detail.html')

    def test_person_create_view_for_logged_out_user(self):
        self.client.logout()
        url = reverse('person_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '%s?next=/persons/create/' % (
                (reverse('account_login')))
        )
        response = self.client.get(
            '%s?next=/persons/create/' % (reverse('account_login'))
        )
        self.assertContains(response, 'Log In')

    def test_person_update_view_for_logged_in_user(self):
        self.client.login(email='testuser@email.com',
                          password='testpass123')
        url = reverse('person_update', args=[str(self.person.id)])
        response = self.client.post(url,
                                    {'title': 'Astronaut',
                                     'first_name': 'Michael',
                                     'last_name': 'Collins'})
        self.person.refresh_from_db()
        self.assertEqual(self.person.title, 'Astronaut')
        self.assertEqual(self.person.first_name, 'Michael')
        self.assertEqual(self.person.last_name, 'Collins')
        self.assertEqual(response.status_code, 302)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'persons/person_update.html')

    def test_person_update_view_for_logged_out_user(self):
        self.client.logout()
        url = reverse('person_update', args=[str(self.person.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '%s?next=/persons/update/%s' % (
                (reverse('account_login')), self.person.id)
        )
        response = self.client.get(
            '%s?next=/persons/update/%s' % (reverse('account_login'),
                                            self.person.id)
        )
        self.assertContains(response, 'Log In')

    def test_person_delete_view_for_logged_in_user(self):
        self.client.login(email='testuser@email.com',
                          password='testpass123')
        url = reverse('person_delete', args=[str(self.person.id)])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Person.objects.filter(id=self.person.id).exists())

    def test_person_delete_view_for_logged_out_user(self):
        self.client.logout()
        url = reverse('person_delete', args=[str(self.person.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '%s?next=/persons/delete/%s' % (
                (reverse('account_login')), self.person.id)
        )
        response = self.client.get(
            '%s?next=/persons/delete/%s' % (reverse('account_login'),
                                            self.person.id)
        )
        self.assertContains(response, 'Log In')
