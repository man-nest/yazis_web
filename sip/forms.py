from django import forms

from .models import *


class DocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Document
        fields = ['title', 'some_info', 'author', 'file_path', 'cover']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Название документа'}),
            'some_info': forms.Textarea(
                attrs={'class': 'form-control', 'cols': 60, 'rows': 5, 'placeholder': 'О документе'}),
            'author': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Автор'}),
            'file_path': forms.ClearableFileInput(
                attrs={'class': 'form-control', 'placeholder': 'ТxТ файл'}),
            'cover': forms.ClearableFileInput(
                attrs={'class': 'form-control', 'placeholder': 'Фото статьи '}),

        }
        labels = {
            'title': 'Название документа',
            'some_info': 'О документе',
            'author': 'Автор',
            'file_path': 'ТxТ файл',
            'cover': 'Фото статьи ',
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