from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker
from .checkCyrillic import checkCyrillic


def textPreprocessing(rawText):
    rawText = rawText.lower()  # to lowercase
    rawText = rawText.translate(str.maketrans('', '', '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'))  # remove punctuation

    rawText = word_tokenize(rawText)  # tokenize
    
    # rawText = [word for word in word_tokenize(rawText) if
    #     not any(char.isdigit() for char in word)]  # remove tokens with numbers

    spell: SpellChecker
    if checkCyrillic(rawText[0]):
        spell = SpellChecker(language='ru')
    else:
        spell = SpellChecker()  # correct misspelled words
    

    rawText = [spell.correction(word) if spell.correction(word) is not None else word for word in rawText]

    return rawText