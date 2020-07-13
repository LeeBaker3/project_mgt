from django.test import TestCase, Client
from django.urls import reverse
from .models import Customer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

# Create your tests here.


class CustomerTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )
        self.special_permission = Permission.objects.get(
            codename='special_status'
        )

        self.customer = Customer.objects.create(
            name='NASA',
        )

    def test_customer_list_view_for_logged_in_user(self):
        self.client.login(email='testuser@email.com',
                          password='testpass123')
        response = self.client.get(reverse('customer_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'NASA')
        self.assertTemplateUsed(response, 'customers/customer_list.html')

    def test_customer_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('customer_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '%s?next=/customers/' % (reverse('account_login'))
        )
        response = self.client.get(
            '%s?next=/customers/' % (reverse('account_login'))
        )
        self.assertContains(response, 'Log In')

    def test_customer_detail_view_for_logged_in_user(self):
        self.client.login(email='testuser@email.com',
                          password='testpass123')
        response = self.client.get(self.customer.get_absolute_url())
        no_response = self.client.get('/customer/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'NASA')
        self.assertTemplateUsed(response, 'customers/customer_detail.html')

    def test_customer_detail_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(self.customer.get_absolute_url())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '%s?next=/customers/%s' % (
                (reverse('account_login')), self.customer.id)
        )
        response = self.client.get(
            '%s?next=/customers/%s' % (reverse('account_login'),
                                       self.customer.id)
        )
        self.assertContains(response, 'Log In')
