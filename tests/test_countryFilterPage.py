from django.test import TestCase, Client
from django.urls import reverse
from world_recipe.models import Recipe
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from django.utils import timezone
from world_recipe.models import UserProfile
from unittest.mock import patch


class AjaxFilterTests(TestCase):
    def setUp(self):
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
            title="Bibimbap",
            meal_type="LU",  # Lunch
            originID=1,  # South Korea
            authorID=self.user,
            ingredients="Rice, Vegetables",
            instructions="Mix together",
            publish_date=timezone.now()
        )
        self.recipe2 = Recipe.objects.create(
            title="Tteokbokki",
            meal_type="SN",  # Snack
            originID=1,  # South Korea
            authorID=self.user,
            ingredients="Rice Cakes, Spicy Sauce",
            instructions="Cook and mix",
            publish_date=timezone.now()
        )
        self.recipe3 = Recipe.objects.create(
            title="Kimchi Fried Rice",
            meal_type="LU",  # Lunch
            originID=1,  # South Korea
            authorID=self.user,
            ingredients="Kimchi, Rice, Egg",
            instructions="Stir-fry everything",
            publish_date=timezone.now()
        )
        self.country_url = reverse("world_recipe:country", kwargs={"country": "south-korea"})
        # initialize the test client
        self.client = Client()
        
    def test_country_filter(self):
        # test that the country filter page loads successfully
        response = self.client.get(reverse('world_recipe:country', kwargs={'country': 'india'}))
        self.assertEqual(response.status_code, 200)
        
    def test_country_filter_template(self):
        # test that the country filter page uses the correct template
        response = self.client.get(reverse('world_recipe:country', kwargs={'country': 'india'}))
        self.assertTemplateUsed(response, 'world_recipe/country.html')
        




