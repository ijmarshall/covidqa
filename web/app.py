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
doc_texts, doc_html = data_helper.get_docs()
print("embedding all articles... ")
article_embeddings = retriever.embed_docs(doc_texts[:5])
print("done")

# Display all things
@app.route('/')
def show_main():
    return render_template('search.html')


@app.route('/', methods=['POST'])
def my_form_post():
    q = request.form['text']
    results = retriever.rank_for_q(q, article_embeddings)
    best_article = doc_html[results[0][0]]

    import pdb; pdb.set_trace()


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
