import re
import commands
import os
import time

import BeautifulSoup

import spider

s = spider.Spider()
domain = 'http://edcorner.stanford.edu'
url = '/authorMaterialInfo.html?mid=%s'

file_url = '/repository/%s.flv'

def get_video_page(mid):
    return s.get(domain + url % mid)

def get_metadata(mid):
    html = get_video_page(mid)
    soup = BeautifulSoup.BeautifulSoup(html)
    table = soup.find('table', {'class':'recTable'})

    metadata = {}
    metadata['id'] = mid

    metadata['title'] = table.find('div', {'class':'recTitle'}).renderContents()

    authors = table.find('li', {'id':'author'}).findAll('a')
    metadata['who'] = ', '.join([author.renderContents() for author in authors])

    metadata['company'] = table.find('li', {'id':'org'}).string.strip('\r\n\t ')

    description_div = table.find('div', {'class':'recDescription'})
    metadata['description'] = description_div.contents[2].strip('\r\n\t ')

    other = table.find('ul', {'id':'recMeta'}).find('table').tr.contents
    metadata['date'] = other[1].renderContents()

    metadata['length'] = other[3].renderContents().strip('\r\n\t ')
    return metadata

def download_video(mid):
    whole_url = domain + file_url % mid
    to_file = '/mnt/stvp/repository/%s.flv' % mid
    if os.path.exists(to_file):
        print 'File for %s already exists' % mid
    else:
        command = 'nohup wget -O %s %s' % (to_file, whole_url)
        print 'running commands %s' % command
        commands.getoutput(command)
    

#mid = 736
#m = get_metadata(mid); print m

import shelve
videos = shelve.open('shelf.videos', writeback=True)

#ids are in video_ids.py
for id in ids:
    id = str(id)
    if id not in videos:
        videos[id] = get_metadata(id)
        videos.sync()
videos.close()

'''
for id in ids:
    download_video(id)
    print 'sleeping'
    time.sleep(10)
    print 'done sleeping'
'''
