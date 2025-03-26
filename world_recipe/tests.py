from django.test import TestCase
from django.contrib.auth.models import User
from world_recipe.models import UserProfile, Recipe
def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")



def test_slug_creation(self):
    
    recipe = Recipe(
            authorID=self.user,
            originID=1,
            meal_type="DN",
            title="Random slug test"
        )
    recipe.save() 
    self.assertEqual(recipe.slug, "random-slug-test-testuser")
    

def test_slug_uniqueness(self):
        recipe1 = Recipe(authorID=self.user, originID=1, meal_type="DN", title="Kimchi Stew")
        recipe1.save()
        
        recipe2 = Recipe(authorID=self.user, originID=1, meal_type="DN", title="Kimchi Stew")
        recipe2.save()
        
        self.assertNotEqual(recipe1.slug, recipe2.slug)
        self.assertEqual(recipe2.slug, "kimchi-stew-testuser-1")

