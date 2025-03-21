import os
import django
from datetime import datetime
from django.utils import timezone
from django.db.models import Avg
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'wad_recipe_sharing.settings')
django.setup()
from world_recipe.models import Recipe, Rating
from world_recipe.utils import COUNTRIES

def populate():
    recipes = [
        {'name': 'Empanadas', 'regionID': 1, 'meal_type': 'Snack',
         'ingredients': ['Dough', 'Beef', 'Onion', 'Egg'],
         'instructions': [
             '1. Prepare the beef filling by sautéing the onion and beef together.',
             '2. Roll out the dough and cut it into circles.',
             '3. Place a spoonful of the filling onto the dough circle.',
             '4. Fold the dough over and crimp the edges to seal.',
             '5. Bake at 375°F (190°C) until golden brown and crispy.'
         ], 'publish_date': timezone.now(), 'image': 'recipe_images/empanadas.jpg'},

        {'name': 'Vegemite Toast', 'regionID': 2, 'meal_type': 'Breakfast',
         'ingredients': ['Bread', 'Butter', 'Vegemite'],
         'instructions': [
             '1. Toast the bread until golden brown.',
             '2. Spread a thin layer of butter on the toast.',
             '3. Spread Vegemite over the buttered toast.',
             '4. Serve with a hot beverage like tea or coffee.'
         ], 'publish_date': timezone.now(), 'image': 'recipe_images/vegemite_toast.jpg'},

        {'name': 'Belgian Waffles', 'regionID': 3, 'meal_type': 'Breakfast',
         'ingredients': ['Flour', 'Eggs', 'Milk', 'Sugar'],
         'instructions': [
             '1. Mix the flour, sugar, and eggs in a bowl.',
             '2. Add milk and stir until the batter is smooth.',
             '3. Preheat the waffle iron and lightly grease it.',
             '4. Pour batter into the waffle iron and cook until golden brown.',
             '5. Serve with toppings like syrup, whipped cream, or fresh berries.'
         ], 'publish_date': timezone.now(), 'image': 'recipe_images/belgian_waffles.jpg'},

        {'name': 'Feijoada', 'regionID': 4, 'meal_type': 'Lunch',
         'ingredients': ['Black beans', 'Chicken', 'Rice', 'Oranges'],
         'instructions': [
             '1. Cook the black beans in water until tender.',
             '2. Add chicken pieces and cook until fully done.',
             '3. Serve the beans and chicken over cooked rice.',
             '4. Garnish with fresh orange slices for a citrusy kick.'
         ], 'publish_date': timezone.now(), 'image': 'recipe_images/feijoada.jpg'},

        {'name': 'Poutine', 'regionID': 5, 'meal_type': 'Dinner',
         'ingredients': ['Fries', 'Cheese curds', 'Gravy'],
         'instructions': [
             '1. Fry the potatoes to make crispy fries.',
             '2. Melt cheese curds on top of the hot fries.',
             '3. Pour hot gravy over the fries and cheese curds.',
             '4. Serve immediately while hot and crispy.'
         ], 'publish_date': timezone.now(), 'image': 'recipe_images/poutine.jpg'},

        {'name': 'Spaghetti Carbonara', 'regionID': 14, 'meal_type': 'Dinner',
         'ingredients': ['Spaghetti', 'Bacon', 'Eggs', 'Parmesan cheese', 'Black pepper'],
         'instructions': [
             '1. Cook the spaghetti in salted boiling water according to package instructions.',
             '2. While the pasta is cooking, fry the bacon until crispy.',
             '3. In a bowl, whisk together the eggs, grated Parmesan cheese, and black pepper.',
             '4. Drain the pasta, reserving a bit of pasta water.',
             '5. Combine the hot pasta with the bacon and egg mixture, tossing until creamy.',
             '6. If the sauce is too thick, add some reserved pasta water to thin it.'
         ], 'publish_date': timezone.now(), 'image': 'recipe_images/spaghetti_carbonara.jpg'}
    ]

    for recipe_data in recipes:
        recipe = add_recipe(recipe_data['name'], recipe_data['regionID'], recipe_data['meal_type'],
                            recipe_data['ingredients'], recipe_data['instructions'], recipe_data['publish_date'], recipe_data['image'])
        for i in range(random.randint(3,7)):
            add_rating(recipe, random.randint(1, 5))
    
for recipe in Recipe.objects.all():
        ratings = Rating.objects.filter(recipe=recipe)
        print(f'{recipe.name} from {recipe.get_country_name()}')
    
    
def add_recipe(name, regionID, meal_type, ingredients, instructions, publish_date, image):
    recipe, created = Recipe.objects.get_or_create(
        name=name, 
        regionID=regionID,
        defaults={ 
            'meal_type': meal_type,
            'ingredients': ingredients,  
            'instructions': instructions, 
            'publish_date': publish_date
        }
    )
    if not created:  
        recipe.meal_type = meal_type
        recipe.ingredients = ingredients
        recipe.instructions = instructions
        recipe.publish_date = publish_date
        recipe.image = image

        recipe.save()

    return recipe



def add_rating(recipe, rating):
    Rating.objects.create(recipe=recipe, rating=rating)


if __name__ == '__main__':
    print('Starting World Recipe population script...')
    populate()