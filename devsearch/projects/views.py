from django.shortcuts import render, redirect, get_object_or_404
from . models import Project, Comment
from . forms import ProjectForm, CommentForm
from django.contrib.auth.decorators import login_required
from users.models import Profile
from django.contrib import messages
from django.urls import reverse

def projects(request):
    projs = Project.objects.all()
    context = {'projects': projs}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectobj = Project.objects.get(id=pk)
    comments = Comment.objects.filter(project=projectobj).order_by('-created_at')
    comment_form = CommentForm()

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.project = projectobj
            comment.user = request.user.profile  # or use request.user.profile if linking to Profile
            comment.save()
            return redirect('project', pk=projectobj.id)

    return render(request, 'projects/single_project.html', {
        'project': projectobj,
        'comments': comments,
        'comment_form': comment_form
    })
    

@login_required(login_url='login')
def create_project(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)  
            profile = Profile.objects.get(user=request.user)
            project.owner = profile
            project.save() 
            form.save_m2m()
            return redirect('projects')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url = 'login')
def update_project(request, pk):
    proj_var = Project.objects.get(id=pk)

    # Ensure only the owner can edit the project
    if proj_var.owner != request.user.profile:
        messages.error(request, "You are not allowed to edit this project.")
        return redirect(reverse('project', kwargs={'pk': pk}))

    form = ProjectForm(instance=proj_var)

    if request.method == 'POST':
        if "clear_image" in request.POST:
            # Delete the existing image file
            if form.instance.featured_image:
                form.instance.featured_image.delete(save=False)  

            # Assign the default image instead of None
            form.instance.featured_image = "projects/default.png"
        # Handle normal form submission
        form = ProjectForm(request.POST, request.FILES, instance=proj_var)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your project has been updated successfully.')
            return redirect('project', pk=proj_var.id)

    context = {'form': form, 'project': proj_var}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url = 'login')
def delete_project(request, pk):
    proj_list = Project.objects.get(id = pk)
    if proj_list.owner != request.user.profile:
        messages.error(request, "You are not allowed to delete this project.")
        return redirect(reverse('project', kwargs={'pk': pk}))
    
    if request.method == 'POST':
        proj_list.delete()
        return redirect('projects')
    context = {'object': proj_list, 'project': proj_list}
    return render(request, 'projects/delete_template.html', context)

def search_project(request):
    query = request.GET.get('q', '')  # Get search input from user
    
    if query:  
        try:
            projct = Project.objects.get(title__iexact=query)  # Case-insensitive exact match
            return redirect('project', pk=projct.id)
        except Project.DoesNotExist:
            messages.error(request, "No results found.")  # Show error message

    return redirect('projects') # Stay on the same page

