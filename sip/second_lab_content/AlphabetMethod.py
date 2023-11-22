from nltk.corpus import stopwords

from sip.second_lab_content.HtmlDocument import HtmlDocument


class AlphabetMethod:
    def __init__(self, english_doc_path: str, french_doc_path: str) -> None:
        self.english_alphabet = self.get_alphabet(
            self.get_text(english_doc_path), 'english')
        self.french_alphabet = self.get_alphabet(
            self.get_text(french_doc_path), 'french')

    def get_language(self, file_path: str):
        alphabet = self.get_alphabet(self.get_text(file_path))
        test_len = len(alphabet)
                
        fra_intersect_len = len(alphabet.intersection(self.french_alphabet))
        eng_intersect_len = len(alphabet.intersection(self.english_alphabet))

        fra_measure = fra_intersect_len / test_len * 100
        eng_measure = eng_intersect_len / test_len * 100

        if eng_measure > fra_measure:
            return 'English'
        else:
            return 'French'

    @staticmethod
    def get_alphabet(text: str, language:str = 'default'):
        alphabet = set()
        stop_words = []
        
        if language == 'default':
            stop_words = stopwords.words('english') + stopwords.words('french')
        else:
            stop_words = stopwords.words(language)
        
        for sign in text:
            alphabet.add(sign)
        
        for stopword in stop_words:
            if stopword in text:
                alphabet.add(stopword)

        return alphabet

    @staticmethod
    def get_text(document_path: str) -> str:
        return HtmlDocument(document_path).get_text(document_path)
