import spacy
from spacy.matcher import Matcher
import nltk
from nltk.corpus import wordnet as wn
import numpy as np
from collections import Counter

# Download necessary NLTK and spaCy data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nlp = spacy.load('en_core_web_sm')  # Load spaCy model

class Objective:
    def __init__(self, data, noOfQues):
        self.summary = data
        self.noOfQues = noOfQues

    def get_keywords(self):
        doc = nlp(self.summary)
        keywords = []
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "ORG", "GPE", "PRODUCT"]:
                keywords.append(ent.text)
        # Extract common nouns
        noun_freq = Counter([token.lemma_ for token in doc if token.pos_ == "NOUN"])
        common_nouns = [noun for noun, freq in noun_freq.most_common(10)]
        keywords.extend(common_nouns)
        return list(set(keywords))  # Remove duplicates

    def get_important_sentences(self):
        doc = nlp(self.summary)
        important_sentences = []
        keywords = self.get_keywords()
        for sent in doc.sents:
            score = self.calculate_sentence_score(sent, doc, keywords)
            if score > 0.5:
                important_sentences.append(sent.text)
        return important_sentences

    def calculate_sentence_score(self, sentence, doc, keywords):
        score = 0
        if len(list(sentence.ents)) > 0:
            score += 0.2
        for keyword in keywords:
            if keyword.lower() in sentence.text.lower():
                score += 0.1
        num_sentences = len(list(nlp(self.summary).sents))
        sentence_position = 0
        for sent in doc.sents:
            if sent == sentence:
                break
            sentence_position += 1
        sentence_position = (num_sentences - sentence_position) / num_sentences
        score += 0.1 * sentence_position
        return score

    def identify_questionable_phrases(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        pos_tags = nltk.pos_tag(tokens)
        doc = nlp(sentence)
        matcher = Matcher(nlp.vocab)
        # Adjusted pattern to catch more noun phrases
        noun_phrase_pattern = [{'POS': 'NOUN'}, {'POS': 'NOUN', 'OP': '?'}, {'POS': 'NOUN', 'OP': '?'}]
        matcher.add("NOUN_PHRASE", [noun_phrase_pattern])
        matches = matcher(doc)
        questionable_phrases = []
        for match_id, start, end in matches:
            span = doc[start:end]
            questionable_phrases.append(span.text)
        return questionable_phrases

    def get_mcq_data(self, phrase, sentence):
        answer = phrase
        similar_words = self.answer_options(phrase)
        distractors = self.generate_distractors(similar_words)
        distractors = distractors[: max(0, len(similar_words) - 1)]
        options = [answer] + distractors
        np.random.shuffle(options)
        question = sentence.replace(phrase, "__________")
        return {
            "Question": question,
            "Answer": answer,
            "Options": options
        }

    def answer_options(self, word):
        synsets = wn.synsets(word, pos="n")
        if not synsets:
            return []
        hypernyms = synsets[0].hypernyms()
        if not hypernyms:
            return []
        similar_words = [lemma.name().replace("_", " ") for hypernym in hypernyms for lemma in hypernym.lemmas() if lemma.name() != word]
        return similar_words[:3]

    def generate_distractors(self, similar_words):
        distractors = []
        doc = nlp(self.summary)
        for sent in doc.sents:
            for ent in sent.ents:
                if ent.text not in similar_words:
                    distractors.append(ent.text)
            if len(distractors) == len(similar_words):
                return distractors
        for word in doc:
            if word.text.lower() not in similar_words and word.pos_ in ['NOUN', 'VERB', 'ADJ']:
                distractors.append(word.text)
        return distractors[:len(similar_words)]

    def generate_test(self):
        important_sentences = self.get_important_sentences()
        mcq_data = []
        for sentence in important_sentences:
            questionable_phrases = self.identify_questionable_phrases(sentence)
            for phrase in questionable_phrases:
                mcq_data.append(self.get_mcq_data(phrase, sentence))
                
            if len(mcq_data) >= int(self.noOfQues):
                break
        if len(mcq_data) > int(self.noOfQues):
            mcq_data = list(np.random.choice(mcq_data, size=int(self.noOfQues), replace=False))
        return mcq_data

