# Acknowledgement: use some codes in link:
# https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c

import requests
import pandas as pd
import pickle
import os
import numpy as np


def getClosestSubreddit(query, subredditList):
    minimum_dist = 10000
    minimum_name = ""
    for i in range(len(subredditList)):
        name = subredditList[i]
        dist = levenshteinDistanceDP(name, query)
        if dist == 0:
            return name
        if dist < minimum_dist:
            minimum_dist = dist
            minimum_name = name
    return minimum_name


def getRedditData(keyword):

    auth = requests.auth.HTTPBasicAuth(
        'L8EUKo7XiZpgyQ', '9a5BnUJdM7k_RiGjB-QfUVQP2liwcA')
    data = {'grant_type': 'password',
            'username': 'PlanAggravating7453',
            'password': 'Huangmingxi927'}

    headers = {'User-Agent': 'MyBot/0.0.1'}
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)
    TOKEN = res.json()['access_token']
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
    requests.get('https://oauth.reddit.com/api/v1/me', headers=headers).json()
    res = requests.get("https://oauth.reddit.com/r/{subreddit}/hot".format(subreddit=keyword),
                       headers=headers)

    df = pd.DataFrame()
    for post in res.json()['data']['children']:
        df = df.append({
            'subreddit': post['data']['subreddit'],
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            'num_comments': post['data']['num_comments'],
            'url': post['data']['url']
        }, ignore_index=True)
    srDict = df.to_dict()
    return srDict


def top_five(indexes, srDict):
    result = list()
    for ind in indexes:
        title = srDict['title'][ind]
        selftext = srDict['selftext'][ind] if len(
            srDict['selftext'][ind]) < 1000 else (srDict['selftext'][ind][:1000] + "...")
        url = srDict['url'][ind]
        result.append((title, selftext, url))
    return result


"""acknowledgement: https://blog.paperspace.com/implementing-levenshtein-distance-word-autocomplete-autocorrect/"""


def levenshteinDistanceDP(token1, token2):
    distances = np.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2

    a = 0
    b = 0
    c = 0

    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if (token1[t1-1] == token2[t2-1]):
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]

                if (a <= b and a <= c):
                    distances[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1
    return distances[len(token1)][len(token2)]


def getRedditResult(keyword):
    try:
        myDict = getRedditData(keyword)
        sortedByComment = sorted(
            list(myDict['num_comments'].items()), key=lambda x: x[1], reverse=True)
        indexes = []
        # print(myDict['selftext'])
        for i in sortedByComment[:5]:
            indexes.append(i[0])
        result = top_five(indexes, myDict)
        return result
    except:
        result = []
        return result


if __name__ == "__main__":
    pass
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # picklePath = dir_path+'/../../../datasource/subredditList.pkl'
    # with open(picklePath, 'rb') as f:
    #     subredditList = pickle.load(f)

    # # print(subredditList[0:10])
    # print(getClosestSubreddit("chelsea", subredditList))

    # sort them by number of comments

    # 0.num_comments 1. selftext 2. subreddit 3. title 4.url
    # result = getRedditResult("china")
