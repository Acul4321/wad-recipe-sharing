from django.test import TestCase
from django.contrib.auth.models import User
from world_recipe.models import UserProfile, Recipe
def setUp(self):
        """Create a test user for the recipes."""
        self.user = User.objects.create_user(username="testuser", password="testpassword")



def test_slug_creation(self):
    #checks to make sure that when a recipe is created, an appropriate slug is created
    recipe = Recipe(
            authorID=self.user,
            originID=1,
            meal_type="DN",
            title="Random slug test"
        )
    recipe.save() 
    self.assertEqual(recipe.slug, "random-slug-test-testuser")
    

def test_slug_uniqueness(self):
        """Ensure slug is unique when duplicate titles exist."""
        recipe1 = Recipe(authorID=self.user, originID=1, meal_type="DN", title="Kimchi Stew")
        recipe1.save()
        
        recipe2 = Recipe(authorID=self.user, originID=1, meal_type="DN", title="Kimchi Stew")
        recipe2.save()
        
        self.assertNotEqual(recipe1.slug, recipe2.slug)
        self.assertEqual(recipe2.slug, "kimchi-stew-testuser-1")

