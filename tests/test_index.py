from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from world_recipe.models import Recipe, UserProfile, Rating
from django.utils import timezone
from django.conf import settings
from world_recipe.views import index

class IndexViewTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            originID=1
        )
        
        # Create some test recipes
        self.recipe1 = Recipe.objects.create(
            title='Test Recipe 1',
            authorID=self.user,
            originID=1,
            meal_type='BF',
            ingredients='test ingredients',
            instructions='test instructions',
            publish_date=timezone.now()
        )
        
        self.recipe2 = Recipe.objects.create(
            title='Test Recipe 2',
            authorID=self.user,
            originID=2,
            meal_type='DN',
            ingredients='test ingredients 2',
            instructions='test instructions 2',
            publish_date=timezone.now()
        )
        r1 = Rating.objects.create(recipeID=self.recipe1, rating=4, userID=self.user)
        r2 = Rating.objects.create(recipeID=self.recipe1, rating=5, userID=self.user)
        r3 = Rating.objects.create(recipeID=self.recipe2, rating=3, userID=self.user)

        # initialize the test client
        self.client = Client()
    
    def test_view_exists(self):
        """
        does the index() view exist in the world_recipe app's views.py module?
        """
        is_callable = callable(index)
        self.assertTrue(is_callable, "the index() view for world_recipe does not exist ")

    def test_index_view_status(self):
        # test that the index page loads successfully
        response = self.client.get(reverse('world_recipe:index'))
        self.assertEqual(response.status_code, 200)
        
    def test_index_view_template(self):
        # test that the correct template is used
        response = self.client.get(reverse('world_recipe:index'))
        self.assertTemplateUsed(response, 'world_recipe/index.html')
        
    def test_index_view_context(self):
        # test that the context contains the expected data
        response = self.client.get(reverse('world_recipe:index'))
        self.assertTrue('most_recent_recipes' in response.context)
        self.assertTrue('most_rated_recipes' in response.context)
        self.assertTrue('google_maps_api_key' in response.context)
        self.assertTrue('all_recipes' in response.context)
        
    def test_recipes_in_context(self):
        # Test that the recipes are present in the context
        response = self.client.get(reverse('world_recipe:index'))
        self.assertIn(self.recipe1, response.context['all_recipes'])
        self.assertIn(self.recipe2, response.context['all_recipes'])
        
    def test_recent_recipes_order(self):
        # test that recent recipes are ordered by publish date
        response = self.client.get(reverse('world_recipe:index'))
        recent_recipes = response.context['most_recent_recipes']
        self.assertGreaterEqual(len(recent_recipes), 2)
        # check that recipes are ordered by publish date (newest first)
        self.assertGreaterEqual(recent_recipes[0].publish_date, recent_recipes[1].publish_date)

    


    def test_recipe_titles_in_context(self):
        """check if recipe titles are correctly displayed in the index page content """
        response = self.client.get(reverse('world_recipe:index'))
        content = response.content.decode()  

        self.assertIn(self.recipe1.title, content, "Index page does not contain the title '%s'." % self.recipe1.title)
        self.assertIn(self.recipe2.title, content, "Index page does not contain the title '%s'." % self.recipe2.title)
            
    def test_rated_recipes_order(self):
        # Test that rated recipes are ordered by rating value
        response = self.client.get(reverse('world_recipe:index'))
        rated_recipes = response.context['most_rated_recipes']
        self.assertGreaterEqual(len(rated_recipes), 2)
        # check that recipes are ordered by rating value (highest rating first)
        # avg_rating is passed
        self.assertGreaterEqual(rated_recipes[0].avg_rating, rated_recipes[1].avg_rating)


    def test_index_view_contains_map_script(self):
        # test that the index page contains the google maps script
        response = self.client.get(reverse('world_recipe:index'))
        content = response.content.decode('utf-8')
        
        self.assertIn('<div id="recipe-map"', content)
        
        google_maps_api_key = settings.GOOGLE_MAPS_API_KEY
        self.assertIn(f'https://maps.googleapis.com/maps/api/js?key={google_maps_api_key}&callback=initMap', content)



    def test_recipe_ratings_in_context(self):
        # test that the ratings for the recipes are correctly displayed in the context
        response = self.client.get(reverse('world_recipe:index'))
        self.assertContains(response, self.recipe1.average_rating())
        self.assertContains(response, self.recipe2.average_rating())
        

    def test_for_about_hyperlink(self):
        #about hyperlink in the index page
        response = self.client.get(reverse('world_recipe:index'))

        # check for the correct 'about' link (without worrying about quotes)
        about_link_single = "<a href='/world-recipe/about/'>About</a>" in response.content.decode()
        about_link_double = '<a href="/world-recipe/about/">About</a>' in response.content.decode()

        # assert that the About link is present
        self.assertTrue(about_link_single or about_link_double, "We couldn't find the hyperlink to the /world-recipe/about/ URL in your index page check that it appears EXACTLY as in the book ")
    
    
    def test_for_register_hyperlink(self):
        """
        Does the response contain the 'register' hyperlink in the index page?
        """
        response = self.client.get(reverse('world_recipe:index'))
        
        # check if the 'Register' link exists in the page
        register_link_single = '<a href="/world-recipe/register/">Register</a>' in response.content.decode()
        register_link_double = '<a href="/world-recipe/register/" class="register-link">Register</a>' in response.content.decode()
        
        self.assertTrue(register_link_single or register_link_double, 
                        "we couldn't find the hyperlink to the /world-recipe/register/ URL in your index page. Check that it appears EXACTLY as in the index template ")
    
    def test_for_login_hyperlink(self):
        """
        Does the response contain the 'login' hyperlink in the index page?
        """
        response = self.client.get(reverse('world_recipe:index'))
        
        # check if the 'Login' link exists in the page
        login_link_single = '<a href="/world-recipe/login/">Login</a>' in response.content.decode()
        login_link_double = '<a href="/world-recipe/login/" class="login-link">Login</a>' in response.content.decode()
        
        self.assertTrue(login_link_single or login_link_double, 
                        "we couldn't find the hyperlink to the /world-recipe/login/ URL in your index page. Check that it appears EXACTLY as in the index template ")
        

    def test_index_starts_with_doctype(self):
        response = self.client.get(reverse('world_recipe:index'))
        self.assertTrue(response.content.decode().startswith('<!DOCTYPE html>'), "your index.html does not start with <!DOCTYPE html>")

