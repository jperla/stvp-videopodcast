import re

import BeautifulSoup

import spider

s = spider.Spider()
domain = 'http://edcorner.stanford.edu'
url = '/authorMaterialInfo.html?topicId=%s&d-5886639-p=%s'
topic = 1
page = 1

def links_on_page(html):
    soup = BeautifulSoup.BeautifulSoup(html)
    tbody = soup.find('table', {'id':'materialElement'}).tbody
    links = []
    for tr in tbody.findAll('tr'):
        tds = [td for td in list(tr.findAll('td'))]
        if tds[0].renderContents().lower() == 'video':
            links.append(tds[1].find('a')['href'])
    return links

def get_pages(topic=1):
    html = s.get(domain + url % (topic, page))
    soup = BeautifulSoup.BeautifulSoup(html)
    td = soup.find('td', {'class':'rightInfo'})
    page_numbers = [1]
    page_numbers.extend([int(a.renderContents()) for a in td.findAll('a')])
    num_pages = max(page_numbers)

    pages = [s.get(domain + url % (topic, pg)) for pg in range(1, num_pages+1)]
    return pages

def get_links_for_all_topics():
    links = [links_on_page(page) \
                for topic in range(1, 11+1) \
                    for page in get_pages(topic)]
    return links

def parse_out_mid(link):
    return s.get_match(link, 'mid=([0-9]+)')

def flatten(lists):
    new_list = []
    for l in lists:
        new_list.extend(l)
    return new_list
        
g = get_links_for_all_topics()
ids = set([parse_out_mid(link) for link in flatten(g)])


