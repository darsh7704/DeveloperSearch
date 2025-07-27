from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, skill
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomerUserCreationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def profiles(request):
    profiles = Profile.objects.all()  
    context = {'profiles': profiles} 
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profs = Profile.objects.get(id=pk)
    topskills = profs.skill_set.exclude(description="")  
    otherskills = profs.skill_set.filter(description="") 
    context = {'profs': profs, 'topskills': topskills, 'otherskills': otherskills}
    return render(request, 'users/user-profile.html', context)

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('profiles')  # Redirect if already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('profiles')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'users/login_register.html', {'page': 'login'})

def logoutUser(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

def registerUser(request):
    if request.user.is_authenticated:
        return redirect('profiles')  # Prevent logged-in users from registering again  
    if request.method == 'POST':
        form = CustomerUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Your account has been created!')
            login(request, user)  # Log the user in immediately after registration
            return redirect('profiles')
        else:
            messages.error(request, 'An error occurred during registration. Please correct the errors below.')
    form = CustomerUserCreationForm()  # Initialize the form for GET request
    return render(request, 'users/login_register.html', {'page': 'register', 'form': form})



def logoutUser(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

@login_required
def edit_profile(request):
    profile = request.user.profile  # Get the current user's profile
    form = ProfileForm(instance = profile)
    if request.method == 'POST':
        if "clear_image" in request.POST:
            # Delete the existing image file
            if form.instance.profile_image:
                form.instance.profile_image.delete(save=False)  

            # Assign the default image instead of None
            form.instance.profile_image = "profiles/user-default.png"
        # Handle normal form submission
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('user-profile', pk=profile.id) # Redirect to the profile page after update
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form})
    
@login_required
def profile(request):
    profile = request.user.profile  # Get the current user's profile
    skills = profile.skill_set.all()  # Get the user's skills

    context = {
        'profile': profile,
        'skills': skills
    }

    return render(request, 'users/user-profile', context)

def search_developer(request):
    query = request.GET.get('q', '')  # Get search input from user
    
    if query:  
        try:
            developer = Profile.objects.get(name__iexact=query)  # Case-insensitive exact match
            # Redirect to profile page
            return redirect('user-profile', pk=developer.id)
        except Profile.DoesNotExist:
            messages.error(request, "No results found.")  # Show error message

    return redirect('profiles') # Stay on the same page
    