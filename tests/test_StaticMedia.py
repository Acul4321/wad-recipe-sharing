from django.test import TestCase
from django.conf import settings
import os
from dotenv import load_dotenv
from world_recipe.models import UserProfile, Recipe
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse



class StaticMediaTemplatesTests(TestCase):
    def setUp(self):
        
        self.project_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.template_dir = os.path.join(self.project_base_dir, 'templates')
        self.static_dir = os.path.join(self.project_base_dir, 'static')
        self.media_dir = os.path.join(self.project_base_dir, 'media')

        load_dotenv()

    def test_template_dir(self):
        # test that the template directory is set correctly
        self.assertEqual(settings.TEMPLATE_DIR, self.template_dir)
    
    def test_static_dir(self):
        # test that the static directory is set correctly
        self.assertEqual(settings.STATIC_DIR, self.static_dir)
    


    def test_static_directory_exists(self):
        """check if the static directory exists."""
        self.assertTrue(os.path.isdir(self.static_dir), "Staic directory does not exist!")

        does_images_static_dir_exist = os.path.isdir(os.path.join(self.static_dir, 'images'))
        does_default_jpg_exist = os.path.isfile(os.path.join(self.static_dir, 'images', 'default.png'))
        self.assertTrue(does_images_static_dir_exist, "The images subdirectory was not found in your static directory")
        self.assertTrue(does_default_jpg_exist, "We couldn't locate the default.jpg image in the /static/images/ directory")
    

    def test_media_directory_exists(self):
        """Check if the media directory, profile_pictures, and recipe_images exist."""
        self.assertTrue(os.path.isdir(self.media_dir), "Media directory does not existt")
        self.profile_pictures_dir = os.path.join(self.media_dir, 'profile_pictures')
        self.recipe_images_dir = os.path.join(self.media_dir, 'recipe_images')
        self.assertTrue(os.path.isdir(self.profile_pictures_dir), "profile_pictures subdirectory was not found in media directory ")
        self.assertTrue(os.path.isdir(self.recipe_images_dir), "recipe_images subdirectory was not found in media directory ")


    def test_template_directory_exists(self):
        self.assertTrue(os.path.isdir(self.template_dir), "template directory does not exist ")
    
    def test_template_files_exist(self):
        """Check that the required templates exist."""
        index_template = os.path.join(self.template_dir, 'world_recipe/index.html')
        about_template = os.path.join(self.template_dir, 'world_recipe/about.html')
        self.assertTrue(os.path.isfile(index_template), "index.html template was not found in the templates directory ")
        self.assertTrue(os.path.isfile(about_template), "about.html template was not found in the templates directory ")



    def test_static_media_config(self):
        static_dir_exists = 'STATIC_DIR' in dir(settings)
        self.assertTrue(static_dir_exists, "your settings.py module does not have the variable STATIC_DIR defined")

        static_path = os.path.normpath(settings.STATIC_DIR)
        expected_static_path = os.path.normpath(self.static_dir)
        self.assertEqual(expected_static_path, static_path, "the value of STATIC_DIR does not equal the expected path It should point to your project root with 'static' appended")

        staticfiles_dirs_exists = 'STATICFILES_DIRS' in dir(settings)
        self.assertTrue(staticfiles_dirs_exists, "the required setting STATICFILES_DIRS is not present in your project's settings.py module ")
        self.assertTrue(isinstance(settings.STATICFILES_DIRS, list), "STATICFILES_DIRS should be a list")

        static_url_exists = 'STATIC_URL' in dir(settings)
        static_url_value = settings.STATIC_URL
        self.assertTrue(static_url_exists, "the STATIC_URL variable has not been defined in settings.py.")
        self.assertEqual(static_url_value, '/static/', "STATIC_URL should be set to '/static/'")

        #media parts
        media_dir_exists = 'MEDIA_DIR' in dir(settings)
        self.assertTrue(media_dir_exists, "the MEDIA_DIR variable in settings.py has not been defined ")

        media_path = os.path.normpath(settings.MEDIA_DIR)
        expected_media_path = os.path.normpath(self.media_dir)
        self.assertEqual(expected_media_path, media_path, "the MEDIA_DIR setting does not point to the correct path ")

        media_root_exists = 'MEDIA_ROOT' in dir(settings)
        self.assertTrue(media_root_exists, "the MEDIA_ROOT setting has not been defined ")

        media_root_path = os.path.normpath(settings.MEDIA_ROOT)
        self.assertEqual(expected_media_path, media_root_path, "the value of MEDIA_ROOT does not equal the value of MEDIA_DIR ")
        media_url_exists = 'MEDIA_URL' in dir(settings)
        self.assertTrue(media_url_exists, "the setting MEDIA_URL has not been defined in settings.py ")
        media_url_value = settings.MEDIA_URL
        self.assertEqual(media_url_value, '/media/', "MEDIA_URL should be set to '/media/'")


    
    def test_recipe_list_displays_images(self):
        index_template = os.path.join(self.template_dir, 'world_recipe/includes/recipe_list.html')
        with open(index_template, 'r') as file:
            content = file.read()
            self.assertTrue('<img' in content, "the recipe list does not display images")


    def test_secret_key_loaded_from_env(self):
        self.assertTrue(hasattr(settings, 'SECRET_KEY'), "SECRET_KEY is not set in Django settings")
        secret_key_from_env = os.getenv('DJANGO_SECRET_KEY')
        self.assertIsNotNone(secret_key_from_env, "The SECRET_KEY variable was not found in the .env file")

    