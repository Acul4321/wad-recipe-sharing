from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from world_recipe.models import Recipe, UserProfile
from django.utils import timezone

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
        
        # Initialize the test client
        self.client = Client()

    def test_index_view_status(self):
        # Test that the index page loads successfully
        response = self.client.get(reverse('world_recipe:index'))
        self.assertEqual(response.status_code, 200)
        
    def test_index_view_template(self):
        # Test that the correct template is used
        response = self.client.get(reverse('world_recipe:index'))
        self.assertTemplateUsed(response, 'world_recipe/index.html')
        
    def test_index_view_context(self):
        # Test that the context contains the expected data
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
        # Test that recent recipes are ordered by publish date
        response = self.client.get(reverse('world_recipe:index'))
        recent_recipes = response.context['most_recent_recipes']
        self.assertGreaterEqual(len(recent_recipes), 2)
        # Check that recipes are ordered by publish date (newest first)
        self.assertGreaterEqual(recent_recipes[0].publish_date, recent_recipes[1].publish_date)
