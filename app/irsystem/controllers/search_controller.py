import nltk
from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import os
import re
from collections import Counter
import math

# add import
import json
from nltk.tokenize import TreebankWordTokenizer
import string
from collections import defaultdict
from collections import Counter
import numpy as np
from app.irsystem.controllers.redditRequest import getRedditData, top_five, getRedditResult
from app.irsystem.controllers.new_search_method import build_inverted_index, compute_idf, compute_doc_norms, index_search

project_name = "Go!News"
net_id = "Simon Huang (mh954), Beining Yang(by258), Zhiqian Ma(zm79), Xirui He(xh358)"

dir_path = os.path.dirname(os.path.realpath(__file__))
jsonPath = dir_path+'/../../../datasource/categorized_news.json'

with open(jsonPath, "r") as f:
    newsList = json.load(f)

treebank_tokenizer = TreebankWordTokenizer()
for news in newsList:
    news['tokens'] = treebank_tokenizer.tokenize(news['title'].lower())
inv_idx = build_inverted_index(newsList)
idf = compute_idf(inv_idx, len(newsList),
                  min_df=15,
                  max_df_ratio=0.9)
inv_idx = {key: val for key, val in inv_idx.items()
           if key in idf}
doc_norms = compute_doc_norms(inv_idx, idf, len(newsList))


# def get_cos_similarity(vec_text1, vec_text2):
#     intersection = set(vec_text1.keys()) & set(vec_text2.keys())
#     numerator = sum([vec_text1[x] * vec_text2[x] for x in intersection])
#     sum1 = sum([vec_text1[x] ** 2 for x in list(vec_text1.keys())])
#     sum2 = sum([vec_text2[x] ** 2 for x in list(vec_text2.keys())])
#     denominator = math.sqrt(sum1) * math.sqrt(sum2)

#     if not denominator:
#         return 0.0
#     else:
#         return float(numerator) / denominator


# def text_to_vector(text):
#     words = WORD.findall(text)
#     return Counter(words)


# def sim_search(query):
#     qvec = text_to_vector(query)
#     result = []
#     for news in newsList:
#         title = news['title']
#         tvec = text_to_vector(title)
#         sim_measure = get_cos_similarity(qvec, tvec)
#         news['sim'] = sim_measure

#         result.append((news['title'],
#                       news['sim'], news['url']))
#     result = sorted(result, key=lambda x: x[1], reverse=True)
#     returnList = [(x[0], x[2], x[1]) for x in result]
#     return returnList[:10]


def getComments(keyword):
    data = getRedditResult(keyword=keyword)
    return data


@irsystem.route('/', methods=['GET'])
def search():
    query = request.args.get('search')
    if not query:
        reddit = []
        data = []
        context = dict()
        output_message = ''
    else:
        output_message = query
        lst = query.split(' ')
        reddit = []
        for word in lst:
            reddit_lst = getComments(word)
            for item in reddit_lst:
                reddit.append(item)
        newsRank = index_search(query, inv_idx, idf, doc_norms)
        newsResult = []
        for score, doc_id in newsRank[:10]:
            newsResult.append(
                (newsList[doc_id]['title'], newsList[doc_id]['url'], score))

        context = {
            'reddit': reddit,
            'news': newsResult
        }

    return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, context=context)
