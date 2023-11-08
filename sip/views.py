import os
import nltk

from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from sip.some_content.Analyzer import Analyzer, TextRedactor
from .forms import *
from .second_lab_content.AlphabetMethod import AlphabetMethod
from .second_lab_content.GramMethod import GramsMethod
from .second_lab_content.NeuralMethod import NeuralMethod

dataset = ["sip/second_lab_content/dataset/english.html", "sip/second_lab_content/dataset/french.html"]


def main_page(request):
    
    nltk.download('all')

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
        'query': query,

    }

    return render(request, 'search_view.html', context)


def show_doc(request, article_slug):
    article = get_object_or_404(Document, slug=article_slug)

    context = {
        'article': article,
    }

    return render(request, 'document_page.html', context)


class AddDocument(View):
    template_name = 'add_document.html'

    def get(self, request, **kwargs):
        form = DocumentForm(initial={'title': None})

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            document = form.save(commit=False)
            if document.title is None:
                document.title = (str(document.file_path).replace('.txt', '')).replace('_', ' ')
            document.slug = (document.title.lower()).replace(' ', '_')
            path = 'documents\\' + str(document.file_path)
            document.save()
            document.text = TextRedactor.read_from_file(path)
            document.save()
            docs = Document.objects.all()
            Analyzer.some_init(docs)
            return redirect('main_page')  # Редирект после успешного сохранения

        context = {
            'form': form,
        }

        return render(request, self.template_name, context)


class CheckLanguage(View):
    template_name = 'check_language.html'

    def get(self, request, **kwargs):
        context = {

        }
        return render(request, self.template_name, context)

    def post(self, request):

        choice = request.POST.get('choice')
        path = request.POST.get('path')
        error = ''
        answer = ''

        if 'save_button' in request.POST:
            if len(dataset) == 3:
                answer = CheckLanguage.save_results(dataset[2])
                del dataset[2]
            else:
                error = 'Нечего сохранять'
            context = {
                'error_message': error,
                'answer': answer
            }
            return render(request, self.template_name, context)
        elif choice is None:
            error = 'Не выбран метод'
        elif path == '':
            error = 'Не введён путь к файлу'
        else:
            match choice:
                case '1':
                    method = GramsMethod(dataset[0], dataset[1])
                case '2':
                    method = AlphabetMethod(dataset[0], dataset[1])
                case '3':
                    method = NeuralMethod(dataset[0], dataset[1])
                case _:
                    method = None
            answer = CheckLanguage.analyze(method.get_language, path)

        context = {
            'error_message': error,
            'answer': answer
        }

        return render(request, self.template_name, context)

    @staticmethod
    def analyze(method, path):
        abs_path = os.path.abspath(path)
        import pathlib
        uri = pathlib.Path(abs_path).as_uri()
        import time
        start_time = time.time()
        content = uri + ' -- ' + method(path)
        answer_string = (content + " ( %s seconds )" % (time.time() - start_time))
        if len(dataset) == 3:
            dataset[2] = content
        else:
            dataset.append(content)
        return answer_string

    @staticmethod
    def save_results(content):
        answer = ''
        from datetime import date
        today = date.today()
        path = 'sip/second_lab_content/out/' + str(today) + ".txt"

        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)

        abs_path = os.path.abspath(path)
        import pathlib
        uri = pathlib.Path(abs_path).as_uri()
        answer = 'Saved -- ' + str(uri)

        return answer


def help_some(request):
    return render(request, 'help.html')


# Create your views here.
def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена<h1>")
