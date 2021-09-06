from NetworkInterface import NetworkInterface
from bs4 import BeautifulSoup
import pprint
import sys


def connect(url, param):
    '''
    param:
    url = connect to the page desired to be crawled

    return:
    response object
    '''
    # connect to the page
    ni = NetworkInterface()
    res = ni.get(url, param)
    return res


def hack_news_digest(res, threshold=100):
    '''
    param:
    res = the response object by requests
    threshold = only scrape the artical with votes > threshold

    return:
    list of dictionary with structure
    [Dict(title='title', link='link', vote='123')]
    '''
    # convert to BeautifulSoup Obj
    soup = BeautifulSoup(res.text, 'html.parser')

    stories = soup.select('.storylink')
    subs = soup.select('.subtext')

    result_list = []
    for idx, story in enumerate(stories):
        item = {}
        # no score class
        if len(subs[idx].select('.score')) < 1:
            continue
        # no score value
        if len(subs[idx].select('.score')[0].contents) < 1:
            continue
        vote = int(subs[idx].select('.score')[
            0].contents[0].replace(' points', ' '))
        if vote < threshold:
            continue
        item['vote'] = vote
        item['link'] = story.get('href')
        item['title'] = story.contents[0]
        result_list.append(item)
    return result_list


def sort_result_list(result_list, key):
    return sorted(result_list, key=lambda item: item[key], reverse=True)


def main(depth):
    hns = []
    for p in range(0, depth):
        # connect to the page
        param = {'p': p}
        res = connect('https://news.ycombinator.com/news', param)

        # hacker_news_parser
        hns.extend(hack_news_digest(res, 300))

    # sort result by vote desc
    sorted_list = sort_result_list(hns, 'vote')
    pprint.pprint(sorted_list)


if __name__ == '__main__':

    try:
        depth = int(sys.argv[1])
    except ValueError as error:
        print('[error] first argument: how many pages you want to scrape ')
        exit()
    except IndexError:
        depth = 1
    main(depth)
