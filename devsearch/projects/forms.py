from django.forms import ModelForm, widgets
from .models import Project
from django import forms
from .models import Comment

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        
        # Loop over the fields and apply the 'input' class
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        self.fields['featured_image'].widget.attrs.pop('clearable', None)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']