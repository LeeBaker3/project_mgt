from django.test import TestCase, Client
from django.urls import reverse
from .models import Project, Deliverable
from .forms import ProjectForm
from customers.models import Customer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

# Create your tests here


class ProjectTests(TestCase):
    """[summary]

    Args:
        TestCase ([type]): [description]
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )

        self.customer = Customer.objects.create(
            name='NASA',
        )

        self.project = Project.objects.create(
            project_name='Moon Landing',
            project_manager='Neil Armstrong',
            project_number='abc123',
            customer=self.customer
        )

        self.deliverable = Deliverable.objects.create(
            project=self.project,
            deliverable_name='Engine',
            deliverable_description='Rocket for stage 1'
        )

    # Tests for testing Project model ListView

    def test_project_listing(self):
        """ This method tests that the test project instance created
            in the  setUp method is correct
        """
        self.assertEqual(f'{self.project.project_name}', 'Moon Landing')
        self.assertEqual(f'{self.project.project_manager}', 'Neil Armstrong')
        self.assertEqual(f'{self.project.project_number}', 'abc123')

    def test_project_list_view_for_logged_in_user(self):
        """ This method tests that a logged in user can see the test project 
            instance created in the setUp method is displayed on the project 
            ListView, that Status Code '200 OK' is returned 
            (https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/200),
            and the html template project_list.html is used.
        """

        self.client.login(email='testuser@email.com',
                          password='testpass123')
        response = self.client.get(reverse('project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Moon Landing')
        self.assertTemplateUsed(response, 'projects/project_list.html')

    def test_project_list_view_for_logged_out_user(self):
        """ This method tests that a logged out user can't see the the project 
            ListView, and that Status Code '302 Found' is returned 
            (https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/302).
            The user should be retuned to the account_login page. Once logged in,
            the user should then be redirected to the project_list.html page
            .
        """

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

    # Tests for testing Project model DetailView

    def test_project_detail_view_for_logged_in_user(self):
        """ This method tests that a logged in user can see the the project 
            DetailView, Status Code '200 OK' is returned 
            (https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/302), 
            the Project created in the setUp method is displayed,
            and the html template project_detail.html is used.
        """

        self.client.login(email='testuser@email.com',
                          password='testpass123')
        response = self.client.get(self.project.get_absolute_url())
        no_response = self.client.get('/projects/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Moon Landing')
        self.assertContains(response, 'Neil Armstrong')
        self.assertContains(response, 'abc123')
        self.assertTemplateUsed(response, 'projects/project_detail.html')

    # Tests for testing Project model CreateView

    def test_project_create_view_for_logged_out_user(self):
        """ This method tests that a logged out user can't see the the project 
            CreateView, and that Status Code '302 Found' is returned 
            (https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/302).
            The user should be retuned to the account_login page. Once logged in,
            the user should then be redirected to the project_create.html page.
        """

        self.client.logout()
        url = reverse('project_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '%s?next=/projects/create/' % (
                (reverse('account_login')))
        )
        response = self.client.get(
            '%s?next=/projects/create/' % (reverse('account_login'))
        )
        self.assertContains(response, 'Log In')

    def test_project_create_view_for_logged_in_user(self):
        """ This method tests that a logged in user can see the the project 
            CreateView, a form is posted with new project details and 
            Status Code '302 Found' is returned 
            (https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/302), 
            a the user is redirected to the project_list.html page.
        """

        self.client.login(email='testuser@email.com',
                          password='testpass123')
        url = reverse('project_create')
        response = self.client.post(url, data={'customer': self.customer.id,
                                               'project_name': 'Mars Rover',
                                               'project_manager': 'Bill Murray',
                                               'project_number': 'abc567'}
                                    )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, (reverse('project_list')))

    # Tests for testing Project model UpdateView

    def test_project_update_view_for_logged_in_user(self):
        """ This method tests that a logged in user can see the the project 
            UpdateView. The project created in the setUp methed is updated 
            with new deails and Status Code '302 Found' is returned 
            (https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/302), 
            The project details are checked by refreshing the db
            the Project by going to the project_detail.html and 
            Status Code '200 OK' is retrued
        """

        self.client.login(email='testuser@email.com',
                          password='testpass123')
        url = reverse('project_update', args=[str(self.project.id)])
        response = self.client.post(url, data={'customer': self.customer.id,
                                               'project_name': 'Mars Lander',
                                               'project_manager': 'Bill Murray',
                                               'project_number': 'abc890'}
                                    )
        self.project.refresh_from_db(),
        self.assertEqual(self.project.project_name, 'Mars Lander')
        self.assertEqual(self.project.project_manager, 'Bill Murray')
        self.assertEqual(self.project.project_number, 'abc890')
        self.assertEqual(response.status_code, 302)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/project_update.html')

    # Tests for testing Project model DeleteView

    def test_project_delete_view_for_logged_in_user(self):
        """ This method tests that a logged in user can see the the project 
            DeleteView, and the project object created in the setUp method is delete, and 
            Status Code '302 Found' is returned 
            (https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/302). 
            The method tests that the object has been deleted by trying the 
            url and receiving a Status Code '404 Not Found'
            (https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404). 

        """

        self.client.login(email='testuser@email.com',
                          password='testpass123')
        url = reverse('project_delete', args=[str(self.project.id)])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Project.objects.filter(id=self.project.id).exists())

    def test_project_delete_view_for_logged_out_user(self):
        """ This method tests that a logged out user can't see the the project 
            DeleteView, and that Status Code '302 Found' is returned 
            (https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/302).
            The user should be redirected to the account_login page.
        """

        self.client.logout()
        url = reverse('project_delete', args=[str(self.project.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '%s?next=/projects/delete/%s' % (
                (reverse('account_login')), self.project.id)
        )
        response = self.client.get(
            '%s?next=/projects/delete/%s' % (reverse('account_login'),
                                             self.project.id)
        )
        self.assertContains(response, 'Log In')

    # Test Project Form
    def test_project_form_is_valid(self):
        """[summary]
        """
        form = ProjectForm(data={'customer': self.customer.id,
                                 'project_name': 'Mars Rover',
                                 'project_manager': 'Bill Murray',
                                 'project_number': 'abc567'})
        self.assertTrue(form.is_valid())
