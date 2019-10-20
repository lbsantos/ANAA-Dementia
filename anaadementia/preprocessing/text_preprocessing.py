# -*- coding: utf-8 -*-
from sklearn.base import TransformerMixin, BaseEstimator
from anaadementia.utils import content_words_tags
import string

class Preprocessing(BaseEstimator, TransformerMixin):
    def __init__(self, probabilistic_tagger, tokenize):
        self.probabilistic_tagger = probabilistic_tagger
        self.tokenize = tokenize

    def transform(self, sentences):
        data_out = []
        for sentence in sentences:
            content_words = []
            for word in self.tokenize(sentence):
                word = word.lower()
                word, tag = self.probabilistic_tagger.tag([word])[0]
                if tag in content_words_tags:
                    content_words.append(word)
            data_out.append(content_words)
        return data_out

class PreprocessingSTS(TransformerMixin):
    def __init__(self, tokenizer, stop_words=None):
        self.tokenizer = tokenizer
        self.stop_words = stop_words
        self._punct = string.punctuation
 
    def transform(self, X, y=None):
        X_ = []
        for sent in X:            
            X_.append(
                [i.lower() for i in self.tokenizer(sent) if
                 i.lower() not in self.stop_words and i not in self._punct]
                )
        return X_

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def fit(self, X, y=None, **fit_params):
        return self

class ExpadingSynonyms(TransformerMixin):
    def __init__(self, synonyms, stemmer, delaf):
        self.synonyms = synonyms
        self.stemmer = stemmer
        self.delaf = delaf

    def _synonyms(self, tokens, it=1):
        """Docstring."""
        def recursion(tokens):
            new = []
            for token in tokens:
                try:
                    sin = self.synonyms[self.delaf[token]]
                    if len(sin) < 2:
                        new += sin
                except:
                    pass
            return list(set(tokens + new))
        for _ in range(it):
            tokens = recursion(tokens)
        return tokens
    
    def _apply_stemmer(self, tokens):
        return [self.stemmer.stem(token) for token in tokens]

    def transform(self, X, y=None):
        X_ = []
        for sent in X:
            tokens = self._synonyms(sent)
            X_.append(self._apply_stemmer(tokens))
        return X_

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def fit(self, X, y=None, **fit_params):
        return self