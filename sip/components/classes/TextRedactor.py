import pymorphy3

from nltk.corpus import stopwords
from pathlib import Path

from sip.models import Document


class TextRedactor:
    
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
    def save(title, text):
        current_path = str(Path(__file__).resolve().parent.parent).replace('sip', 'media\\').replace('components', '')
        current_path += 'essay\\'
        
        current_path = current_path + title + '.txt'
        print(current_path)
        with open(current_path, "w", encoding='UTF-8') as document:
            document.write(text)