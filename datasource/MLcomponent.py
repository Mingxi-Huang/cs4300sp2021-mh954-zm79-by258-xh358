from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import json

# Business, Finance & Economics
# Computers, Science & Technology
# Entertainment, Art & Culture
# General News & Current Affairs
# Health & Medicine
# Lifestyle
# Sport & Leisure
# Trade & Professional

# dir_path = os.path.dirname(os.path.realpath(__file__))
# jsonPath = dir_path+'/../../../datasource/4300news.json'

with open("4300news.json", "r") as f:
    transcripts = json.load(f)

# pubDict: {'NYT':[[news],count],'guardian':[[news],count],......}
# kvList: [(NYT, [[list of news], count]),(Guardian,[[list of news],count]), ......]
kvList = list(transcripts.items())
newsList = []
newsTitleList = []
for pub, lst in kvList:
    for news in lst[0]:
        newsList.append(news)
        newsTitleList.append(news["title"])

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(newsTitleList)

true_k = 8
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=25, n_init=1)
model.fit(X)

order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()

if __name__ == "__main__":
    for i in range(true_k):
        print("Cluster %d:" % i)
        for ind in order_centroids[i, :10]:
            print('%s' % terms[ind])

    print("\n")
    print("Prediction")
    X = vectorizer.transform(
        ["Nothing is easy in cricket. Maybe when you watch it on TV, it looks easy. But it is not. You have to use your brain and time the ball."])
    predicted = model.predict(X)
    print(predicted)
