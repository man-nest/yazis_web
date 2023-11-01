from django.http import HttpResponseNotFound
from django.shortcuts import render

from sip.models import *
from sip.some_content.Analyzer import Analyzer


def main_page(request):
    query = request.GET.get('query')
    if query:

        results = Analyzer.analyze(query)

        return render(request, 'search_view.html', {'results': results, 'query': query})
    else:
        if not bool(Analyzer.documents):
            docs = Document.objects.all()
            Analyzer.some_init(docs)

    return render(request, 'search_view.html')


# Create your views here.
def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена<h1>")
