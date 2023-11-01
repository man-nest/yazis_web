import math

from sip.some_content.Document import Document


class Analyzer:
    documents = list()
    dictionary = None
    dict_term_inverse_frequency = None

    @staticmethod
    def some_init(docs):
        for one_obj in docs:
            path = one_obj.file_path
            Analyzer.documents.append(Document(str(path)))
        Analyzer.dictionary = Analyzer.create_dictionary()
        Analyzer.dict_term_inverse_frequency = Analyzer.create_term_inverse_frequency_dictionary()
        Analyzer.create_term_weight_dictionaries()

    @staticmethod
    def analyze(query: str):
        query_vector = Analyzer.calculate_query_vector(query)
        print(query_vector)
        print(Analyzer.dictionary)
        return {}

    @staticmethod
    def create_dictionary():
        dictionary = dict()

        for term in Analyzer.get_unique_terms():
            amount_documents_with_term = 0
            for document in Analyzer.documents:
                if document.has_term(term):
                    amount_documents_with_term += 1

            dictionary[term] = amount_documents_with_term

        return dictionary

    @staticmethod
    def get_unique_terms() -> set:
        terms = set()
        for document in Analyzer.documents:
            for term in document.dict_term_count.keys():
                terms.add(term)

        return terms

    @staticmethod
    # Calculating B
    def create_term_inverse_frequency_dictionary():
        term_inverse_frequency_dictionary = dict()

        for term in Analyzer.get_unique_terms():
            term_inverse_frequency_dictionary[term] = math.log(len(Analyzer.documents) / Analyzer.dictionary[term])

        return term_inverse_frequency_dictionary

    @staticmethod
    def create_term_weight_dictionaries():
        for document in Analyzer.documents:
            document.create_term_weight_dictionary(Analyzer.dict_term_inverse_frequency)

    @staticmethod
    def calculate_query_vector(query: str) -> tuple:
        query = Analyzer.clean_text(query)
        print(query)

        query_vector = list()

        for term in Analyzer.dictionary:
            if term in query:
                query_vector.append(1)
            else:
                query_vector.append(0)

        return tuple(query_vector)

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
