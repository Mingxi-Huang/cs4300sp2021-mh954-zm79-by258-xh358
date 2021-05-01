# Acknowledgement: use some codes in link:
# https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c

import requests
import pandas as pd


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
            'ups': post['data']['ups'],
            'num_comments': post['data']['num_comments'],
            'url': post['data']['url']
        }, ignore_index=True)
    srDict = df.to_dict()
    return srDict


def top_five(indexes, srDict):
    result = list()
    for ind in indexes:
        title = srDict['title'][ind]
        selftext = srDict['selftext'][ind]
        url = srDict['url'][ind]
        result.append((title, selftext, url))
    return result


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

    # sort them by number of comments

    # 0.num_comments 1. selftext 2. subreddit 3. title 4.ups 5.url
    result = getRedditResult("china")
