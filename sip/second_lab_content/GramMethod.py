from sip.second_lab_content.GramCreator import GramCreator


class GramsMethod:
    def __init__(self, english_doc_path: str, french_doc_path: str) -> None:
        self.max = 1000
        self.english_grams = GramCreator(english_doc_path).sorted_grams
        self.french_grams = GramCreator(french_doc_path).sorted_grams

    def get_measure(self, grams_a: list, grams_b: list):
        measure = 0
        for i in range(len(grams_a)):
            if grams_a[i] in grams_b:
                temp = grams_b.index(grams_a[i])
                measure += temp
            else:
                measure += self.max

        return measure

    def get_language(self, file_path: str):
        grams = GramCreator(file_path).sorted_grams
        
        english_measure = self.get_measure(grams, self.english_grams)
        french_measure = self.get_measure(grams, self.french_grams)

        if english_measure < french_measure:
            return 'English'
        else:
            return 'French'
