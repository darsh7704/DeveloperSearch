from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, widgets
from django import forms
from . models import Profile

class CustomerUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }


    def __init__(self, *args, **kwargs):
            super(CustomerUserCreationForm, self).__init__(*args, **kwargs)
        
            # Loop over the fields and apply the 'input' class
            for name, field in self.fields.items():
                field.widget.attrs.update({'class': 'input'})
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'location', 'short_intro', 'bio', 
                  'profile_image', 'social_github', 'social_twitter', 'social_linkedin', 
                  'social_youtube', 'social_website']
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        # Loop over the fields and apply the 'input' class
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})