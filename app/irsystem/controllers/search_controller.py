import nltk
from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import os
import re
import random
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

project_name = "Go!News"
net_id = "Simon Huang (mh954), Beining Yang(by258), Zhiqian Ma(zm79), Xirui He(xh358)"

dir_path = os.path.dirname(os.path.realpath(__file__))
jsonPath = dir_path+'/../../../datasource/categorized_news.json'

with open(jsonPath, "r") as f:
    newsList = json.load(f)


def verbatim_search_on_title(query):
    result = []
    for news in newsList:
        title = news["title"]
        if query in title:
            result.append(title)
    if len(result) < 10:
        return result
    return random.sample(result, 10)

# print(kvList)


history = []


def hot_search(query):
    if query not in history:
        history.append(query)


def list_to_str(str_lst):
    result = ""
    index = 0
    for string in str_lst:
        result = result + (" " if index == 0 else ", ") + string
        index += 1
    return result


# -------------------------------
def tokenize(searchContent):
    return [x for x in re.findall(r"[a-z]+", searchContent.lower())]

# titleList = [x["title"] for x in news]


WORD = re.compile(r"\w+")


def get_cos_similarity(vec_text1, vec_text2):
    intersection = set(vec_text1.keys()) & set(vec_text2.keys())
    numerator = sum([vec_text1[x] * vec_text2[x] for x in intersection])
    sum1 = sum([vec_text1[x] ** 2 for x in list(vec_text1.keys())])
    sum2 = sum([vec_text2[x] ** 2 for x in list(vec_text2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


# Xirui adds another method
def word_to_vec_without_stopwords(text):
    WORD = re.compile(r"\w+")
    words = WORD.findall(text)
    clean_words = []
    for word in words:
        if word not in stopwords.words('english'):
            clean_words.append(word)
    return Counter(clean_words)


def get_first_sentence(content):
    contentList = content.split('.' + ' ')
    return contentList[0]


def sim_search(query):
    qvec = text_to_vector(query)
    result = []
    for news in newsList:
        title = news['title']
        tvec = text_to_vector(title)
        sim_measure = get_cos_similarity(qvec, tvec)
        news['sim'] = sim_measure
        news['first_sent'] = get_first_sentence(news['content']) + ' ...'
        result.append((news['title'], news['first_sent'],
                      news['sim'], news['url']))
    result = sorted(result, key=lambda x: x[2], reverse=True)
    returnList = [(x[0], x[3], x[2]) for x in result]
    return returnList[:10]


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
        #search_history = "Your search history:" + list_to_str(history)
        news = sim_search(query)

        context = {
            'reddit': reddit,
            'news': news
        }
        #data = index_search(query)
    return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, context=context)
