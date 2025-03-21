from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
# rename login & logout to avoid confilcts with view functions
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, reverse
from django.http import HttpResponse, JsonResponse
from world_recipe.forms import UserForm, UserProfileForm, ProfileEditForm, RecipeForm
from world_recipe.models import UserProfile, Recipe, Comment, Rating
from utils import COUNTRIES, get_country_name, get_country_id
from django.db.models import Avg
from django.contrib.auth.models import User
from django.utils.text import slugify
import json
from django.conf import settings

def index(request):
    context_dict = {}
    most_recent_recipes = Recipe.objects.all().order_by('-publish_date')[:5]
    most_rated_recipes = Recipe.objects.annotate(avg_rating=Avg('rating__rating')).order_by('-avg_rating')[:5]
    
    context_dict['most_recent_recipes'] = most_recent_recipes
    context_dict['most_rated_recipes'] = most_rated_recipes
    context_dict['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
    return render(request, 'world_recipe/index.html', context_dict)

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
    try:
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        
        if request.method == 'POST' and request.user == user:
            form = ProfileEditForm(request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                form.save()
                return redirect('world_recipe:profile', username=username)
        else:
            form = ProfileEditForm(instance=user_profile)
        
        context_dict = {
            'userprofile': user_profile,
            'selected_user': user,
            'profile_form': form,
        }
        return render(request, 'world_recipe/profile.html', context_dict)
    except (User.DoesNotExist, UserProfile.DoesNotExist):
        return redirect('world_recipe:index')

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.authorID = request.user
            recipe.save()
            return redirect('world_recipe:recipe', 
                            country=slugify(recipe.get_country_name()),
                            meal_type=slugify(recipe.get_meal_type()),
                            recipe_name=recipe.slug
                            )
    else:
        form = RecipeForm()
    
    return render(request, 'world_recipe/add_recipe.html', {'form': form})

def search(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('q', '')
        recipes = Recipe.objects.filter(title__icontains=query)[:5]
        
        results = []
        for recipe in recipes:
            results.append({
                'title': recipe.title,
                'country': slugify(recipe.get_country_name()),
                'meal_type': slugify(recipe.get_meal_type()),
                'slug': recipe.slug,
                'image': recipe.image.url if recipe.image else None
            })
        
        return JsonResponse({'recipes': results})
    
    # Handle non-AJAX requests here if needed
    return render(request, 'world_recipe/search.html')

def country(request, regionID):
    context_dict ={}
    country_name = Recipe.objects.get(regionID=regionID).get_country_name
    recipes = Recipe.objects.filter(regionID=regionID)
    context_dict['country_name'] = country_name
    context_dict['recipes'] = recipes
    
    return render(request, 'world_recipe/recipes_by_region.html', context_dict)

def meal_type(request, country_slug, meal_type_slug):
    return HttpResponse(f"{meal_type} recipes from {country_slug}")

def recipe(request, country, meal_type, recipe_name):
    try:
        recipe = get_object_or_404(Recipe, slug=recipe_name)
        
        # Verify the URL parameters match the recipe
        if (slugify(recipe.get_country_name()) != country or 
            slugify(recipe.get_meal_type()) != meal_type):
            return HttpResponse("Recipe not found")
            
        context = {
            'recipe': recipe,
            'country': country,
            'meal_type': meal_type,
        }
        return render(request, 'world_recipe/recipe.html', context)
    except Recipe.DoesNotExist:
        return HttpResponse("Recipe not found")

@login_required
def comment(request, country, meal_type, recipe_name):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content = data.get('content')
            parent_id = data.get('parent_id')
            
            recipe = get_object_or_404(Recipe, slug=recipe_name)
            
            comment = Comment.objects.create(
                recipeID=recipe,
                userID=request.user,
                content=content,
                parent_id=parent_id
            )
            
            return JsonResponse({
                'status': 'success',
                'comment': {
                    'id': comment.id,
                    'content': comment.content,
                    'username': comment.userID.username,
                    'parent_id': comment.parent_id
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def delete(request, country, meal_type, recipe_name):
    try:
        recipe = get_object_or_404(Recipe, slug=recipe_name)
        
        # check if user is the author
        if request.user != recipe.authorID:
            return HttpResponse("You are not authorized to delete this recipe")
            
        recipe.delete()
        return redirect('world_recipe:index')
        
    except Recipe.DoesNotExist:
        return HttpResponse("Recipe not found")
