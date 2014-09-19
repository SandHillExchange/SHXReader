""" This script runs as a cron job to send a list of URLs to the Queue for scraping
"""
import json

# News from crunchbase
CB_NEWS = 'http://api.crunchbase.com/v/2/organization/%s/news?user_key=%s'
# Websites from crunchbase
CB_WEB = 'http://api.crunchbase.com/v/2/organization/%s/websites?user_key=%s'
CB_KEY = '083267a8d507c32eef4f3bf791c5b6ce'

def get_cb_news(org):
    """ get org info by company
        input is crunchbase org name
    """
    org_url = CB_NEWS % (org, CB_KEY)

    try:
        cb = json.loads(urllib2.urlopen(org_url).read())
        data = cb.get('data')
    except:
        return None
    if not data:
        return None

    items = data.get('items')
    urls = []

    if items:
        for i in items:
            url = i.get('url')
            date = i.get('posted_on')       # date posted if TC article (useless?)
            created = i.get('created_at')   # epoch time for when CB posted the link

            # include some initial information
            # warren: remove if you only want urls
            data = {'url' : url,
                    'date': date,
                    'created': created,
                    'org': org }
            urls.append(data)

    return urls

def get_twitter_handle(org):
    """ get twitter handle
        input is crunchbase org name
    """
    org_url = CB_WEB % (org, CB_KEY)

    try:
        cb = json.loads(urllib2.urlopen(org_url).read())
        data = cb.get('data')
    except:
        return None
    if not data:
        return None

    items = data.get('items')

    if items:
        for i in items:
            # only pay attention to twitter for now
            title = i.get('title')
            if title and title == 'twitter':
                url = i.get('url')
                if url:
                    return url.split('/')[-1]
            else:
                continue
    return None
