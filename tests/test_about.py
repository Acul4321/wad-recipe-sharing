from django.test import TestCase
from django.urls import reverse

class AboutPageTests(TestCase):
    def test_about_page_status(self):
        response = self.client.get(reverse('world_recipe:about'))
        self.assertEqual(response.status_code, 200)
        
    def test_about_page_template(self):
        response = self.client.get(reverse('world_recipe:about'))
        self.assertTemplateUsed(response, 'world_recipe/about.html')

    def test_about_page_content(self):
        response = self.client.get(reverse('world_recipe:about'))
        self.assertContains(response, 'About World Recipes')