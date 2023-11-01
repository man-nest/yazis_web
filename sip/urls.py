from django.urls import path

from .views import *

urlpatterns = [
    path('', main_page, name='main_page'),
    path('reading/<slug:article_slug>/', show_doc, name='document_page')
]
