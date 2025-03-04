from django.shortcuts import render

def index(request):
    response = render(request, 'world_recipe/index.html')
    return response
