from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from world_recipe.models import UserProfile
import world_recipe
from world_recipe.forms import UserProfileForm
from world_recipe import forms
from django.conf import settings
from django.contrib import admin
from django.forms import fields as django_fields

class AuthLoginAndRegisterTests(TestCase):
    def setUp(self):
        user, created = User.objects.get_or_create(
            username='testuser', 
            first_name='Test',
            last_name='User',
            email='test@test.com',
        )
        if created:
            user.set_password('testpass123')
            user.save()
        self.superuser = User.objects.create_superuser(username='admin', email='admin@test.com', password='testpassword')
        self.client = Client()

    def test_installed_apps(self):
        self.assertTrue('django.contrib.auth' in settings.INSTALLED_APPS)

    def test_userprofile_class(self):
        self.assertTrue('UserProfile' in dir(world_recipe.models))


    def test_model_in_admin(self):
        super_user = self.superuser
        self.client.login(username='admin', password='testpassword')
       
        response = self.client.get('/admin/world_recipe/userprofile/')
        self.assertEqual(response.status_code, 200)

    def test_user_profile_form(self):
        self.assertTrue('UserProfileForm' in dir(world_recipe.forms))
        user_profile_form = forms.UserProfileForm()
        self.assertEqual(type(user_profile_form.__dict__['instance']), world_recipe.models.UserProfile)
        fields = user_profile_form.fields
        expected_fields = {'originID': django_fields.ChoiceField}
        for field_name in expected_fields:
            expected_field = expected_fields[field_name]
            self.assertTrue(field_name in fields.keys())
            self.assertEqual(expected_field, type(fields[field_name]),"field is not of the correct type")

#registration
    def test_register_page_status(self):
        response = self.client.get(reverse('world_recipe:register'))
        self.assertEqual(response.status_code, 200)

    def test_new_regi_view_exists(self):
        url = ''
        try:
            url = reverse('world_recipe:register')
        except:
            pass
        self.assertEqual(url, '/world-recipe/register/')

    
    def test_bad_regi_post_response(self):
        # Simulate valid data
        form_data = {
            'username': 'new_user',
            'password': 'password123',
            'confirm_password': 'password123',
            'originID': '1',  # assuming '1' is a valid country ID
        }
        form = UserProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        # Simulate password mismatch
        form_data = {
            'username': 'new_user',
            'password': 'password123',
            'confirm_password': 'password124',  # mismatched password
            'originID': '1',
        }
        form = UserProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'confirm_password', 'Passwords do not match')

    def test_username_with_spaces(self):
        # Simulate username with spaces
        form_data = {
            'username': 'new user',
            'password': 'password123',
            'confirm_password': 'password123',
            'originID': '1',
        }
        form = UserProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'username', 'Username cannot contain spaces')

    def test_invalid_username_characters(self):
        # Simulate invalid characters in username
        form_data = {
            'username': 'new$user',
            'password': 'password123',
            'confirm_password': 'password123',
            'originID': '1',
        }
        form = UserProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'username', 'Username can only contain letters, numbers, underscore, hyphen, and period')

    def test_existing_username(self):
        # Simulate existing username
        User.objects.create_user(username='existing_user', password='password123')
        form_data = {
            'username': 'existing_user',
            'password': 'password123',
            'confirm_password': 'password123',
            'originID': '1',
        }
        form = UserProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'username', 'This username is already taken')


#login
    def test_login_page_status(self):
            response = self.client.get(reverse('world_recipe:login'))
            self.assertEqual(response.status_code, 200)


    
    # def test_login_required_for_favorite(self):
    #     response = self.client.get(reverse('world_recipe:favorite'))
    #     self.assertEqual(response.status_code, 302)


