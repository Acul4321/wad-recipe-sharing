from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the world_recipe index.")
    # response = render(request, 'world_recipe/index.html')
    # return response
