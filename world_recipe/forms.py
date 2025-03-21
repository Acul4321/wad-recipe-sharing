from django import forms
from world_recipe.models import Recipe

class RecipeForm(forms.ModelForm):
    name = forms.CharField(max_length=128, 
                           help_text="Please enter the recipe name")
    region_name = forms.CharField(max_length=200, help_text="Enter the region name")
    meal_type = forms.CharField(max_length=100, help_text="Enter the meal type")
    image = forms.ImageField(required=False, help_text="Upload an image for the recipe (optional)")
    ingredients = forms.CharField(widget=forms.Textarea, help_text="Enter ingredients (one per line)")
    instructions = forms.CharField(widget=forms.Textarea, help_text="Enter instructions (one per line)")

    class Meta:
        model = Recipe
        fields = ['name', 'region_name', 'meal_type', 'ingredients', 'instructions', 'image']
        