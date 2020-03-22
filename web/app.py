from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash

# from sqlalchemy import create_engine, asc, desc, \
#     func, distinct
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.serializer import loads, dumps

# from database_setup import Base, Things

import random
import string
import logging
import json
import httplib2
import requests

import data_helper 
import retriever 

app = Flask(__name__)


# Connect to database and create database session
# engine = create_engine('sqlite:///flaskstarter.db')
# Base.metadata.bind = engine

# DBSession = sessionmaker(bind=engine)
# session = DBSession()
doc_texts, doc_urls, doc_titles = data_helper.get_docs()
print("embedding all {} articles... ".format(len(doc_texts)))
article_embeddings = retriever.embed_docs(doc_texts)
print("done")

# Display all things
@app.route('/')
def show_main():
    return render_template('search.html', results=None)


@app.route('/', methods=['POST'])
def retrieve(k=5):
    q = request.form['text']
    results = retriever.rank_for_q(q, article_embeddings)

    titles, urls = [], []
    for i in range(k):
    	doc_idx = results[i][0]
    	titles.append(doc_titles[doc_idx])
    	urls.append(doc_urls[doc_idx])

    #import pdb; pdb.set_trace()
    return render_template('search.html', results=zip(titles, urls))
    


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
