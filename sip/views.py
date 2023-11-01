from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

from sip.models import *
from sip.some_content.Analyzer import Analyzer


def main_page(request):
    query = request.GET.get('query')
    documents = []
    method = 2
    if not bool(Analyzer.documents):
        docs = Document.objects.all()
        Analyzer.some_init(docs)

    if query:
        docs_title, terms = Analyzer.analyze(query, method)
        number = 0

        for one in docs_title:
            obj = Document.objects.filter(title=one).first()
            if method == 1:
                obj.terms = terms
                documents.append(obj)
            else:
                obj.terms = terms[number]
                if len(documents) < 1:
                    documents.append(obj)
                elif documents[-1].terms[-1] < obj.terms[-1]:
                    documents.clear()
                    documents.append(obj)
                number += 1

        if method == 2:
            documents[-1].terms[-1] = 'Общая оценка релевантности: ' + str(documents[-1].terms[-1])

    context = {
        "results": documents,
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
