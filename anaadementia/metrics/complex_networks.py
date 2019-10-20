# -*- coding: utf-8 -*-
from sklearn.base import TransformerMixin
from statistics import mean, stdev
from scipy.stats import skew
from igraph import Graph
import numpy as np


class ComplexNetworks(TransformerMixin):
    def __init__(self, tokenize, stopwords):
        self.tokenize = tokenize
        self.stopwords = stopwords

        metrics = ['pagerank',
                    'betweenness',
                    'eccentricity',
                    'eigenvector_centrality',
                    'knn',
                    'shortest_paths',
                    'degree']

        self.feature_names = []
        for m in metrics:
            self.feature_names.extend(['avg_' + m, 'std_' + m, 'sk_' + m])

        self.feature_names.extend(['diameter',
                                   'transitivity_undirected'])

    def transform(self, X, y=None,**fit_params):
        out_m = []

        for example in X:
            text = []
            if isinstance(example, list):
                for sentences in example:
                    text.extend(self.tokenize(sentences))
            else:
                text = self.tokenize(example)
            g = self._build_graph(text)
            out_m.append(self._feature_extraction(g))

        return np.array(out_m)

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def fit(self, X, y=None, **fit_params):
        return self

    def _build_graph(self, original_tokens):
        tokens = [w.lower() for w in original_tokens if w.lower(
        ) not in self.stopwords and not w.isnumeric()]
        g = Graph()
        edges = []

        g.add_vertices(tokens[0])
        for i in range(1, len(tokens)):
            if tokens[i] not in g.vs['name']:
                g.add_vertices(tokens[i])
                edge = sorted((tokens[i], tokens[i - 1]))
                if edge not in edges:
                    edges.append(edge)

            else:
                edge = sorted((tokens[i], tokens[i - 1]))
                if edge not in edges:
                    edges.append(edge)

        g.add_edges(edges)
        return g

    def _mean_sd_sk(self, values):
        return mean(values), stdev(values), skew(values)

    def _feature_extraction(self, graph):
        example = []
        example.extend(self._mean_sd_sk(graph.pagerank()))
        example.extend(self._mean_sd_sk(graph.betweenness()))
        example.extend(self._mean_sd_sk(graph.eccentricity()))
        example.extend(self._mean_sd_sk(graph.eigenvector_centrality()))
        graph_simple = graph.simplify()
        example.extend(self._mean_sd_sk(graph_simple.knn()[0]))
        shortest_paths = graph_simple.shortest_paths()
        shortest_paths2 = []
        for shortest_path in shortest_paths:
            shortest_paths2.append(mean(shortest_path))

        example.extend(self._mean_sd_sk(shortest_paths2))

        example.extend(self._mean_sd_sk(graph.degree()))
        example.append(graph.diameter())
        example.append(graph.transitivity_undirected()) # Clustering Coefficient
        return example

    def get_graph(self, example):
        text = []
        if isinstance(example, list):
            for sentences in example:
                text.extend(self.tokenize(sentences))
        else:
            text = self.tokenize(example)
        return self._build_graph(text)

class EnrichedComplexNetworks(ComplexNetworks):

    def __init__(self, tokenize, stopwords, model, threshold):
        super(self.__class__, self).__init__(tokenize, stopwords)
        self.model = model
        self.threshold = threshold

    def _build_graph(self, original_tokens):

        tokens = [w.lower() for w in original_tokens if w.lower(
        ) not in self.stopwords and not w.isnumeric()]
        g = Graph()
        edges = []

        g.add_vertices(tokens[0])
        for i in range(1, len(tokens)):
            if tokens[i] not in g.vs['name']:
                g.add_vertices(tokens[i])
                edge = sorted((tokens[i], tokens[i - 1]))
                if edge not in edges:
                    edges.append(edge)
            else:
                edge = sorted((tokens[i], tokens[i - 1]))
                if edge not in edges:
                    edges.append(edge)

        for i in range(len(tokens)):
            for j in range(len(tokens)):
                if i != j and tokens[i] != tokens[j]:
                    edge = sorted((tokens[i], tokens[j]))
                    if edge not in edges:
                        # TODO: change if we'll use weights
                        similarity = self.model.similarity(edge[0], edge[1])
                        if similarity > self.threshold:
                            edges.append(edge)
        g.add_edges(edges)
        return g

