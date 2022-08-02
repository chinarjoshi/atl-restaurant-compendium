import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from collections import Counter

def summarize(text: str, sentence_count: int = 3) -> str:
    doc = spacy.load('en_core_web_sm')(text)

    word_frequencies = Counter()
    for word in doc:
        word = word.text.lower()
        if word not in STOP_WORDS and word not in punctuation:
            word_frequencies[word] += 1

    max_frequency = word_frequencies.most_common(1)[0][1]

    for word in word_frequencies.values():
        word = word / max_frequency

    sentence_scores = Counter()
    for sent in doc.sents:
        for word in sent:
            word = word.text.lower()
            if word in word_frequencies:
                sentence_scores[sent] += word_frequencies[word]

    summary = nlargest(sentence_count, sentence_scores, key=sentence_scores.get)
    return ' '.join(word.text for word in summary)
