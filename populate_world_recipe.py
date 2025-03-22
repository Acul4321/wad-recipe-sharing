import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wad_recipe_sharing.settings')

import django
django.setup()


import random
from django.contrib.auth.models import User
from django.utils import timezone
from world_recipe.models import UserProfile, Recipe, Rating


# Function to create a user and profile
def create_user(username, email, password, originID):
    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()

    profile = UserProfile.objects.create(
        user=user,
        originID=originID,
        profile_picture='profile_pictures/default.jpg',
        description="Description for %s" % username
    )
    profile.save()

    print("Created User: %s" % user.username)
    return user

# Function to create a recipe
def create_recipe(author, originID, meal_type, title, ingredients, instructions, image):
    recipe = Recipe.objects.create(
        authorID=author,
        originID=originID,
        meal_type=meal_type,
        title=title,
        ingredients=ingredients,
        instructions=instructions,
        publish_date=timezone.now(),
        image=image
    )
    recipe.save()

    print("Created Recipe: %s by %s" % (recipe.title, author.username))
    return recipe

# Function to create a rating
def create_rating(user, recipe, rating_value):
    rating = Rating.objects.create(
        userID=user,
        recipeID=recipe,
        rating=rating_value
    )
    rating.save()

    print("Added Rating: %s for %s by %s" % (rating.rating, recipe.title, user.username))
    return rating

# Function to add multiple ratings to a recipe
def add_ratings(recipe, users):
    for _ in range(2):  # Each recipe gets 2 ratings
        user = random.choice(users)  # Pick a random user
        rating_value = random.randint(1, 5)  # Assign random rating (1-5)
        create_rating(user, recipe, rating_value)

# Population function
def populate():
    # Create sample users
    users_data = [
        {'username': 'user1', 'email': 'user1@gmail.com', 'password': 'password1', 'originID': 1},
        {'username': 'user2', 'email': 'user2@gmail.com', 'password': 'password2', 'originID': 2},
        {'username': 'user3', 'email': 'user3@gmail.com', 'password': 'password3', 'originID': 3}
    ]

    users = []
    for user_data in users_data:
        users.append(create_user(user_data['username'], user_data['email'], user_data['password'], user_data['originID']))

    # Sample Recipe Data (6 recipes)
    recipes_data = [
    {'author': users[0], 'originID': 16, 'meal_type': 'BF', 'title': 'Belgian Waffles', 
     'ingredients': 'Flour, Eggs, Sugar, Butter, Milk, Yeast', 
     'instructions': 'Mix ingredients, let batter rise, cook in waffle iron.', 
     'image': 'recipe_images/belgian_waffles.jpg'},

    {'author': users[1], 'originID': 102, 'meal_type': 'SN', 'title': 'Empanadas', 
     'ingredients': 'Flour, Ground Beef, Onion, Garlic, Spices', 
     'instructions': 'Fill dough with meat mixture, fold, and fry.', 
     'image': 'recipe_images/empanadas.jpg'},

    {'author': users[2], 'originID': 23, 'meal_type': 'DN', 'title': 'Feijoada', 
     'ingredients': 'Black Beans, Pork, Beef, Onion, Garlic, Spices', 
     'instructions': 'Slow cook beans and meat with spices.', 
     'image': 'recipe_images/feijoada.jpg'},

    {'author': users[0], 'originID': 30, 'meal_type': 'LU', 'title': 'Poutine', 
     'ingredients': 'French Fries, Cheese Curds, Gravy', 
     'instructions': 'Layer fries with cheese curds and pour gravy over.', 
     'image': 'recipe_images/poutine.jpg'},

    {'author': users[1], 'originID': 30, 'meal_type': 'DN', 'title': 'Maple Glazed Salmon', 
     'ingredients': 'Salmon, Maple Syrup, Soy Sauce, Garlic', 
     'instructions': 'Marinate salmon in sauce and bake.', 
     'image': 'recipe_images/maple_glazed_salmon.jpg'},

    {'author': users[2], 'originID': 147, 'meal_type': 'DN', 'title': 'Spaghetti Carbonara', 
     'ingredients': 'Spaghetti, Eggs, Parmesan, Pancetta, Black Pepper', 
     'instructions': 'Cook spaghetti, mix with eggs and pancetta.', 
     'image': 'recipe_images/spaghetti_carbonara.jpg'},

    {'author': users[1], 'originID': 147, 'meal_type': 'BF', 'title': 'Cornetto', 
     'ingredients': 'Flour, Sugar, Butter, Yeast, Milk', 
     'instructions': 'Bake crescent-shaped pastries.', 
     'image': 'recipe_images/cornetto.jpg'}
]
    
    recipes = []
    for recipe_data in recipes_data:
        recipes.append(create_recipe(**recipe_data))

    # Add ratings for each recipe
    for recipe in recipes:
        add_ratings(recipe, users)

if __name__ == '__main__':
    print("Starting world_recipe population script...")
    populate()