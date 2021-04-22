import json
import nltk
import random
import os
import re
import math
from collections import Counter
dir_path = os.path.dirname(os.path.realpath(__file__))
jsonPath = dir_path+'/../../../datasource/4300news.json'

with open(jsonPath, "r") as f:
    transcripts = json.load(f)

# pubDict: {'NYT':[[news],count],'guardian':[[news],count],......}
# kvList: [(NYT, [[list of news], count]),(Guardian,[[list of news],count]), ......]
kvList = list(transcripts.items())
newsList = []
for pub, lst in kvList:
    print(len(lst[0]))
    for news in lst[0]:
        newsList.append(news)
#print(newsList[0]['content'].lower())


def case_insensitive(query, searchContent):
    if query.lower() in searchContent.lower():
        return True
    else:
        return False
#print(case_insensitive('NEW', newsList[0]['content']))

def tokenize(searchContent):
    return [x for x in re.findall(r"[a-z]+", searchContent.lower())]
#print(tokenize(newsList[0]['content']))

#Cosine Similarity
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

# get_cos_similarity helper: convert string to vector
def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


def verbatim_search_on_title(query):
    result = []
    for news in newsList:
        title = news["title"]
        if query in title:
            result.append(title)
    return random.sample(result, 10)

