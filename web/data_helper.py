'''
An interface to the underlying data.
'''
import numpy as np
import pandas as pd

from bs4 import BeautifulSoup 

import spacy
nlp = spacy.load("en_core_web_sm")

def get_sentences(text):
    #soup = BeautifulSoup(html) 
    #spacy_text =  nlp(soup.get_text())
    spacy_text =  nlp(text)
    return spacy_text.sents

def get_docs():
    # TODO generalize
    #df = pd.read_csv("../data/nhs_corona.csv")
    df = pd.read_csv("../data/bjgplife.csv")
    doc_texts, doc_urls, doc_titles = [], [], []
    # @TODO this is silly, sorry
    #import pdb; pdb.set_trace()
    for d, link, title in zip(df['text'].values, df['url'].values, df['title'].values):
        #try:

        doc_texts.append(list(get_sentences(d)))
        doc_urls.append(link)
        doc_titles.append(title)
        #except:
        #pass
    return doc_texts, doc_urls, doc_titles