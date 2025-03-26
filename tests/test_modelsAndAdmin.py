#test that you cant have a rating of less than one
from django.test import TestCase
from django.contrib.auth.models import User
from world_recipe.models import Recipe, Rating, Comment, Favorite, UserProfile
from django.utils import timezone


class ModelTests(TestCase):
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
        
        self.recipe1 = Recipe.objects.create(
            title='Test Recipe 1',
            authorID=self.user,
            originID=1,
            meal_type='BF',
            ingredients='test ingredients',
            instructions='test instructions',
            publish_date=timezone.now()
        )

        Recipe.objects.create(
            title='Test Recipe 2',  
            authorID=self.user,
            originID=2,
            meal_type='DN',
            ingredients='test ingredients 2',
            instructions='test instructions 2',
            publish_date=timezone.now()
        )
        self.rating1 = Rating.objects.create(recipeID=self.recipe1, rating=5, userID=self.user)
        self.rating2 = Rating.objects.create(recipeID=self.recipe1, rating=3, userID=self.user)
        
        self.comment = Comment.objects.create(
            recipeID=self.recipe1,
            userID=self.user,
            content="Great recipe!"
        )

        self.favorite = Favorite.objects.create(user=self.user, recipe=self.recipe1)

        # Create a superuser
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@example.com'
        )

    def test_recipe_model(self):
        self.recipe1 = Recipe.objects.get(title='Test Recipe 1')
        self.assertEqual(self.recipe1.authorID, self.user, "tests on the recipe model failed")
        self.assertEqual(self.recipe1.originID, 1, "tests on the recipe model failed")
        self.assertEqual(self.recipe1.meal_type, 'BF', "tests on the recipe model failed")

        self.recipe2 = Recipe.objects.get(title='Test Recipe 2')
        self.assertEqual(self.recipe2.authorID, self.user, "tests on the recipe model failed")
        self.assertEqual(self.recipe2.originID, 2, "tests on the recipe model failed")
        self.assertEqual(self.recipe2.meal_type, 'DN', "tests on the recipe model failed")

    def test_rating_model(self):
        ratings = Rating.objects.filter(recipeID=self.recipe1)
        self.assertEqual(ratings.count(), 2, "tests on the rating model failed")
        self.assertEqual(ratings[0].rating, 5, "tests on the rating model failed")

    def test_comment_model(self):
        comments = Comment.objects.filter(content="Great recipe!")
        self.assertEqual(comments.count(), 1, "tests on the comment model failed")
        self.assertEqual(comments.first().content, "Great recipe!", "tests on the comment model failed")

    def test_str_methods(self):
        self.recipe = Recipe.objects.get(title='Test Recipe 1')
        self.rating1 = Rating.objects.filter(recipeID=self.recipe).first()
        self.comment = Comment.objects.get(recipeID=self.recipe1)
        self.favorite = Favorite.objects.get(recipe=self.recipe1)
        self.assertEqual(str(self.recipe1), 'Test Recipe 1', "tests on the str method failed")
        self.assertEqual(str(self.user_profile), 'testuser', "UserProfile __str__() method failed ")
        self.assertEqual(str(self.rating1), "Test Recipe 1: 5", "Rating __str__() method failed ")
        self.assertEqual(str(self.comment), "Test Recipe 1: Great recipe!", "Comment __str__() method failed ")
        self.assertEqual(str(self.favorite), "testuser favorites Test Recipe 1", "Favorite __str__() method failed ")

#testing models methods
    def test_slug_creation(self):
        """
        Tests whether the slug is correctly generated from the title and author's username.
        """
        recipe = Recipe.objects.create(
            title="Delicious Pasta",
            authorID=self.user,
            originID=1,
            meal_type='DN',
            ingredients="Pasta, Sauce",
            instructions="Cook the pasta, add sauce.",
            publish_date=timezone.now()
        )
        
        
        self.assertEqual(recipe.slug, "delicious-pasta-testuser", "Recipe slug was not correctly generated ")
    
    def test_slug_uniqueness(self):
        """
        Tests whether the slug is unique when duplicate titles exist.
        """
        recipe1 = Recipe.objects.create(
            title="Delicious Pasta",
            authorID=self.user,
            originID=1,
            meal_type='DN',
            ingredients="Pasta, Sauce",
            instructions="Cook the pasta, add sauce.",
            publish_date=timezone.now()
        )
        
        recipe2 = Recipe.objects.create(
            title="Delicious Pasta",
            authorID=self.user,
            originID=1,
            meal_type='DN',
            ingredients="Pasta, Sauce",
            instructions="Cook the pasta, add sauce.",
            publish_date=timezone.now()
        )
        
        self.assertNotEqual(recipe1.slug, recipe2.slug, "Recipe slugs are not unique ")
        self.assertEqual(recipe2.slug, "delicious-pasta-testuser-1", "Recipe slug was not correctly generated ")
    
#testing models methods
    def test_get_country_name(self):
        self.assertEqual(self.recipe1.get_country_name(), 'Afghanistan', "get_country_name method failed ")

    def test_get_ingredients_list(self):
        self.assertEqual(self.recipe1.get_ingredients_list(), ['test ingredients'], "get_ingredients_list method failed ")

    def test_average_rating(self):
        self.assertEqual(self.recipe1.average_rating(), 4, "Average rating method failed ")

    
    def test_rating_min_value(self):
        """
        Tests whether the rating value is at least 1.
        """
        rating = Rating.objects.create(recipeID=self.recipe1, rating=0, userID=self.user)
        self.assertEqual(rating.rating >= 1, True)
    
    def test_rating_max_value(self):
        """
        Tests whether the rating value is at most 5.
        """
        rating = Rating.objects.create(recipeID=self.recipe1, rating=6, userID=self.user)
        self.assertEqual(rating.rating <= 5, True)
    

#ADMIN INTEFRACE TESTS
    def test_admin_interface_accessible(self):
        """
        Tests whether the admin interface is accessible.
        """
        # Log in as the superuser
        self.client.login(username='admin', password='adminpass123')
        
        # Access the admin interface
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200, "Admin interface is not accessible ")
    
    def test_models_present(self):
        """
        Tests whether the models are present in the admin interface.
        """
        self.client.login(username='admin', password='adminpass123')
        
        # access the admin interface
        response = self.client.get('/admin/')
        response_body = response.content.decode()
        self.assertIn('Models in the World_Recipe application', response_body, "the Rango app wasn't listed on the admin interface's homepage. You haven't added the models to the admin interface ")
        self.assertIn('Recipes', response_body, "Recipes model is not present in the admin interface ")
        self.assertIn('Ratings', response_body, "Ratings model is not present in the admin interface ")
        self.assertIn('Comments', response_body, "Comments model is not present in the admin interface ")
        self.assertIn('Favorites', response_body, "Favorites model is not present in the admin interface ")
        self.assertIn('User profiles', response_body, "User profiles model is not present in the admin interface ")

    def test_admin_recipe_list_display(self):
        """
        Tests whether the admin interface displays the correct fields for the Recipe model.
        """
        self.client.login(username='admin', password='adminpass123')
        
        response = self.client.get('/admin/world_recipe/recipe/')
        response_body = response.content.decode()
        self.assertIn('<div class="text"><a href="?o=1">Title</a></div>', response_body, "Title column is missing in the admin interface.")
        self.assertIn('<div class="text"><a href="?o=4">Meal type</a></div>', response_body, "Meal Type column is missing in the admin interface.")






    




