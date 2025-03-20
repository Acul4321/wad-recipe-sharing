from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
# rename login & logout to avoid confilcts with view functions
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, reverse
from django.http import HttpResponse
from world_recipe.forms import UserForm, UserProfileForm
from world_recipe.models import UserProfile

def index(request):
    return render(request, 'world_recipe/index.html')

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

def country(request, country_slug):
    return HttpResponse(f"Recipes from {country_slug}")

def meal_type(request, country_slug, meal_type_slug):
    return HttpResponse(f"{meal_type} recipes from {country_slug}")

def recipe(request, country_slug, meal_type_slug, recipe_name_slug):
    return HttpResponse(f"Recipe: {recipe_name_slug}")

@login_required
def comment(request, country_slug, meal_type_slug, recipe_name_slug):
    return HttpResponse(f"Add comment to {recipe_name_slug}")

@login_required
def delete(request, country_slug, meal_type_slug, recipe_name_slug):
    return HttpResponse(f"Delete {recipe_name_slug}")