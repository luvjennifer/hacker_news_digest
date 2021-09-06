from NetworkInterface import NetworkInterface
from bs4 import BeautifulSoup
import pprint


def article_info_by_id(id_list):
    result_list = []
    for id in id_list:
        link = soup.find(id=id).select('.title .storylink')[0].get('href')
        title = soup.find(id=id).select('.title .storylink')[0].contents[0]
        # vote = soup.find(id='score_'+id).contents[0]
        vote = int(
            soup.find(id='score_'+id).contents[0].replace(' points', ' '))
        result_list.append(dict(title=title, link=link, vote=vote))

    return result_list


def score_filter(threshold, score_list):
    '''
    params:
    threshold: display articles with points greater than this threshold
    score_list: all items with class=score

    return
    list of article ids which meet the requirement
    '''
    ids = []
    for item in score_list:
        if len(item.contents) < 1:
            continue
        if len(item.contents[0].split(' ')) < 2:
            continue
        #points > threshold
        if int(item.contents[0].split(' ')[0]) >= threshold:
            if len(item.get('id').split('score_')) < 2:
                continue
            ids.append(item.get('id').split('score_')[1])
    return ids


# connect to the page
ni = NetworkInterface()
res = ni.get('https://news.ycombinator.com/news')

# convert to BeautifulSoup Obj
soup = BeautifulSoup(res.text, 'html.parser')

# get aricle ids with points > 100 and grab their whole information
score_list = soup.select('.score')
ids = score_filter(100, score_list)
result_list = article_info_by_id(ids)

# sort by vote
pprint.pprint(sorted(result_list, reverse=True, key=lambda k: k['vote']))
