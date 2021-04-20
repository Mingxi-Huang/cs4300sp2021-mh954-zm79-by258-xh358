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
    return random.sample(result, 10)


def social_component_hotsearch_pm03(query):
    querySearchHistory = []
    if query not in querySearchHistory:
        querySearchHistory.append(query)
    return querySearchHistory



@irsystem.route('/', methods=['GET'])
def search():
    query = request.args.get('search')
    if not query:
        data = []
        output_message = 'Please enter a valid keyword in the search bar'
    else:
        output_message = "Your search: " + query
        data = social_component_hotsearch_pm03(query) + verbatim_search_on_title(query)
    return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
