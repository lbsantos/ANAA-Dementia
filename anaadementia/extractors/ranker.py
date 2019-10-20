
# -*- coding: utf-8 -*-
from sklearn.base import BaseEstimator, ClassifierMixin
from anaadementia.utils import cosine_similarity
from operator import itemgetter
import numpy as np

class ChunkRanker(BaseEstimator, ClassifierMixin):
    '''
    Recebe um objeto gensim representado as embeddings, e a dicionário
    contendo as proposições (classes) e a sentença de origem.
    O método de raqueamento recebe um vetor de tokens
    TODO: A entreda necessita ser tokenizada, a filtrar stopwords ou palavras de conteúdo
    '''
    def __init__(self, word_embeddings, proposicoes, chunks=[1, 2, 3]):
        self.word_embeddings = word_embeddings
        self.chunks = chunks
        self.proposicoes = proposicoes

    def _get_average_embedding(self, tokens):
        out_ = []
        for word in tokens:
            if word in self.word_embeddings:
                out_.append(self.word_embeddings[word])
        return np.mean(out_, axis=0)

    def _get_chunks_with_scors(self, tokens, context):
        n_original_tokens = len(tokens)
        chunks_with_scors = []

        for i in range(n_original_tokens):
            for chunk_size in self.chunks:
                if i + chunk_size - 1 < n_original_tokens:
                    chunk = tokens[i: i + chunk_size]
                    chunk_embedded = self._get_average_embedding(chunk)
                    score = cosine_similarity(
                        context,
                        chunk_embedded)

                    chunks_with_scors.append((
                        (i, i + chunk_size),
                        chunk,
                        score))
        return sorted(chunks_with_scors, key=itemgetter(2), reverse=True)
    
    def ranker(self, passage, context):
        if len(context) > 1:
            context_embedded = self._get_average_embedding(context)
        else:
            try:
                context_embedded = self.word_embeddings[context[0]]
            except KeyError:
                raise KeyError("A context word need to be in the word embeddings")
        chunks_with_scors = self._get_chunks_with_scors(passage, context_embedded)
        return chunks_with_scors

    def fit(self, X, y=None):
        return self
    
    def predict(self, X):
        predictions = []
        for sentence in X:
            preds = []
            for _, context in self.proposicoes.items():
                score = self.ranker(sentence,
                                    context)
                preds.append(score[0][-1])
            predictions.append(preds)
        return np.asarray(predictions)
