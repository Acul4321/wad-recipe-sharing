from django.db import models
from .utils import COUNTRIES

from django.template.defaultfilters import slugify

class 

class Recipe(models.Model):
    #author/user foreign key
    name = models.CharField(max_length=200)
    regionID = models.IntegerField()
    meal_type = models.CharField(max_length=100)
    ingredients = models.JSONField()
    instructions = models.JSONField()
    publish_date = models.DateTimeField('Date published')
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Recipe, self).save(*args, **kwargs)

    def get_country_name(self):
        return COUNTRIES.get(self.regionID, 'Country unavailable')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Recipe'  #for admin interface
        verbose_name_plural = 'Recipes'
    

class Comment(models.Model):
    #user here foreign key
    #parent replies 
    
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    content = models.TextField()
    publish_date = models.DateTimeField('Date published')


class Rating(models.Model):
    #user and parent replies here
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)   
    rating = models.IntegerField()  
    

#class userprofile
