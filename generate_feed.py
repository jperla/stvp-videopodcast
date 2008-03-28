import datetime
import PyRSS2Gen

def get_some_random_videos():
    import shelve
    import random
    s = shelve.open('shelf.videos')
    ids = s.keys()
    random.shuffle(ids)
    return [s[id] for id in ids[:3]]

#videos = get_some_random_videos()


rss = PyRSS2Gen.RSS2(
        title = 'Entrepreneurial Thought Leaders Videos (by Ivy Call)',
        link = 'http://www.ivycall.com/stvp',
        description = '''Stanford Technology Ventures Program brings the world the Entrepreneurial Thought Leaders Series. The Entrepreneurial Thought Leaders lecture series takes place every Wednesday during the academic quarters.''',
        lastBuildDate = datetime.datetime.now(),

        items = [
            PyRSS2Gen.RSSItem(
                title = video['title'],
                link = 'http://edcorner.stanford.edu/repository/%s.flv' % video['id'],
                enclosure = PyRSS2Gen.Enclosure('http://edcorner.stanford.edu/repository/%s.flv' % video['id'], 100, 'video/flv'),
                description = video['description'],
                guid = PyRSS2Gen.Guid('http://edcorner.stanford.edu/%s' % video['id']),
                pubDate = datetime.datetime.now()) \
                        for video in videos])

rss.write_xml(open('final.xml', 'w'))

