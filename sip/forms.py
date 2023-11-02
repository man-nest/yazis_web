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
                attrs={'class': 'form-control', 'placeholder': 'Название документа', 'style': 'width: 250px;'}),
            'some_info': forms.Textarea(
                attrs={'class': 'form-control', 'cols': 60, 'rows': 10, 'placeholder': 'О документе',
                       'style': 'width: 350px;'}),
            'author': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Автор', 'style': 'width: 250px;'}),
            'file_path': forms.ClearableFileInput(
                attrs={'class': 'form-control-file', 'placeholder': 'ТxТ файл', 'style': 'width: 260px;'}),
            'cover': forms.ClearableFileInput(
                attrs={'class': 'form-control-file', 'placeholder': 'Фото статьи ', 'style': 'width: 260px;'}),

        }
        labels = {
            'title': 'Название документа',
            'some_info': 'О документе',
            'author': 'Автор',
            'file_path': 'ТxТ файл',
            'cover': 'Фото статьи ',
        }
