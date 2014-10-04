import os
import time
import calendar
import requests
from urlparse import urlparse
from datetime import datetime
import MySQLdb as mdb
from crawler import CHROME_USER_AGENT


SPIDER_DATA = '/mnt/shxreader/spider/data'


def lookup_page(url):
    con = mdb.connect('localhost', 'shxreader', 'shxreader', 'shxreader')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        prepared_statement = "select * from crawler where url = %s"
        r = cur.execute(prepared_statement, (url, ))
        if r > 0:
            return cur.fetchone()


def crawl_page(url, user_agent=CHROME_USER_AGENT):
    headers = {'User-Agent': user_agent}
    resp = requests.get(url, headers=headers)
    return resp.text


def store_page(url, page_source, user_agent=CHROME_USER_AGENT):
    domain = urlparse(url).netloc

    # write meta_info
    con = mdb.connect('localhost', 'shxreader', 'shxreader', 'shxreader')
    with con:
        cur = con.cursor()
        prepared_statement = "insert into crawler VALUES(DEFAULT, %s, %s, NULL, %s, %s)"
        timestamp = calendar.timegm(time.gmtime())
        cur.execute(prepared_statement, (domain, url, user_agent, timestamp))
        page_id = cur.lastrowid

    # write source to file
    datestamp = datetime.utcnow().strftime('%Y-%m-%d')
    directory = '%s/%s/%s/' % (SPIDER_DATA, domain, datestamp)
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = '%s/%s/%s/%s' % (SPIDER_DATA, domain, datestamp, page_id)
    with open(filename, 'w') as f:
        f.write(page_source.encode('utf-8'))


def crawl_and_store_page(url, user_agent=CHROME_USER_AGENT):
    if lookup_page(url) is not None:
        page_source = crawl_page(url, user_agent)
        store_page(url, page_source, user_agent)


if __name__ == '__main__':
    crawl_and_store_page(
        'http://stackoverflow.com/questions/2548493/in-python-after-i-insert-into-mysqldb-how-do-i-get-the-id')
