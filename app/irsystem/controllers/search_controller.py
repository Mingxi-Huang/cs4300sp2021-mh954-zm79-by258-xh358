from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import os
import re
import random
from collections import Counter
import math

#add import 
import json
from nltk.tokenize import TreebankWordTokenizer
import string
from collections import defaultdict
from collections import Counter
import numpy as np

project_name = "Go!News"
net_id = "Simon Huang (mh954), Beining Yang(by258), Zhiqian Ma(zm79), Xirui He(xh358)"

dir_path = os.path.dirname(os.path.realpath(__file__))
jsonPath = dir_path+'/../../../datasource/4300news.json'

with open(jsonPath, "r") as f:
    newsList = json.load(f)

# # Make nparray 
# with open("4300news.json") as f:
#     newsList = np.array(json.load(f))
# # Update with preprocess 
# def preprocess(query):
# #     Takes in a query (string) and returns a string with all lowercase and without punctuation.
#     query=query.lower()
#     text = "".join([ele for ele in query if ele not in string.punctuation and ele not in ["”", "—", "“",",","’"]])
#     return text

# count_label=0
# for item in newsList:
#     item["merged_content"]=preprocess(item["title"]+". "+item["content"])
#     item['article_index_number']=count_label
#     count_label+=1

# #add build inverted index 
# corpus={int(i['article_index_number']):i["merged_content"] for i in newsList}
# def build_inverted_index(news):
#     tok_dict=defaultdict(list)
#     for ind,txt in news.items():
#         word_counter=Counter(txt.split())
#         for word in word_counter.keys():
#             if word in tok_dict:
#                 tok_dict[word].append((ind,word_counter[word]))
#             else:
#                 tok_dict[word]=[(ind,word_counter[word])]
#     return tok_dict
# ind=build_inverted_index(corpus)
# # idf 
# def compute_idf(inv_idx, n_news=21000, min_df=10, max_df_ratio=0.95):
#     w_dict={}
#     for word in inv_idx.keys():
#         if len(inv_idx[word]) >=min_df and len(inv_idx[word])/n_news <= max_df_ratio:  
#             ratio=np.log2(n_news/(1+len(inv_idx[word])))
#             w_dict[word]=np.round(ratio,2)
#     return w_dict
# ind_to_idf=compute_idf(ind)

# #compute news norms(number of news =21000)
# def compute_news_norms(index, idf, n_news=21000):    
#     norms=np.zeros(n_news)
#     for word in idf.keys():
#         for i in range(len(index[word])):
#             norms[index[word][i][0]]+= ((index[word][i][1]*idf[word])**2)
#     return np.sqrt(norms)
# dnorms=compute_news_norms(ind,ind_to_idf)

# #use index search-cosine similarity to determine the similarity scores
# def index_search(query, index=ind, idf=ind_to_idf, news_norms=dnorms, tokenizer=TreebankWordTokenizer):
#     querytokenlist=TreebankWordTokenizer().tokenize(query.lower())
#     setquery = set(querytokenlist)
#     querynorm = 0
#     for word2 in setquery: 
#         if word2 in idf:
#             querynorm = querynorm + pow(querytokenlist.count(word2)*idf[word2], 2)
#     querynorm = np.sqrt(querynorm)
#     scorenews = np.zeros(news_norms.size, dtype=float)
#     scorelist = []
#     for word2 in setquery:
#         if word2 in index:
#             for (news_id, tf) in index[word2]:
#                 scorenews[news_id] = scorenews[news_id]+(querytokenlist.count(word2)*tf*idf[word2]*idf[word2])/(news_norms[news_id]*querynorm)
#     for i in range(0, scorenews.size):
#         scorelist.append((scorenews[i], i))
#     finalscorelist = sorted(scorelist, key= lambda x: x[0], reverse = True)
#     topscores= sorted(final, reverse=True)[:10]

#    # now only show the top scores and the id need to link the article id and get the title, publication, publication year and score
# #     topdic={score:[_______] for score, article_id in topscores} #may want to return the title, publication,publication year and score
#     return topscores

    

# pubDict: {'NYT':[[news],count],'guardian':[[news],count],......}
# kvList: [(NYT, [[list of news], count]),(Guardian,[[list of news],count]), ......]


# define new_search(query)
import nltk
def process_query(query):
    split_query = split


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


#-------------------------------
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


def get_first_sentence (content):
    contentList = content.split('.'+ ' ')
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
        result.append((news['title'], news['first_sent'], news['sim'], news['url']))
    result = sorted(result, key= lambda x : x[2], reverse=True)
    returnList = [(x[0], x[3], x[2]) for x in result]
    return returnList[:10]



@irsystem.route('/', methods=['GET'])
def search():
    query = request.args.get('search')
    if not query:
        data = []
        output_message = 'Please enter a valid keyword in the search bar'
    else:
        hot_search(query)
        output_message = "Your search: " + query 
        #search_history = "Your search history:" + list_to_str(history)
        data = sim_search(query)
        #data = index_search(query)
    return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)