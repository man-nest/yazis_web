from nltk.corpus import wordnet
from wiki_ru_wordnet import WikiWordnet

from .checkCyrillic import checkCyrillic


plural_of_irregular_nouns = {
    'man': 'men',
    'person': 'people',
    'woman': 'women',
    'mouse': 'mice',
    'child': 'children',
    'tooth': 'teeth',
    'goose': 'geese',
    'ox': 'oxen',
    'fish': 'fish',
    'fruit': 'fruit',
    'deer': 'deer',
    'sheep': 'sheep',
    'Swiss': 'Swiss',
    'phenomenon': 'phenomena',
    'datum': 'data',
    'formula': 'formulae',
    'genius': 'genii',
}


def getSynonyms(word):
    synonyms = []
    
    if checkCyrillic(word):
        wikiwordnet = WikiWordnet()
        
        for synset in wikiwordnet.get_synsets(word):
            for word in synset.get_words():
                if word.lemma() not in synonyms:
                    synonyms.append(word.lemma())
    else:     
        for synset in wordnet.synsets(word):
            for lemma in synset.lemmas():
                if lemma.name() not in synonyms:
                    synonyms.append(lemma.name())
             
    if len(synonyms) == 0:
        synonyms.append(word)
    
    return synonyms


def getSynonymsForList(query_list):
    query_synonyms = []
    
    for word in query_list:
        synonyms = getSynonyms(word)
        
        for synonym in synonyms:
            if synonym in plural_of_irregular_nouns:
                if plural_of_irregular_nouns[synonym] not in synonyms:
                    synonyms.append(plural_of_irregular_nouns[synonym])
            elif synonym in plural_of_irregular_nouns.values():
                key = [k for k, v in plural_of_irregular_nouns.items() if v == synonym][0]
                if key not in synonyms:
                    synonyms.append(key)
                    
        if checkCyrillic(query_list[0]):
            synonyms.extend(
                [synonym + 's' for synonym in synonyms if synonym[-1] != 's' 
                    and synonym not in plural_of_irregular_nouns.keys()
                    and synonym not in plural_of_irregular_nouns.values()
                ]
            )
            
        query_synonyms.append(synonyms)
    
    return query_synonyms