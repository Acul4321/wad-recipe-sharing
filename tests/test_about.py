from django.test import TestCase
from django.urls import reverse
from world_recipe import views

class AboutPageTests(TestCase):
    def test_about_page_status(self):
        response = self.client.get(reverse('world_recipe:about'))
        self.assertEqual(response.status_code, 200)
        
    def test_about_page_template(self):
        response = self.client.get(reverse('world_recipe:about'))
        self.assertTemplateUsed(response, 'world_recipe/about.html')

    def test_about_page_content(self):
        response = self.client.get(reverse('world_recipe:about'))
        content = response.content.decode()
        self.assertIn('About World Recipes', content, "about page doesnt contain about world recipes")
    

    def test_view_exists(self):
        """
        Does the about() view exist in your app's views.py module and is it callable?
        """
        is_callable = callable(getattr(views, 'about'))  # checks if 'about' is callable
        
        self.assertTrue(is_callable, "Check you have defined your about() view correctly. We can't execute it.")

    def test_for_index_hyperlink(self):
        #checks for links in the about page
        response = self.client.get(reverse('world_recipe:about'))  # Replace with actual URL name for your about page
        
        single_quotes_check = '<a href=\'/world-recipe/\'>Home</a>' in response.content.decode()
        double_quotes_check = '<a href="/world-recipe/">Home</a>' in response.content.decode()

        self.assertTrue(single_quotes_check or double_quotes_check,
                        "we could not find a hyperlink back to the index page in your about view ")