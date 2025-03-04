from django.urls import path
from world_recipe import views

app_name = 'world_recipe'

urlpatterns = [
    path('', views.index, name='index')
]
