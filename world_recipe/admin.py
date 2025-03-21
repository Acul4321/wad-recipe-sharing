from django.contrib import admin
from world_recipe.models import UserProfile, Recipe, Comment, Rating

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'originID', 'profile_picture')

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'authorID', 'originID', 'meal_type')
    list_filter = ('meal_type', 'originID')
    search_fields = ['title', 'ingredients']

class CommentAdmin(admin.ModelAdmin):
    list_display = ('recipeID', 'userID', 'timestamp', 'content')
    list_filter = ('timestamp',)

class RatingAdmin(admin.ModelAdmin):
    list_display = ('recipeID', 'userID', 'rating')
    list_filter = ('rating',)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Rating, RatingAdmin)