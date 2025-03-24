from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
# rename login & logout to avoid confilcts with view functions
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, reverse
from django.http import HttpResponse, JsonResponse
from world_recipe.forms import UserForm, UserProfileForm, ProfileEditForm, RecipeForm, LoginForm
from world_recipe.models import UserProfile, Recipe, Comment, Rating, Favorite
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
    
    all_recipes = Recipe.objects.all()
    context_dict['all_recipes'] = all_recipes
    

    return render(request, 'world_recipe/index.html', context_dict)
    

def about(request):
    return render(request, 'world_recipe/about.html')

#
# User auth
#

def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and user_profile_form.is_valid():
            try:
                # Create User
                user = user_form.save(commit=False)
                user.set_password(user.password)
                user.save()
                
                # Create UserProfile
                profile = user_profile_form.save(commit=False)
                profile.user = user
                profile.originID = user_profile_form.cleaned_data['originID']
                profile.save()

                # Auto login
                user = authenticate(username=user.username, 
                                    password=user_form.cleaned_data['password'])
                if user:
                    auth_login(request, user)
                    return redirect('world_recipe:index')
            except Exception as e:
                # if there is an error, delete the user if created
                if user:
                    user.delete()
                return HttpResponse(f"An error occurred during registration: {str(e)}")
    else:
        user_profile_form = UserProfileForm()
        
    return render(request, 
                 'world_recipe/register.html',
                 {'profile_form': user_profile_form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            
            if user and user.is_active:
                auth_login(request, user)
                return redirect('world_recipe:index')
    else:
        form = LoginForm()
    
    return render(request, 'world_recipe/login.html', {'login_form': form})

@login_required
def logout(request): # since user is logged in, we do not need to check
    auth_logout(request)
    return redirect('world_recipe:index')


def profile(request, username):
    try:
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        favorite_recipes = Recipe.objects.filter(favorite__user=user)
        
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
            'favorite_recipes': favorite_recipes,
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

def country(request, country):
    context_dict = {}
    
    # get the country ID from the country slug
    try:
        country_id = get_country_id(country)  # cahnge slug to originID using your utility function
        # filtering recipes based on the country ID
        recipes = Recipe.objects.filter(originID=country_id)
        country_name = country
        meal_type = request.GET.get('meal_type', None)
        sort_by = request.GET.get('sort_by', None)

        if meal_type and meal_type != 'all':
            recipes = Recipe.objects.filter(originID=country_id, meal_type=meal_type)
        else:
            recipes = Recipe.objects.filter(originID=country_id)
        
        if sort_by == 'most_rated':
            recipes = recipes.annotate(avg_rating=Avg('rating__rating')).order_by('-avg_rating')
        elif sort_by == 'recently_published':
            recipes = recipes.order_by('-publish_date')
        

        context_dict['country_name'] = country_name
        context_dict['recipes'] = recipes
        context_dict['meal_type'] = meal_type
        context_dict['sort_by'] = sort_by
    except Recipe.DoesNotExist:
        context_dict['error_message'] = "country not found"
    
    return render(request, 'world_recipe/country.html', context_dict)

def meal_type(request, country_slug, meal_type_slug):
    return HttpResponse(f"{meal_type} recipes from {country_slug}")

def recipe(request, country, meal_type, recipe_name):
    try:
        recipe = get_object_or_404(Recipe, slug=recipe_name)
        
        # Verify the URL parameters match the recipe
        if (slugify(recipe.get_country_name()) != country or 
            slugify(recipe.get_meal_type()) != meal_type):
            return HttpResponse("Recipe not found")
        
        # Check if user has favorited this recipe
        is_favorite = False
        if request.user.is_authenticated:
            is_favorite = Favorite.objects.filter(user=request.user, recipe=recipe).exists()
            
        context = {
            'recipe': recipe,
            'country': country,
            'meal_type': meal_type,
            'is_favorite': is_favorite,
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

@login_required
def rate(request, country, meal_type, recipe_name):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rating_value = int(data.get('rating'))
            
            recipe = get_object_or_404(Recipe, slug=recipe_name)
            
            # Create or update rating
            rating = Rating.objects.update_or_create(
                recipeID=recipe,
                userID=request.user,
                defaults={'rating': rating_value}
            )[0]
            
            return JsonResponse({
                'status': 'success', 
                'new_average': recipe.average_rating()
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def toggle_favorite(request, recipe_id):
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})
        
    recipe = get_object_or_404(Recipe, id=recipe_id)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        recipe=recipe
    )
    
    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True
        
    return JsonResponse({
        'status': 'success',
        'is_favorite': is_favorite
    })

@login_required
def toggle_favorite(request, country, meal_type, recipe_name):
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})
        
    recipe = get_object_or_404(Recipe, slug=recipe_name)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        recipe=recipe
    )
    
    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True
        
    return JsonResponse({
        'status': 'success',
        'is_favorite': is_favorite
    })
