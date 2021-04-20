from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import os
import random

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
        data = verbatim_search_on_title(query)
    return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
