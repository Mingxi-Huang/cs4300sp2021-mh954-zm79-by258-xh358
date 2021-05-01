# add import
import os
import json
from nltk.tokenize import TreebankWordTokenizer
from collections import defaultdict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

dir_path = os.path.dirname(os.path.realpath(__file__))
jsonPath = dir_path+'/../../../datasource/categorized_news.json'

with open(jsonPath, "r") as f:
    newsList = json.load(f)

# print(len(newsList))
# print(newsList[0])


tfidf_vec = TfidfVectorizer(
    stop_words='english', max_df=0.8, min_df=10, max_features=5000)
tfidf_mat = tfidf_vec.fit_transform([d['title'] for d in newsList]).toarray()


def get_cos_sim(query, doc, tfidf_vec):
    """Returns the cosine similarity of two movie scripts.

    Params: {mov1: String,
             mov2: String,
             input_doc_mat: np.ndarray,
             movie_name_to_index: Dict}
    Returns: Float
    """
    # YOUR CODE HERE
    vec1 = tfidf_vec.fit_transform(query)
    vec2 = tfidf_vec.fit_transform(doc)
    dotprod = np.dot(vec1, vec2)
    v1_norm = np.linalg.norm(vec1)
    v2_norm = np.linalg.norm(vec2)
    return dotprod / (v1_norm * v2_norm)
