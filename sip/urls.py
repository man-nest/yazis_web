from django.urls import path

from .views import *

urlpatterns = [
    path('', main_page, name='main_page'),
    path('reading/<slug:article_slug>/', show_doc, name='document_page'),
    path('add_document/', AddDocument.as_view(), name='add_document'),
    path('help/', help_some, name='help')
]
