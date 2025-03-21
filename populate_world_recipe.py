import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wad_recipe_sharing.settings')

import django
django.setup()

from django.core.files import File
from django.contrib.auth.models import User
from world_recipe.models import Recipe, Rating, UserProfile
from utils import COUNTRIES
import random
from datetime import datetime, timedelta

def create_user(username, password, origin_id):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user, originID=origin_id)
    return user

def add_recipe(title, author, origin_id, meal_type, ingredients, instructions, image_name=None):
    recipe = Recipe.objects.get_or_create(
        title=title,
        authorID=author,
        originID=origin_id,
        meal_type=meal_type,
        ingredients=ingredients,
        instructions=instructions
    )[0]
    
    if image_name:
        image_path = os.path.join('population_images', image_name)
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                recipe.image.save(image_name, File(f), save=True)
    
    return recipe

def add_ratings(recipe, num_ratings):
    users = list(User.objects.all())
    if len(users) < num_ratings:
        return
    
    # Get random users for ratings
    rating_users = random.sample(users, num_ratings)
    
    for user in rating_users:
        Rating.objects.get_or_create(
            recipeID=recipe,
            userID=user,
            rating=random.randint(1, 5)
        )

def populate():
    # Create test users
    users = [
        {'username': 'john_doe', 'password': 'testpass123', 'origin': 168},  # UK
        {'username': 'alice_smith', 'password': 'testpass123', 'origin': 169},  # USA
        {'username': 'mario_rossi', 'password': 'testpass123', 'origin': 76},  # Italy
    ]
    
    created_users = []
    for user_data in users:
        user = create_user(user_data['username'], user_data['password'], user_data['origin'])
        created_users.append(user)

    # Recipe data
    recipes = [
        {
            'title': 'Classic Spaghetti Carbonara',
            'author': created_users[2],  # mario_rossi
            'origin_id': 76,  # Italy
            'meal_type': 'DN',  # Dinner
            'ingredients': '400g spaghetti\n200g guanciale\n4 egg yolks\n100g pecorino romano\nBlack pepper',
            'instructions': '1. Cook pasta\n2. Fry guanciale\n3. Mix eggs and cheese\n4. Combine all ingredients',
            'image': 'carbonara.jpg',
            'num_ratings': 5
        },
        {
            'title': 'English Breakfast',
            'author': created_users[0],  # john_doe
            'origin_id': 168,  # UK
            'meal_type': 'BF',  # Breakfast
            'ingredients': 'Eggs\nBacon\nSausages\nBeans\nMushrooms\nTomatoes\nToast',
            'instructions': '1. Fry bacon and sausages\n2. Cook eggs\n3. Heat beans\n4. Serve hot',
            'image': 'english_breakfast.jpg',
            'num_ratings': 3
        },
        {
            'title': 'American Burger',
            'author': created_users[1],  # alice_smith
            'origin_id': 169,  # USA
            'meal_type': 'LU',  # Lunch
            'ingredients': 'Beef patty\nBurger buns\nLettuce\nTomato\nCheese\nOnion',
            'instructions': '1. Grill the patty\n2. Toast the buns\n3. Assemble burger\n4. Add condiments',
            'image': 'burger.jpg',
            'num_ratings': 4
        }
    ]

    # Create recipes and their ratings
    for recipe_data in recipes:
        recipe = add_recipe(
            title=recipe_data['title'],
            author=recipe_data['author'],
            origin_id=recipe_data['origin_id'],
            meal_type=recipe_data['meal_type'],
            ingredients=recipe_data['ingredients'],
            instructions=recipe_data['instructions'],
            image_name=recipe_data['image']
        )
        add_ratings(recipe, recipe_data['num_ratings'])

if __name__ == '__main__':
    print('Starting World Recipe population script...')
    populate()
    print('Population complete!')
