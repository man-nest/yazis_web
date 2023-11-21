import os
import nltk
import pathlib
import time

from urllib.request import urlopen
from datetime import date

from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import *

from .components.classes.Analyzer import Analyzer, TextRedactor
from .components.textFromHTML import text_from_html
from .components.classes.MetricCalculator import MetricCalculator

from .second_lab_content.AlphabetMethod import AlphabetMethod
from .second_lab_content.GramMethod import GramsMethod
from .second_lab_content.NeuralMethod import NeuralMethod

from .components.classes.Essay import Essay

dataset = ["sip/second_lab_content/dataset/english.html", "sip/second_lab_content/dataset/french.html"]

# Create your views here.
def main_page(request):
    
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('all')

    query = request.GET.get('query')
    method = int(request.GET.get('choice')) if request.GET.get('choice') != None else 1
    

    documents = []
    if not bool(Analyzer.documents):
        docs = Document.objects.all()
        Analyzer.some_init(docs)

    if query:
        docs_title, terms = Analyzer.analyze(query, method)
        number = 0
        
        if len(docs_title) > 0:
            for one in docs_title:
                obj = Document.objects.filter(title=one).first()
                if method == 1:
                    obj.terms = terms
                    documents.append(obj)
                else:
                    terms[number][-1] = 'Общая оценка релевантности: ' + str(terms[number][-1])
                    obj.terms = terms[number]
                                       
                    documents.append(obj)

                    number += 1


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
            
            document.text = document.file_path.read().decode()
            document.save()
            
            docs = Document.objects.all()
            Analyzer.some_init(docs)

            return redirect('main_page')  # Редирект после успешного сохранения

        context = {
            'form': form,
        }

        return render(request, self.template_name, context)


class AddDocumentURL(View):
    template_name = 'add_document_url.html'

    def get(self, request, **kwargs):
        form = DocumentURLForm(initial={'title': None})

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        error = ''
        form = DocumentURLForm(request.POST, request.FILES)

        if form.is_valid():
            document = form.save(commit=False)

            try:
                html = urlopen(document.url)
                document.title, document.text = text_from_html(html.read())
                document.slug = (document.title.lower()).replace(' ', '_').replace('|', '')
                document.author = 'website'
                
                title = document.title.replace(' ', '_').replace('|', '')
                file = 'documents\\' + str(title) + '.txt'
                
                document.file_path = file
                
                document.save()   
                docs = Document.objects.all()
                Analyzer.some_init(docs)
                
                return redirect('main_page')  # Редирект после успешного сохранения
            except:
                error = 'Wrong url'
                

        context = {
            'form': form,
            'error': error,
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

        uri = pathlib.Path(abs_path).as_uri()

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
        
        today = date.today()
        path = 'sip/second_lab_content/out/' + str(today) + ".txt"

        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)

        abs_path = os.path.abspath(path)

        uri = pathlib.Path(abs_path).as_uri()
        answer = 'Saved -- ' + str(uri)

        return answer


def create_essay(request):
    error = ''
    essay = ''
    keywords = ''
    document = []
    
    method = request.POST.get('choice')
    
    if request.method == 'POST':
        if "Submit" in request.POST:
            
            keywordsOutput = []
            essayOutput = []
            if "File" in request.FILES:
                title = str(request.FILES['File'])
                slug = (title.split('.', 1)[0].lower()).replace(' ', '_').replace('|', '')

                file = request.FILES['File'].read()
                text = file.decode()

                essayObj = Essay(text)
                if method == 'Sentence_extraction':
                    essayOutput = essayObj.get_summary()
                    
                    for output in essayOutput:
                        essay += output 
                        
                elif method == 'ML':
                    essayOutput = essayObj.ml()
                    
                    for output in essayOutput:
                        essay += str(output)
                
                if request.POST.get('keywords') == 'Keywords':
                    keywordsOutput = essayObj.keywords()

                    for output in keywordsOutput:
                        keywords += str(output)

                try:
                    doc = Document(title=title, slug=slug, text=text, essay=essay, keywords=keywords)
                    doc.save()
                    
                    doc = Document.objects.get(essay=essay)
                    document.append(doc)
                except:
                    
                    error = 'Document with that name already exists!'
                    
                    if keywords != '':
                        doc = Document.objects.filter(title=title).update(keywords=keywords)
                        error = 'Document with that name already exists, but keywords added!'
                        
    context = {
        'document': document,
        'error': error,
    }

    return render(request, 'create_essay.html', context)

def metrics(request):
    error = ''
    metricsDict = {}
    
    if "Submit" in request.POST:        
        try:
            a = int(request.POST.get('a'))
            b = int(request.POST.get('b'))
            c = int(request.POST.get('c'))
            d = int(request.POST.get('d'))
            
            
            metric = MetricCalculator(a, b, c, d)
            metricsDict = {
                'Recall': metric.recall,
                'Precision': metric.precision,
                'Accuracy': metric.accuracy,
                'Error': metric.error,
                'F measure': metric.f_measure
            }
            
            
        except:
            error = 'Enter only numbers'
        
    context = {
        'metrics': metricsDict,
        'error': error
    }
    
    return render(request, 'metrics.html', context)

def help_some(request):
    return render(request, 'help.html')


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена<h1>")
