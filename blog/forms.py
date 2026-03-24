# blog/forms.py
# Django Forms handle validation, rendering, and data cleaning automatically.

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Task


class PostForm(forms.ModelForm):
    """
    ModelForm automatically generates form fields from the Post model.
    It also handles validation rules defined on the model (max_length, etc.)
    """
    class Meta:
        model   = Post
        fields  = ['title', 'content', 'is_published']
        widgets = {
            'title':   forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Write your post content here...'
            }),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TaskForm(forms.ModelForm):
    """
    Form for creating and editing tasks.
    Demonstrates form with dropdown choices and date picker.
    """
    class Meta:
        model  = Task
        fields = ['title', 'description', 'status', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status':   forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class RegisterForm(UserCreationForm):
    """
    Extends Django's built-in UserCreationForm to add an email field.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model  = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap classes to all fields
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
