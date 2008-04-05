import os
import datetime
import PyRSS2Gen

def get_videos():
    import shelve
    import random
    s = shelve.open('shelf.videos')
    ids = s.keys()
    #only get the ones that have been transcoded for iphone (mp4)
    ids = [id for id in ids if os.path.exists('/mnt/stvp/transcoded/%s.mp4' % id)]
    random.shuffle(ids)
    return [s[id] for id in ids]



def make_item(video):
    url = 'http://static.ivycall.com/stvp/transcoded/%s.mp4' % video['id']
    filesize = os.stat('/mnt/stvp/transcoded/%s.mp4' % video['id'])[6]
    item = PyRSS2Gen.RSSItem(
        title = '%s: %s' % (video['who'], video['title']),
        link = 'http://edcorner.stanford.edu/authorMaterialInfo.html?mid=%s' % video['id'],
        enclosure = PyRSS2Gen.Enclosure(url, filesize, 'video/mp4'),
        description = video['description'],
        guid = PyRSS2Gen.Guid('http://edcorner.stanford.edu/%s' % video['id']),
        pubDate = datetime.datetime.strptime(video['date'], '%Y-%m-%d'))
    return item

def make_rss(videos):
    rss = PyRSS2Gen.RSS2(
        title = 'Entrepreneurial Thought Leaders Videos (by Ivy Call)',
        link = 'http://www.ivycall.com/stvp/',
        description = '''Stanford Technology Ventures Program brings the world the Entrepreneurial Thought Leaders Series. The Entrepreneurial Thought Leaders lecture series takes place every Wednesday during the academic quarters.''',
        lastBuildDate = datetime.datetime.now(),
        items = [make_item(video) for video in videos])
    return rss

def sort_by_date_then_id(videos):
    videos = list(videos)
    def date_then_id(video, other):
        d1 = video['date']
        d2 = other['date']
        if d1 > d2:
            return -1
        elif d2 > d1:
            return 1
        else:
            i1 = video['id']
            i2 = other['id']
            if i1 > i2:
                return -1
            elif i2 > i1:
                return 1
            else:
                raise Exception('sorting same file?')
    videos.sort(date_then_id)
    return videos

videos = get_videos()
videos = sort_by_date_then_id(videos)


rss = make_rss(videos)

rss.write_xml(open('stvp.xml', 'w'))

