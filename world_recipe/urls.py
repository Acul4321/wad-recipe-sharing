from django.urls import path
from world_recipe import views

app_name = 'world_recipe'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('browse/region/<int:regionID>/', views.recipes_by_region, name='recipes_by_region'),
    path('recipe/<int:recipe_id>/<slug:recipe_slug>', views.show_recipe, name='show_recipe'),
]
