# https://github.com/UKPLab/sentence-transformers
from sentence_transformers import SentenceTransformer
embedder = SentenceTransformer('bert-base-nli-mean-tokens')

from scipy.spatial.distance import cdist

import numpy as np 

def embed_doc(doc_sents, get_mean=True):
    doc_vecs = embedder.encode([s.string for s in doc_sents])
    if get_mean:
        return np.mean(doc_vecs, axis=0)
    return doc_vecs

def embed_docs(all_docs):
	article_embeddings = [embed_doc(doc) for doc in all_docs]
	return article_embeddings

def rank_for_q(q_str, doc_embeddings):
	query_embedding = embedder.encode([q_str])
	distances = cdist(query_embedding, doc_embeddings, "cosine")[0]
	results = zip(range(len(distances)), distances)
	results = sorted(results, key=lambda x: x[1])
	return results

def best_match_in_doc(q_v, doc_embeddings, k=5):
    distances = scipy.spatial.distance.cdist(q_v, doc_embeddings, "cosine")[0]
    results = zip(range(len(distances)), distances)
    results = sorted(results, key=lambda x: x[1])
    return results[:k]

