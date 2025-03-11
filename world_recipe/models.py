from django.db import models

class Recipe(models.Model):
    #author/user foreign key
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    meal_type = models.CharField(max_length=100)
    ingredients = models.JSONField()
    instructions = models.JSONField()


    def __str__(self):
        return self.name
    

class Comment(models.Model):
    #user here
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    content = models.TextField()

class Rating(models.Model):
    #user and parent replies here
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)   
    rating = models.IntegerField()  
    

#class userprofile
