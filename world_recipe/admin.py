from django.contrib import admin
from world_recipe.models import UserProfile#, Recipe, Comment, Rating, RecipeImages

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'originID', 'profile_picture')

admin.site.register(UserProfile)
# admin.site.register(Recipe)
# admin.site.register(Comment)
# admin.site.register(Rating)
# admin.site.register(RecipeImages)
