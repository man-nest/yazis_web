import pymorphy3

from nltk.corpus import stopwords
from pathlib import Path

from sip.models import Document


class TextRedactor:
    # @staticmethod
    # def get_text(document_path: str) -> str:
    #     current_path = str(Path(__file__).resolve().parent.parent).replace('sip', 'media\\')
    #     current_path = current_path + document_path
    #     text = ""
    #     with open(current_path, "r", encoding='UTF-8') as document:
    #         for line in document:
    #             for term in line.lower().split():
    #                 for symbol in term:
    #                     if symbol.isalpha():
    #                         text += symbol

    #                 if text[-1] != ' ':
    #                     text += " "

    #     return text.strip()
    
    @staticmethod
    def get_text(title:str) -> str:
        document = Document.objects.get(title=title)
        return document.text

    @staticmethod
    def clean_text(text: str) -> str:
        cleaned_text = ''
        for term in text.lower().split():
            for symbol in term:
                if symbol.isalpha():
                    cleaned_text += symbol

            if cleaned_text[-1] != ' ':
                cleaned_text += " "

        return cleaned_text.strip()

    # @staticmethod
    # def filter(text: str) -> str:
    #     filter_list = list()
    #     current_path = str(Path(__file__).resolve().parent.parent).replace('sip', 'media/stop_words/stop_words.txt')
    #     current_path.join("/stop_words/stop_words.txt")

    #     with open(current_path, "r", encoding='UTF-8') as document:
    #         for term in document:
    #             filter_list.append(term.strip())

    #     words = list(text.split())

    #     morph = pymorphy3.MorphAnalyzer(lang='ru')

    #     new_text = ''
    #     for word in words:
    #         if morph.normal_forms(word)[0] not in filter_list:
    #             new_text += morph.normal_forms(word)[0] + ' '

    #     return new_text.strip()
    
    def filter(text: str) -> str:
        words = list(text.split())
        
        stop_words = stopwords.words('english')
        
        morph = pymorphy3.MorphAnalyzer(lang='ru')
        
        new_text = ''
        for word in words:
            if morph.normal_forms(word)[0] not in stop_words:
                new_text += morph.normal_forms(word)[0] + ' '

        return new_text.strip()

    @staticmethod
    def read_from_file(path):
        current_path = str(Path(__file__).resolve().parent.parent).replace('sip', 'media\\')
        current_path = current_path + path

        text = ""
        with open(current_path, "r", encoding='UTF-8') as document:
            for line in document:
                text += line

        return line
    
    # @staticmethod
    # def create_file(path, text):
    #     current_path = str(Path(__file__).resolve().parent.parent).replace('sip', 'media\\')
    #     current_path = current_path + path

    #     with open(current_path, "w", encoding='UTF-8') as document:
    #         document.write(text)
