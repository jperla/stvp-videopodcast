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

def get_metadata(html):
    metadata = {}
    metadata['title'] = ''
    metadata['who'] = ''
    metadata['company'] = ''
    metadata['description'] = ''
    metadata['date'] = ''
    metadata['length'] = ''
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
    

mid = 736
html = get_video_page(mid)
metadata = get_metadata(html)
download_video(mid)

for id in ids:
    download_video(id)
    print 'sleeping'
    time.sleep(10)
    print 'done sleeping'
