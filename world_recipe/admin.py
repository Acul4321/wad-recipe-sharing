from django.contrib import admin
from .models import Recipe, Comment, Rating

class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Comment)
admin.site.register(Rating)



