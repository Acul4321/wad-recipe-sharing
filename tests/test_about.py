from django.test import TestCase
from django.urls import reverse

class AboutPageTests(TestCase):
    def test_about_page_status_code(self):
        response = self.client.get(reverse('world_recipe:about'))  # ✅ Use reverse()
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_by_name(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
    
    def test_about_page_loads(self):
        response = self.client.get(reverse('world_recipe:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "About World Recipe")  # Adjust to match actual content