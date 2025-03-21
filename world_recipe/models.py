from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from django.utils import timezone
from django.utils.text import slugify

from utils import get_country_name, get_country_id,COUNTRIES

#
# User model
#

class UserProfile(models.Model):
    # primary key id is automatically created
    user = models.OneToOneField(User, on_delete=models.CASCADE) # username,password
    originID = models.IntegerField(validators=[MaxValueValidator(len(COUNTRIES)-1), MinValueValidator(0)], blank=False) #range of countries indexes
    # add a default image
    profile_picture = models.ImageField(upload_to='profile_pictures', default='profile_pictures/default.jpg')
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username

    def get_country_id(self) -> int:
        return get_country_id(self.country)

    def get_country_name(self) -> str:
        return get_country_name(self.country)

#
# Recipe Model
# due to django model limitations, we must create a separate model for images and link them to the recipe
# https://qasimalbaqali.medium.com/upload-multiple-images-to-a-post-in-django-ff10f66e8f7a
#

# mealType choices for recipe
class MealType(models.TextChoices):
    BREAKFAST = 'BF', 'Breakfast'
    LUNCH = 'LU', 'Lunch'
    DINNER = 'DN', 'Dinner'
    SNACK = 'SN', 'Snack'
    DESSERT = 'DS', 'Dessert'

class Recipe(models.Model):
    # primary key id is automatically created
    authorID = models.ForeignKey(User, on_delete=models.CASCADE)
    originID = models.IntegerField(validators=[MaxValueValidator(len(COUNTRIES)-1), MinValueValidator(0)], blank=False) #range of countries indexes
    meal_type = models.CharField(max_length=2, choices=MealType.choices, blank=False)
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    title = models.CharField(max_length=200, blank=False)  # Add title field
    timestamp = models.DateTimeField(default=timezone.now)
    ingredients = models.TextField(blank=False)
    instructions = models.TextField(blank=False)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Recipe, self).save(*args, **kwargs)

    def average_rating(self) -> float:
        return Rating.objects.filter(post=self).aggregate(Avg("rating"))["rating__avg"] or 0
    
    def get_ingredients_list(self):
        return [x.strip() for x in self.ingredients.split('\n') if x.strip()]
        
    def get_instructions_list(self):
        return [x.strip() for x in self.instructions.split('\n') if x.strip()]
    
    def get_country_id(self) -> int:
        return get_country_id(self.country)
    
    def get_country_name(self) -> str:
        return get_country_name(self.country)

#
# Comment Model
#

class Comment(models.Model):
    # primary key id is automatically created
    recipeID = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField(max_length=2000, blank=False)

    def __str__(self):
        return f"{self.recipeID}: {self.content}"

#
# Rating Model
#

class Rating(models.Model):
    # primary key id is automatically created
    recipeID = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)], blank=False)

    def __str__(self):
        return f"{self.recipeID}: {self.rating}"