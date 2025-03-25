from django.test import TestCase
from django.conf import settings
import os



class StaticMediaTemplatesTests(TestCase):
    def setUp(self):
        self.project_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.template_dir = os.path.join(self.project_base_dir, 'templates')
        self.static_dir = os.path.join(self.project_base_dir, 'static')
        self.media_dir = os.path.join(self.project_base_dir, 'media')


    def test_template_dir(self):
        # test that the template directory is set correctly
        self.assertEqual(settings.TEMPLATE_DIR, self.template_dir)
    
    def test_static_dir(self):
        # test that the static directory is set correctly
        self.assertEqual(settings.STATIC_DIR, self.static_dir)
    


    def test_static_directory_exists(self):
        """check if the static directory exists."""
        self.assertTrue(os.path.isdir(self.static_dir), "Static directory does not exist!")

        does_images_static_dir_exist = os.path.isdir(os.path.join(self.static_dir, 'images'))
        does_rango_jpg_exist = os.path.isfile(os.path.join(self.static_dir, 'images', 'default.png'))
        self.assertTrue(does_images_static_dir_exist, "The images subdirectory was not found in your static directory")
        self.assertTrue(does_rango_jpg_exist, "We couldn't locate the default.jpg image in the /static/images/ directory")
    

    def test_media_directory_exists(self):
        """Check if the media directory, profile_pictures, and recipe_images exist."""
        self.assertTrue(os.path.isdir(self.media_dir), "Media directory does not exist!")
        self.profile_pictures_dir = os.path.join(self.media_dir, 'profile_pictures')
        self.recipe_images_dir = os.path.join(self.media_dir, 'recipe_images')
        self.assertTrue(os.path.isdir(self.profile_pictures_dir), "profile_pictures subdirectory was not found in media directory.")
        self.assertTrue(os.path.isdir(self.recipe_images_dir), "recipe_images subdirectory was not found in media directory.")


    def test_template_directory_exists(self):
        self.assertTrue(os.path.isdir(self.template_dir), "Template directory does not exist!")
    


    



    