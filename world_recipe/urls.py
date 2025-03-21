from django.urls import path
from world_recipe import views

app_name = 'world_recipe'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),

    # user auth
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # user profile and information
    path('profile/<username>/', views.profile, name='profile'),
    path('profile/<username>/#favourites', views.profile, name='favourites'),
    path('profile/<username>/#my_recipes', views.profile, name='my_recipes'), #will be able to delete if on own profile

    # recipe search and logic
    path('add_recipe', views.add_recipe, name='add_recipe'), #user auth req
    path('search/', views.search, name='search'),
    path('recipe/<slug:country>/', views.country, name='country'),
    path('recipe/<slug:country>/<slug:meal_type>/', views.meal_type, name='meal_type'),
    path('recipe/<slug:country>/<slug:meal_type>/<slug:recipe_name>/', views.recipe, name='recipe'),
    path('recipe/<slug:country>/<slug:meal_type>/<slug:recipe_name>/add_comment/', views.comment, name='comment'), #user auth req, can comment as root(parent=null) or as a subcomment(parent=commentID)
    path('recipe/<slug:country>/<slug:meal_type>/<slug:recipe_name>/delete/', views.delete, name='delete'), #if on recipe made by currently logged in user
    path('recipe/<slug:country>/<slug:meal_type>/<slug:recipe_name>/rate/', views.rate, name='rate'),
]