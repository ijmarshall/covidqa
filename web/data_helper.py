'''
An interface to the underlying data.
'''
import numpy as np
import pandas as pd

from bs4 import BeautifulSoup 

import spacy
nlp = spacy.load("en_core_web_sm")

def get_sentences(html):
    soup = BeautifulSoup(html) 
    spacy_text =  nlp(soup.get_text())
    return spacy_text.sents

def get_docs():
    df = pd.read_csv("../data/nhs_corona.csv")
    doc_texts, doc_html = [], []
    for d in df['text'].values:
        try:
            doc_texts.append(list(get_sentences(d)))
            doc_html.append(d)
        except:
            pass
    return doc_texts, doc_html