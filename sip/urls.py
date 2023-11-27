from django.urls import path

from .views import *

urlpatterns = [
    path('', main_page, name='main_page'),
    path('metrics/', metrics, name='metrics'),
    path('reading/<slug:article_slug>/', show_doc, name='document_page'),
    path('add_document/', AddDocument.as_view(), name='add_document'),
    path('add_document_url/', AddDocumentURL.as_view(), name='add_document_url'),
    path('check_language/', CheckLanguage.as_view(), name='check_language'),
    path('create_essay/', create_essay, name='create_essay'),
    path('speechGeneration/', speechGeneration, name='speechGeneration'),
    path('help/', help_some, name='help')

]
