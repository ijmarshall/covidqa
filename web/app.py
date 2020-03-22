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
print("embedding all articles... ")
article_embeddings = retriever.embed_docs(doc_texts)#[:5])
print("done")

# Display all things
@app.route('/')
def show_main():
    return render_template('search.html', res_title=None, res_url=None)


@app.route('/', methods=['POST'])
def my_form_post():
    q = request.form['text']
    results = retriever.rank_for_q(q, article_embeddings)
    best_doc_idx = results[0][0]
    best_article_url = doc_urls[best_doc_idx]
    best_article_title = doc_titles[best_doc_idx]

    return render_template('search.html', res_title=best_article_title, res_url=best_article_url)
    


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
