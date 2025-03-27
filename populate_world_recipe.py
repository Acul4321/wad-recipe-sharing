import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wad_recipe_sharing.settings')

import django
django.setup()


import random
from django.contrib.auth.models import User
from django.utils import timezone
from world_recipe.models import UserProfile, Recipe, Rating, Comment, Favorite


# function to create a user and profile
def create_user(username, email, password, originID, image):
    user, created = User.objects.get_or_create(username=username, email=email)
    if created:
        user.set_password(password)
        user.save()


        profile = UserProfile.objects.create(
            user=user,
            originID=originID,
            profile_picture=image,
            description="Description for %s: Here are my recipes, please gie=ve it a like and comment!" % username
        )
        profile.save()

        print("Created User: %s" % user.username)
    else:
        print("User already exists: %s" % user.username)
    return user

# function to create a recipe
def create_recipe(author, originID, meal_type, title, ingredients, instructions, image):
    recipe, created = Recipe.objects.get_or_create(
        title=title,
        authorID=author,
        originID=originID,
    )
    if created:
        recipe.meal_type = meal_type
        recipe.ingredients = ingredients
        recipe.instructions = instructions
        recipe.publish_date = timezone.now()
        recipe.image = image
        recipe.save()

        print("Created Recipe: %s by %s" % (recipe.title, author.username))
    else:
        print("Recipe already exists: %s" % recipe.title)

    return recipe

def create_rating(user, recipe, rating_value):
    rating = Rating.objects.create(
        userID=user,
        recipeID=recipe,
        rating=rating_value
    )
    rating.save()
    return rating


def add_ratings(recipe, users):
    for _ in range(2):  
        user = random.choice(users)  
        rating_value = random.randint(3,5)  
        create_rating(user, recipe, rating_value)


def create_comment(user, recipe, content, parent=None):
    comment = Comment.objects.create(
        userID=user,
        recipeID=recipe,
        content=content,
        parent=parent
    )
    comment.save()
    return comment

def add_comments(recipe, users):
    comments_data = [
        ("Great recipe! Turned out amazing!", "Thanks! Glad you liked it!"),
        ("I had to tweak the spice level a bit, but loved it!", "That’s a great idea! What did you adjust?"),
        ("Tried it for dinner, my family loved it.", "Awesome! What did they enjoy the most?")
    ]
    owner = recipe.authorID
    for comment1, reply in comments_data:
        user = random.choice([u for u in users if u != owner])
        comment = create_comment(user, recipe, comment1)
        create_comment(owner, recipe, reply, parent=comment)

    
def create_favorite(user, recipe):
    favorite = Favorite.objects.get_or_create(
        user=user,
        recipe=recipe
    )

    return favorite



def populate():
    #
    users_data = [
        {'username': 'Frida_nims', 'email': 'farida@gmail.com', 'password': 'password1', 'originID': 143, 'image':'profile_pictures/aqua.jpg'},
        {'username': 'summer_bakes', 'email': 'summer@gmail.com', 'password': 'password2', 'originID': 2, 'image':'profile_pictures/KikiBg.jpg'},
        {'username': 'jason_k', 'email': 'jason@gmail.com', 'password': 'password3', 'originID': 3, 'image':'profile_pictures/TotoroRainBg.jpg'},
        {'username': 'chef_anna', 'email': 'anna@gmail.com', 'password': 'password4', 'originID': 4, 'image':'profile_pictures/anna.jpg'},
        {'username': 'baker_bob', 'email': 'bob@gmail.com', 'password': 'password5', 'originID': 5, 'image':'profile_pictures/bob.jpg'},
        {'username': 'culinary_carla', 'email': 'carla@gmail.com', 'password': 'password6', 'originID': 6, 'image':'profile_pictures/carla.jpg'}
    ]

    users = []
    for user_data in users_data:
        users.append(create_user(user_data['username'], user_data['email'], user_data['password'], user_data['originID'], user_data['image']))

    
    recipes_data = [
    
    {'author': users[0], 'originID': 16, 'meal_type': 'BF', 'title': 'Belgian Waffles', 
     'ingredients': 'Flour, Eggs, Sugar, Butter, Milk, Yeast', 
     'instructions': 'Mix ingredients, let batter rise, cook in waffle iron.', 
     'image': 'recipe_images/belgian_waffles.jpg'},

    {'author': users[1], 'originID': 16, 'meal_type': 'LU', 'title': 'Stoemp', 
     'ingredients': 'Mashed Potatoes, Carrots, Leeks, Butter', 
     'instructions': 'Mash vegetables together with butter and season.', 
     'image': 'recipe_images/stoemp.jpg'},

    {'author': users[2], 'originID': 16, 'meal_type': 'DS', 'title': 'Speculoos Cheesecake', 
     'ingredients': 'Speculoos biscuits, Cream Cheese, Sugar, Eggs', 
     'instructions': 'Blend biscuits, mix with cream cheese, bake.', 
     'image': 'recipe_images/speculoos_cheesecake.jpg'},

    {'author': users[1], 'originID': 16, 'meal_type': 'DN', 'title': 'Waterzooi', 
     'ingredients': 'Chicken, Carrots, Celery, Potatoes, Cream', 
     'instructions': 'Simmer ingredients in broth and finish with cream.', 
     'image': 'recipe_images/waterzooi.jpg'},

    
    {'author': users[1], 'originID': 102, 'meal_type': 'SN', 'title': 'Empanadas', 
     'ingredients': 'Flour, Vegetables, Cheese, Onion, Spices', 
     'instructions': 'Fill dough, fold, and bake or fry.', 
     'image': 'recipe_images/empanadas.jpg'},

    {'author': users[0], 'originID': 102, 'meal_type': 'LU', 'title': 'Milanesa de Pollo', 
     'ingredients': 'Chicken, Bread Crumbs, Eggs, Oil', 
     'instructions': 'Coat chicken in eggs and bread crumbs, fry.', 
     'image': 'recipe_images/milanesa.jpg'},

    {'author': users[2], 'originID': 102, 'meal_type': 'DN', 'title': 'Vegetarian Asado', 
     'ingredients': 'Zucchini, Peppers, Sweet Potatoes, Chimichurri', 
     'instructions': 'Grill vegetables and serve with chimichurri sauce.', 
     'image': 'recipe_images/asado.jpg'},

    {'author': users[0], 'originID': 102, 'meal_type': 'DS', 'title': 'Dulce de Leche Pancakes', 
     'ingredients': 'Flour, Milk, Sugar, Dulce de Leche', 
     'instructions': 'Make thin pancakes, spread dulce de leche, roll.', 
     'image': 'recipe_images/dulce_pancakes.jpg'},

   
    {'author': users[2], 'originID': 23, 'meal_type': 'BF', 'title': 'Pão de Queijo', 
     'ingredients': 'Tapioca Flour, Cheese, Eggs, Milk', 
     'instructions': 'Mix ingredients, shape into balls, bake.', 
     'image': 'recipe_images/pao_de_queijo.jpg'},

    {'author': users[0], 'originID': 23, 'meal_type': 'LU', 'title': 'Moqueca', 
     'ingredients': 'Fish, Coconut Milk, Tomatoes, Peppers, Onion', 
     'instructions': 'Cook fish in coconut milk and vegetables.', 
     'image': 'recipe_images/moqueca.jpg'},

    {'author': users[1], 'originID': 23, 'meal_type': 'DN', 'title': 'Vegetable Feijoada', 
     'ingredients': 'Black Beans, Rice, Collard Greens, Garlic', 
     'instructions': 'Slow cook beans with seasonings, serve with rice.', 
     'image': 'recipe_images/feijoada.jpg'},

    {'author': users[2], 'originID': 23, 'meal_type': 'DS', 'title': 'Açaí Bowl', 
     'ingredients': 'Açaí Berries, Bananas, Granola, Honey', 
     'instructions': 'Blend berries and banana, top with granola and honey.', 
     'image': 'recipe_images/acai_bowl.jpg'},

    
    {'author': users[0], 'originID': 30, 'meal_type': 'BF', 'title': 'BeaverTails', 
     'ingredients': 'Dough, Sugar, Cinnamon', 
     'instructions': 'Fry dough, coat with sugar and cinnamon.', 
     'image': 'recipe_images/beavertails.jpg'},

    {'author': users[1], 'originID': 30, 'meal_type': 'LU', 'title': 'Split Pea Soup', 
     'ingredients': 'Split Peas, Carrots, Onion, Celery, Vegetable Broth', 
     'instructions': 'Simmer ingredients until peas are soft.', 
     'image': 'recipe_images/soup.jpg'},

    {'author': users[2], 'originID': 30, 'meal_type': 'DN', 'title': 'Baked Maple Salmon', 
     'ingredients': 'Salmon, Maple Syrup, Soy Sauce, Garlic', 
     'instructions': 'Marinate salmon, bake until flaky.', 
     'image': 'recipe_images/maple_glazed_salmon.jpg'},

    {'author': users[0], 'originID': 30, 'meal_type': 'DS', 'title': 'Nanaimo Bars', 
     'ingredients': 'Chocolate, Coconut, Custard Powder, Butter', 
     'instructions': 'Layer chocolate, custard filling, and coconut crust.', 
     'image': 'recipe_images/bars.jpg'},

    
    {'author': users[2], 'originID': 147, 'meal_type': 'BF', 'title': 'Cornetto', 
     'ingredients': 'Flour, Sugar, Butter, Yeast, Milk', 
     'instructions': 'Bake crescent-shaped pastries.', 
     'image': 'recipe_images/cornetto.jpg'},

    {'author': users[0], 'originID': 147, 'meal_type': 'LU', 'title': 'Margherita Pizza', 
     'ingredients': 'Pizza Dough, Tomato Sauce, Mozzarella, Basil', 
     'instructions': 'Bake dough with toppings at high temperature.', 
     'image': 'recipe_images/pizza.jpg'},

    {'author': users[1], 'originID': 147, 'meal_type': 'DN', 'title': 'Mushroom Risotto', 
     'ingredients': 'Arborio Rice, Mushrooms, Parmesan, Vegetable Broth', 
     'instructions': 'Cook rice with broth, stir in mushrooms and cheese.', 
     'image': 'recipe_images/mushroom_risotto.jpg'},

    {'author': users[2], 'originID': 147, 'meal_type': 'DS', 'title': 'Tiramisu', 
     'ingredients': 'Ladyfingers, Coffee, Mascarpone, Cocoa Powder', 
     'instructions': 'Layer soaked ladyfingers with mascarpone and cocoa.', 
     'image': 'recipe_images/tiramisu.jpg'},

    {'author': users[0], 'originID': 125, 'meal_type': 'DN', 'title': 'Adobo', 
    'ingredients': 'Chicken or Pork, Soy Sauce, Vinegar, Garlic, Bay Leaves', 
    'instructions': 'Simmer meat in soy sauce, vinegar, and spices until tender.', 
    'image': 'recipe_images/adobo.jpg'},

    {'author': users[1], 'originID': 125, 'meal_type': 'DS', 'title': 'Leche Flan', 
     'ingredients': 'Egg Yolks, Condensed Milk, Sugar, Vanilla', 
     'instructions': 'Steam egg and milk mixture until set, then caramelize.', 
     'image': 'recipe_images/leche_flan.jpg'},

    {'author': users[2], 'originID': 81, 'meal_type': 'DN', 'title': 'Nyama Choma', 
     'ingredients': 'Beef or Goat, Salt, Spices', 
     'instructions': 'Grill seasoned meat over open fire and serve hot.', 
     'image': 'recipe_images/choma.jpg'},

    {'author': users[0], 'originID': 81, 'meal_type': 'BF', 'title': 'Mandazi', 
     'ingredients': 'Flour, Coconut Milk, Sugar, Cardamom', 
     'instructions': 'Mix ingredients, shape into triangles, and deep-fry.', 
     'image': 'recipe_images/mandazi.jpg'},

     {'author': users[1], 'originID': 145, 'meal_type': 'DN', 'title': 'Bibimbap', 
      'ingredients': 'Rice, Beef, Egg, Carrots, Spinach, Gochujang', 
      'instructions': 'Top rice with seasoned vegetables, beef, egg, and gochujang sauce. Mix before eating.', 
      'image': 'recipe_images/bibimbap.jpg'}
]

    
    recipes = []
    for recipe_data in recipes_data:
        recipes.append(create_recipe(**recipe_data))

    
    for recipe in recipes:
        add_ratings(recipe, users)
        add_comments(recipe, users)
        for user in users:
            create_favorite(user, recipe)

if __name__ == '__main__':
    print("Starting world_recipe population script...")
    populate()