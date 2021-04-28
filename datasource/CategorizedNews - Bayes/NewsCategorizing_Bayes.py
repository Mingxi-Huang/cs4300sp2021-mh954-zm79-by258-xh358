# %%
import pandas as pd
import numpy as np 
from sklearn.naive_bayes import MultinomialNB  
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer,TfidfVectorizer
import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection   import train_test_split
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer as TFIDF
from pylab import *
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
nltk.download('stopwords')
nltk.download('wordnet')

# %%
f = open('News_Category_Dataset_train.json')
text = f.read()
f.close()
all_list = []
for j in text.split('\n'):
    try:
        all_list.append(eval(j))
    except:
        pass
train = pd.DataFrame(all_list)

# %%
cachedStopWords = stopwords.words("english")

# %%
#train

# %%
def removeStopword(x):
    text = x['headline']
    return  str(' '.join([lemmatizer.lemmatize(word).lower() for word in text.split() if word not in cachedStopWords]))
train['Phrasenostopword'] = train.apply(lambda x: removeStopword(x), axis=1)

# %%
train_xword = train['Phrasenostopword'].values.tolist()
vec = TFIDF()
X = vec.fit_transform(train_xword)

# %%
le = preprocessing.LabelEncoder()
y = le.fit_transform(train['category'])

# %%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state =1)

# %%
clf = MultinomialNB().fit(X_train, y_train)
clf.score(X_test,y_test)

# %%
clf.score(X_test,y_test)

# %%
times = 100
clfcrvs = MultinomialNB()
scores = cross_val_score(clfcrvs, X, y, cv=times)

# %%
#mpl.rcParams['font.sans-serif'] = ['SimHei']
#plt.title('Bayes Model')
#plt.xlabel("Times")
#plt.ylabel("Score")
#plt.plot(range(times), scores)

# %%
#predict

# %%
df_predict = pd.read_json('newsdata.json')

# %%
df_predict

# %%
def removeStopword(x):
    text = x['title']
    return  str(' '.join([lemmatizer.lemmatize(word).lower() for word in text.split() if word not in cachedStopWords]))
df_predict['Phrasenostopword'] = df_predict.apply(lambda x: removeStopword(x), axis=1)

# %%
xne = vec.transform(df_predict['Phrasenostopword'])

# %%
dir(clf)

# %%
df_predict['Category'] = le.inverse_transform(clf.predict(xne))

# %%
df_predict.to_json('categorized_news_data.json', orient='records', lines=True)

# %%
df_predict

# %%
list = []
for item in df['Category']:
    if item not in list:
        list.append(item)
print(list)

# %%
