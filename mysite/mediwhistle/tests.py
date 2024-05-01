from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import os

class HomePageTests(TestCase):
    def test_home_page_access(self):
        response = self.client.get(reverse('home'))  # Make sure 'home' is the correct name in your urls.py
        #self.assertEqual(response.status_code, 200)
        #self.assertContains(response, "Login With Google")

class DocumentUploadTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_document_upload(self):
        upload_file = SimpleUploadedFile("test_file.txt", b"abc", content_type="text/plain")
        response = self.client.post(reverse('upload'), {'upload': upload_file}, follow=True)
        self.assertRedirects(response, reverse('upload_success'))
        self.assertEqual(response.status_code, 200)

class GuestAccessUploadPageTest(TestCase):
    def test_access_upload_as_guest(self):
        # Simulate a guest user by not logging in or using an anonymous user
        response = self.client.get(reverse('upload'))
        self.assertEqual(response.status_code, 200)
        # Assert that the response contains the expected string for a guest user
        self.assertContains(response, "Welcome, you are logged in as a Guest")

class UploadWithoutFileTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    # def test_upload_without_file(self):
    #     response = self.client.post(reverse('upload'), {}, follow=True)
    #     self.assertFormError(response, 'form', 'upload', 'This field is required.')

class AdminAccessTest(TestCase):
    def setUp(self):
        admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'adminpassword')
        self.client.login(username='admin', password='adminpassword')

    def test_admin_access_to_uploaded_files(self):
        response = self.client.get(reverse('admin_document_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Subject")
        self.assertContains(response, "Uploaded at")
        self.assertContains(response, "Status")

class UploadSuccessMessageTest(TestCase):
    def test_upload_success_message_display(self):
        response = self.client.get(reverse('upload_success'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Submission Successful!")

class LogoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')
        self.client.login(username='user', password='pass')

    def test_logout_functionality(self):
        self.client.logout()
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, 'Logout')


class LogoutSessionClearanceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password')
        self.client.login(username='user', password='password')

    def test_logout_clears_session(self):
        self.client.logout()
        response = self.client.get(reverse('home'))
        self.assertNotIn('_auth_user_id', self.client.session.keys())

