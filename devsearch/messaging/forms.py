from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['title', 'description']
        
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        
        # Loop over the fields and apply the 'input' class
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
