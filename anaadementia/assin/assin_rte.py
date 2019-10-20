# -*- coding: utf-8 -*-
# https://github.com/erickrf/assin
from sklearn.base import BaseEstimator, ClassifierMixin
from anaadementia.utils import tokenize
import numpy as np

class AssinRTE(BaseEstimator, ClassifierMixin):
    def __init__(self, base_estimator):
        self.estimator = base_estimator

    def extract_features(self, X):
        new_features = []
        for i in range(len(X)):
            tokenset1 = set(tokenize(X[i][0].lower()))
            tokenset2 = set(tokenize(X[i][1].lower()))
            num_common_tokens = len(tokenset2.intersection(tokenset1))
            proportion1 = num_common_tokens / len(tokenset1)
            proportion2 = num_common_tokens / len(tokenset2)
            new_features.append([proportion1, proportion2])
        return np.asarray(new_features)
    
    def fit(self, X, y):
        features_extracted = self.extract_features(X)
        self.estimator.fit(features_extracted, y)
        return self
    
    def predict(self, X):
        features_extracted = self.extract_features(X)
        return self.estimator.predict(features_extracted)

    def predict_proba(self, X):
        features_extracted = self.extract_features(X)
        return self.estimator.predict_proba(features_extracted)