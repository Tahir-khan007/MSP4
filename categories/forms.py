from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    """Form for creating and editing categories."""
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter category name'
        })
    )

    class Meta:
        model = Category
        fields = ['name']
