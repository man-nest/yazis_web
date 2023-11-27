import math

from .Document import Document
from .TextRedactor import TextRedactor

from ..getSynonyms import getSynonymsForList
from ..textPreprocessing import textPreprocessing


class Analyzer:
    documents = list()
    dictionary = None
    dict_term_inverse_frequency = None

    @staticmethod
    def some_init(docs):
        for one_obj in docs:
            title = one_obj.title
            Analyzer.documents.append(Document(title))
            
        Analyzer.dictionary = Analyzer.create_dictionary()
        Analyzer.dict_term_inverse_frequency = Analyzer.create_term_inverse_frequency_dictionary()
        Analyzer.create_term_weight_dictionaries()

    @staticmethod
    def analyze(query: str, method=1):
        query_two=TextRedactor.filter(TextRedactor.clean_text(query))
        _, query = Analyzer.calculate_query_vector(query)
        

        query = textPreprocessing(query)

        query_synonyms = getSynonymsForList(query)

        dict_term_count = dict()        
       

        list_doc = []
        keys = []

        if method == 1:
            
            for term in query_two.split():
                if term in dict_term_count:
                    dict_term_count[term] += 1
                else:
                    dict_term_count[term] = 1
            
            for doc in Analyzer.documents:
                count = 0
                for term in doc.dict_term_count:
                    if term in dict_term_count:
                        count += 1
                if count == len(dict_term_count):
                    list_doc.append(doc.title)

            for key in dict_term_count.keys():
                keys.append(key)
        else:
            for synonyms_list in query_synonyms:
                for synonym in synonyms_list:
            
                    if synonym in dict_term_count:
                        dict_term_count[synonym] += 1
                    else:
                        dict_term_count[synonym] = 1
                        
            for doc in Analyzer.documents:
                query_vector = []
                rating = 0
                for term in doc.term_weight_dictionary:
                    if term in dict_term_count:
                        query_vector.append(term + ': ' + str(doc.term_weight_dictionary[term]))
                        rating += doc.term_weight_dictionary[term]
                query_vector.append(rating)
                
                if rating != 0:
                    list_doc.append(doc.title)
                    keys.append(query_vector)
        
        return list_doc, keys

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
        query = TextRedactor.filter(TextRedactor.clean_text(query))

        query_synonyms = getSynonymsForList(query.split())
        
        query_vector = list()
        for term in Analyzer.dictionary:
            
            for synonyms_list in query_synonyms:

                if term in synonyms_list:
                    query_vector.append(1)
                else:
                    query_vector.append(0)

        return tuple(query_vector), query
