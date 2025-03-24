from django import forms
from django.contrib.auth.models import User
from world_recipe.models import UserProfile, Recipe, MealType
from utils import COUNTRIES

# used for registering the user
class UserProfileForm(forms.ModelForm): # used to register a new user
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    originID = forms.ChoiceField(choices=[(id, name) for id, name in COUNTRIES.items()],widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ('username','password','confirm_password','originID')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        return cleaned_data
    
class UserForm(forms.ModelForm): #used for login and part of registering(store User to assign to UserProfile)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password')

# used to edit your own profile
class ProfileEditForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}),required=False)
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}),required=False)

    class Meta:
        model = UserProfile
        fields = ('description', 'profile_picture')

# used to create recipes
class RecipeForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    originID = forms.ChoiceField(choices=[(id, name) for id, name in COUNTRIES.items()],widget=forms.Select(attrs={'class': 'form-control'}))
    meal_type = forms.ChoiceField(choices=MealType.choices,widget=forms.Select(attrs={'class': 'form-control'}))
    ingredients = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter each ingredient on a new line'}))
    instructions = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter each step on a new line'}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Recipe
        fields = ('title', 'originID', 'meal_type', 'ingredients', 'instructions', 'image')
