from django import forms

from .models import *


class DocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Document
        fields = ['title', 'description', 'author', 'cover']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Document name'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'cols': 60, 'rows': 5, 'placeholder': 'Document description'}),
            'author': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Author'}),
            'cover': forms.ClearableFileInput(
                attrs={'class': 'form-control', 'placeholder': 'Document image'}),

        }
        labels = {
            'title': 'Document name',
            'description': 'Document description',
            'author': 'Author',
            'cover': 'Document image',
        }


class DocumentURLForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Document
        fields = ['url']
        widgets = {
            'url': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'URL'}
            )
        }
        
        labels = {
            'url': 'Добавить содержимое сайта по ссылке',
        }