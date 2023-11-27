import string
import operator

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from langdetect import detect
from yake import KeywordExtractor

from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.nlp.tokenizers import Tokenizer


class Essay:
    def __init__(self, input) -> None:
        self.input = input
    
    def get_summary(self):
        max_sentences = 10

        sentences_original = sent_tokenize(self.input)
        if max_sentences > len(sentences_original):
            print("Error, number of requested sentences exceeds number of sentences inputted")
        s = self.input.strip('\t\n')

        words_chopped = word_tokenize(s.lower())

        sentences_chopped = sent_tokenize(s.lower())

        stop_words = set(stopwords.words("spanish") + stopwords.words('english'))
        punc = set(string.punctuation)

        filtered_words = []
        for w in words_chopped:
            if w not in stop_words and w not in punc:
                filtered_words.append(w)
        total_words = len(filtered_words)

        word_frequency = {}
        output_sentence = []

        for w in filtered_words:
            if w in word_frequency.keys():
                word_frequency[w] += 1.0  # increment the value: frequency
            else:
                word_frequency[w] = 1.0  # add the word to dictionary

        for word in word_frequency:
            word_frequency[word] = (word_frequency[word] / total_words)

        tracker = [0.0] * len(sentences_original)
        for i in range(0, len(sentences_original)):
            for j in word_frequency:
                if j in sentences_original[i]:
                    tracker[i] += word_frequency[j]


        for i in range(0, len(tracker)):
            index, value = max(enumerate(tracker), key=operator.itemgetter(1))
            if (len(output_sentence) + 1 <= max_sentences) and (sentences_original[index] not in output_sentence):
                output_sentence.append(sentences_original[index])
            if len(output_sentence) > max_sentences:
                break

            tracker.remove(tracker[index])

        sorted_output_sent = self.sort_sentences(sentences_original, output_sentence)
        
        return sorted_output_sent

    def sort_sentences(self, original, output):
        sorted_sent_arr = []
        sorted_output = []
        for i in range(0, len(output)):
            if output[i] in original:
                sorted_sent_arr.append(original.index(output[i]))
        sorted_sent_arr = sorted(sorted_sent_arr)

        for i in range(0, len(sorted_sent_arr)):
            sorted_output.append(original[sorted_sent_arr[i]])
        return sorted_output
    
    def keywords(self):
        kw_extractor = KeywordExtractor()
        keyword = kw_extractor.extract_keywords(self.input)
        return keyword

    def ml(self):

        if detect(self.input) == 'es':
            parser = PlaintextParser.from_string(self.input, Tokenizer('spanish'))
        elif detect(self.input) == 'en':
            parser = PlaintextParser.from_string(self.input, Tokenizer('english'))
        elif detect(self.input) == 'ru':
            parser = PlaintextParser.from_string(self.input, Tokenizer('russian'))

        summarizer_1 = LuhnSummarizer()
        summary_1 = summarizer_1(parser.document, 10)

        return summary_1