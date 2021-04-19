import json
import nltk
import os
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
print(newsList[0])
