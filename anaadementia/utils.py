# -*- coding: utf-8 -*-
from nltk.tokenize import RegexpTokenizer
from gensim.matutils import unitvec
from xml.dom import minidom
import numpy as np

str_to_entailment = {'none': 0,
                    'entailment': 1,
                    'paraphrase': 2}
entailment_to_str = {v: k for k, v in str_to_entailment.items()}

stop_words = [
    'de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'com', 'uma',
    'os', 'no', 'se', 'na', 'por', 'mais', 'as', 'dos', 'como', 'mas', 'ao',
    'das', 'à', 'seu', 'sua', 'ou', 'quando', 'muito', 'já', 'também', 'só',
    'pelo', 'pela', 'até', 'isso', 'entre', 'depois', 'sem', 'mesmo', 'aos',
    'seus', 'quem', 'nas', 'me', 'esse', 'essa', 'num', 'nem', 'suas', 'meu',
    'às', 'minha', 'numa', 'pelos', 'qual', 'lhe', 'deles', 'essas', 'esses',
    'pelas', 'este', 'dele', 'tu', 'te', 'vocês', 'vos', 'lhes', 'meus',
    'minhas', 'teu', 'tua', 'teus', 'tuas', 'nosso', 'nossa', 'nossos', 'nossas',
    'dela', 'delas', 'esta', 'estes', 'estas', 'aquele', 'aquela', 'aqueles',
    'aquelas', 'isto', 'aquilo',
    'então',  'dai', 'daí', 'dum', 'duma', 'nesse', 'nisso', 'pois', 'assim'
]

content_words_tags = ['VAUX', 'V',
                      'PCP',
                      'N', 'NPROP',
                      'ADV', 'PDEN', 'PREP+ADV',
                      'ADJ']

def tokenize(text):
    """
    Script for tokenizing Portuguese text according to the Universal
    Dependencies (UD) tokenization standards. This script was not created by
    the UD team; it was based on observation of the corpus.
    https://gist.github.com/erickrf/d699b1a8c09249c36f74eaaa94690ccb
    """
    tokenizer_regexp = r'''(?ux)
    # the order of the patterns is important!!
    # more structured patterns come first
    [a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+|    # emails
    (?:https?://)?\w{2,}(?:\.\w{2,})+(?:/\w+)*|                  # URLs
    (?:[\#@]\w+)|                     # Hashtags and twitter user names
    (?:[^\W\d_]\.)+|                  # one letter abbreviations, e.g. E.U.A.
    (?:[DSds][Rr][Aa]?)\.|            # common abbreviations such as dr., sr., sra., dra.
    (?:\B-)?\d+(?:[:.,]\d+)*(?:-?\w)*|
        # numbers in format 999.999.999,999, possibly followed by hyphen and alphanumerics
        # \B- avoids picks as F-14 as a negative number
    \.{3,}|                           # ellipsis or sequences of dots
    \w+|                              # alphanumerics
    -+|                               # any sequence of dashes
    \S                                # any non-space character
    '''
    tokenizer = RegexpTokenizer(tokenizer_regexp)

    return tokenizer.tokenize(text)

def cosine_similarity(vec1, vec2):
    s = np.dot(
        unitvec(vec1),
        unitvec(vec2))
    return s


def get_answers(df_data, model, labels_with_sents):
    data_set_predictions = []
    for i in df_data.index:
        sentence = df_data.loc[i,'sentence']
        results_per_sentence = []
        for label, orignal_sent in labels_with_sents.items():
            y_probas = 0 if model.predict([[sentence, orignal_sent]])[0] == 0 else 1
            results_per_sentence.extend([y_probas])
        data_set_predictions.append(results_per_sentence)
    return np.asarray(data_set_predictions)

def read_xml(xml_path):
    xml = minidom.parse(xml_path)
    pairs = xml.getElementsByTagName('pair')
    train_data_sent1 = []
    train_data_sent2 = []
    train_y = []
    for i in pairs:
        train_data_sent1.append(i.getElementsByTagName('t')[0].childNodes[0].data.strip())
        train_data_sent2.append(i.getElementsByTagName('h')[0].childNodes[0].data.strip())
        train_y.append(str_to_entailment[i.attributes['entailment'].value.lower()])
    train_data = []
    for src_setences, trg_senteces in zip(train_data_sent1, train_data_sent2):
        train_data.append([src_setences, trg_senteces])
    train_data = np.asarray(train_data)
    return train_data, train_y