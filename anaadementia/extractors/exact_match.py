# -*- coding: utf-8 -*-
from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np

class ExactMatch(BaseEstimator, ClassifierMixin):
    def __init__(self, units_with_phrares):
        self.units_with_phrares = units_with_phrares
        
    def fit(self, X=None):
        self
        
    def predict(self, X):
        predictions = []
        for sentence in X:
            mathches_per_setence = [0]*len(self.units_with_phrares)
            for i, list_of_phrases in enumerate(self.units_with_phrares):
                for phrase in list_of_phrases:
                    if phrase in sentence:
                        mathches_per_setence[i] = 1
            predictions.append(mathches_per_setence)
        return np.asarray(predictions)