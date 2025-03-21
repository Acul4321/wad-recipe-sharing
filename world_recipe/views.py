from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .utils import COUNTRIES
from .utils import get_country_id
from .models import Recipe, Rating
from django.db.models import Avg

def index(request):
    context_dict ={}
    most_recent_recipes = Recipe.objects.all().order_by('-publish_date')[:5]
    most_rated_recipes = Recipe.objects.annotate(avg_rating=Avg('rating__rating')).order_by('-avg_rating')[:5]
    
    context_dict['most_recent_recipes'] = most_recent_recipes
    context_dict['most_rated_recipes']=most_rated_recipes
    response = render(request, 'world_recipe/index.html', context_dict)
    return response



def about(request):
    context_dict = {'message': 'World Recipe was created by Group 6C.'}
    return render(request, 'world_recipe/about.html',context_dict)


def recipes_by_region(request, regionID):
    context_dict ={}
    country_name = Recipe.objects.get(regionID=regionID).get_country_name
    recipes = Recipe.objects.filter(regionID=regionID)
    context_dict['country_name'] = country_name
    context_dict['recipes'] = recipes
    
    return render(request, 'world_recipe/recipes_by_region.html', context_dict)



def show_recipe(request, recipe_id, recipe_slug):
    try:
        recipe = get_object_or_404(Recipe, pk = recipe_id, slug=recipe_slug)
        
        return render(request, 'world_recipe/show_recipe.html')
    except Recipe.DoesNotExist:
        # Handle case where the recipe is not found
        return HttpResponse("recipe not found")
    
