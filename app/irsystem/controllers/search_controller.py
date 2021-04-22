from app.irsystem.controllers.helper import tokenize
from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import os
import re
import random
from collections import Counter
import math

project_name = "Go!News"
net_id = "Simon Huang (mh954), Beining Yang(by258), Zhiqian Ma(zm79), Xirui He(xh358)"

dir_path = os.path.dirname(os.path.realpath(__file__))
jsonPath = dir_path+'/../../../datasource/4300news.json'

with open(jsonPath, "r") as f:
    transcripts = json.load(f)

# pubDict: {'NYT':[[news],count],'guardian':[[news],count],......}
# kvList: [(NYT, [[list of news], count]),(Guardian,[[list of news],count]), ......]
kvList = list(transcripts.items())
newsList = []
for pub, lst in kvList:
    for news in lst[0]:
        newsList.append(news)


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


def sim_search(query):
    qvec = text_to_vector(query)
    result = []
    for news in newsList:
        title = news['title']
        tvec = text_to_vector(title)
        sim_measure = get_cos_similarity(qvec, tvec)
        news['sim'] = sim_measure
        result.append((news['title'], news['content'], news['sim']))
    result = sorted(result, key= lambda x : x[2], reverse=True)
    returnList = [(x[0], x[2]) for x in result]
    return returnList[:10]



@irsystem.route('/', methods=['GET'])
def search():
    query = request.args.get('search')
    if not query:
        data = []
        output_message = 'Please enter a valid keyword in the search bar'
    else:
        hot_search(query)
        output_message = "Your search: " + query + "---" + \
            "Your search history:" + list_to_str(history)
        data = sim_search(query)
    return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
