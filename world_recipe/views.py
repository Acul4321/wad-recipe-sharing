from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the world_recipe index.")

#
# User auth
#

def register(request):
    return HttpResponse("Register page")

def login(request):
    return HttpResponse("Login page")

@login_required
def logout(request):
    return HttpResponse("Logout functionality")


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