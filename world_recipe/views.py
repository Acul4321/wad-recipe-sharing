from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
# rename login & logout to avoid confilcts with view functions
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, reverse
from django.http import HttpResponse
from world_recipe.forms import UserForm, UserProfileForm
from world_recipe.models import UserProfile, Recipe, Comment, Rating
from utils import COUNTRIES, get_country_name, get_country_id
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

#
# User auth
#

def register(request):
    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST)
        user_form = UserForm(request.POST)
        
        if user_profile_form.is_valid():
            #Create User for link
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            
            # Create UserProfile
            profile = user_profile_form.save(commit=False)
            profile.user = user #link to user
            profile.originID = user_profile_form.cleaned_data['originID']
            profile.save()
            
            return redirect('world_recipe:login')
    else:
        user_form = UserProfileForm()
        
    return render(request, 'world_recipe/register.html', {'user_form': user_form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                auth_login(request, user)
                return redirect(reverse('world_recipe:index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
        
    else:
        return render(request, 'world_recipe/login.html', {'user_form': UserForm()})

@login_required
def logout(request): # since user is logged in, we do not need to check
    auth_logout(request)
    return redirect('world_recipe:index')


def profile(request, username):
    return HttpResponse(f"Profile page for {username}")

@login_required
def add_recipe(request):
    return HttpResponse("Add recipe page")

def search(request):
    return HttpResponse("Search page")

def country(request, regionID):
    context_dict ={}
    country_name = Recipe.objects.get(regionID=regionID).get_country_name
    recipes = Recipe.objects.filter(regionID=regionID)
    context_dict['country_name'] = country_name
    context_dict['recipes'] = recipes
    
    return render(request, 'world_recipe/recipes_by_region.html', context_dict)

def meal_type(request, country_slug, meal_type_slug):
    return HttpResponse(f"{meal_type} recipes from {country_slug}")

def recipe(request, recipe_id, recipe_slug):
    try:
        recipe = get_object_or_404(Recipe, pk = recipe_id, slug=recipe_slug)
        
        return render(request, 'world_recipe/show_recipe.html')
    except Recipe.DoesNotExist:
        # Handle case where the recipe is not found
        return HttpResponse("recipe not found")

@login_required
def comment(request, country_slug, meal_type_slug, recipe_name_slug):
    return HttpResponse(f"Add comment to {recipe_name_slug}")

@login_required
def delete(request, country_slug, meal_type_slug, recipe_name_slug):
    return HttpResponse(f"Delete {recipe_name_slug}")
