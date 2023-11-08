from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker


def textPreprocessing(rawText):
    rawText = rawText.lower()  # to lowercase
    rawText = rawText.translate(str.maketrans('', '', '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'))  # remove punctuation

    rawText = word_tokenize(rawText)  # tokenize

    spell = SpellChecker()  # correct misspelled words
    rawText = [spell.correction(word) for word in rawText]

    return rawText