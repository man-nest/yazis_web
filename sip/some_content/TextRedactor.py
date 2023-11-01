from pathlib import Path

import pymorphy2


class TextRedactor:
    @staticmethod
    def get_text(document_path: str) -> str:
        current_path = str(Path(__file__).resolve().parent.parent).replace('sip', 'media\\')
        current_path = current_path + document_path
        text = ""
        with open(current_path, "r", encoding='UTF-8') as document:
            for line in document:
                for term in line.lower().split():
                    for symbol in term:
                        if symbol.isalpha():
                            text += symbol

                    if text[-1] != ' ':
                        text += " "

        return text.strip()

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

    @staticmethod
    def filter(text: str) -> str:
        filter_list = list()
        current_path = str(Path(__file__).resolve().parent.parent).replace('sip', 'media/stop_words/stop_words.txt')
        current_path.join("/stop_words/stop_words.txt")

        with open(current_path, "r", encoding='UTF-8') as document:
            for term in document:
                filter_list.append(term.strip())

        words = list(text.split())

        morph = pymorphy2.MorphAnalyzer(lang='ru')

        new_text = ''
        for word in words:
            if morph.normal_forms(word)[0] not in filter_list:
                new_text += morph.normal_forms(word)[0] + ' '

        return new_text.strip()
