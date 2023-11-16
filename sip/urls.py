from django.urls import path

from .views import *

urlpatterns = [
    path('', main_page, name='main_page'),
    path('reading/<slug:article_slug>/', show_doc, name='document_page'),
    path('add_document/', AddDocument.as_view(), name='add_document'),
    path('add_document_url/', AddDocumentURL.as_view(), name='add_document_url'),
    path('check_language/', CheckLanguage.as_view(), name='check_language'),
    path('help/', help_some, name='help')

]
