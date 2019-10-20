# -*- coding: utf-8 -*-
from anaadementia.preprocessing.text_preprocessing import PreprocessingSTS, ExpadingSynonyms
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.utils.validation import check_is_fitted
from sklearn.base import TransformerMixin
import numpy as np

class AssinSTS(TransformerMixin):
    def __init__(self, embeddings, synonyms, stemmer, delaf, tokenizer, stop_words=None):
        self.preprocessing = PreprocessingSTS(tokenizer, stop_words)
        self.add_syns = ExpadingSynonyms(synonyms, stemmer, delaf)
        self.embeddings = embeddings
        self._tfidf = TfidfVectorizer()

    def _process(self, src_setences, trg_senteces):
        src_preprocessed = self.preprocessing.transform(src_setences)
        trg_preprocessed = self.preprocessing.transform(trg_senteces)

        src_syns = [' '.join(src) for src in self.add_syns.transform(src_preprocessed)]
        trg_syns = [' '.join(src) for src in self.add_syns.transform(trg_preprocessed)]

        return src_preprocessed, trg_preprocessed, src_syns, trg_syns

    def _cosine(self, src_preprocessed, trg_preprocessed, src_vec, trg_vec):
        cos_distances = []
        for _src_vec, _trg_vec, src_tokens, trg_tokens in zip(src_vec, trg_vec, src_preprocessed, trg_preprocessed):
            e1 = [i if i in self.embeddings else 'unk' for i in src_tokens]
            e2 = [i if i in self.embeddings else 'unk' for i in trg_tokens]
            cos_distances.append(
                [float(cosine_similarity(_src_vec, _trg_vec)),
                self.embeddings.n_similarity(e1, e2)])
        return cos_distances

    def transform(self, src_trg_setences, y=None,**fit_params):
        src_setences = src_trg_setences[:,0]
        trg_senteces = src_trg_setences[:,1]
        check_is_fitted(self, '_tfidf', 'The tfidf vector is not fitted')
        src_preprocessed, trg_preprocessed, src_syns, trg_syns = self._process(src_setences, trg_senteces)
        vecs = self._tfidf.transform(src_syns + trg_syns)
        src_vecs = vecs[0:vecs.shape[0]//2,:]
        trg_vecs = vecs[vecs.shape[0]//2:,:]

        return self._cosine(
            src_preprocessed,
            trg_preprocessed,
            src_vecs,
            trg_vecs)

    def fit_transform(self, src_trg_setences, y=None, **fit_params):
        src_setences = src_trg_setences[:,0]
        trg_senteces = src_trg_setences[:,1]
        src_preprocessed, trg_preprocessed, src_syns, trg_syns = self._process(src_setences, trg_senteces)
        vecs = self._tfidf.fit_transform(src_syns + trg_syns)
        src_vecs = vecs[0:vecs.shape[0]//2,:]
        trg_vecs = vecs[vecs.shape[0]//2:,:]

        return self._cosine(
            src_preprocessed,
            trg_preprocessed,
            src_vecs,
            trg_vecs)

    def fit(self, src_trg_setences, y=None, **fit_params):
        src_setences = src_trg_setences[:,0]
        trg_senteces = src_trg_setences[:,1]
        _, _, src_syns, trg_syns = self._process(src_setences, trg_senteces)
        self._tfidf.fit(src_syns + trg_syns)
        return self