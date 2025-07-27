from django.db import models
import uuid


class Project(models.Model):
    owner = models.ForeignKey('users.Profile', null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length = 120)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(upload_to="projects/", null=True, blank=True, default="projects/default.png")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    created = models.DateField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=120)
    created = models.DateField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    def __str__(self):
        return self.name

class Comment(models.Model):
    user = models.ForeignKey('users.Profile', on_delete=models.CASCADE)  # Associate comment with Profile
    project = models.ForeignKey(Project, related_name="comments", on_delete=models.CASCADE)  # Associate comment with Project
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.user.username} on {self.project.title}"
