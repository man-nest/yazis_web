from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

from sip.models import *
from sip.some_content.Analyzer import Analyzer


def main_page(request):
    query = request.GET.get('query')
    terms = None
    docs = []
    if not bool(Analyzer.documents):
        docs = Document.objects.all()
        Analyzer.some_init(docs)

    if query:
        docs = []
        docs_title, terms = Analyzer.analyze(query)
        for one in docs_title:
            docs.append(Document.objects.filter(title=one).first())

    context = {
        "results": docs,
        'terms': terms,
        'query': query
    }

    return render(request, 'search_view.html', context)


def show_doc(request, article_slug):
    article = get_object_or_404(Document, slug=article_slug)

    context = {
        'article': article
    }

    return render(request, 'document_page.html', context)


# Create your views here.
def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена<h1>")
