import os
import time
import calendar
import requests
from urlparse import urlparse
from datetime import datetime
import MySQLdb as mdb
from crawler import CHROME_USER_AGENT
from bs4 import BeautifulSoup
from crawler.spider.ratelimiter import rate_limited


SPIDER_DATA = '/mnt/shxreader/spider/data'


def page_id_to_path(page_id, domain, timestamp):
    return '%s/%s/%s/%s' % (SPIDER_DATA, domain, timestamp.strftime('%Y-%m-%d'), page_id)


def lookup_page(url):
    con = mdb.connect('localhost', 'shxreader', 'shxreader', 'shxreader')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        prepared_statement = "select * from crawler where url = %s"
        r = cur.execute(prepared_statement, (url, ))
        if r > 0:
            return cur.fetchone()


def lookup_by_domain(domain):
    con = mdb.connect('localhost', 'shxreader', 'shxreader', 'shxreader')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        prepared_statement = "select * from crawler where domain = %s"
        r = cur.execute(prepared_statement, (domain, ))
        if r > 0:
            return cur.fetchall()


@rate_limited(1)
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
    timestamp = datetime.utcnow()
    directory = '%s/%s/%s/' % (SPIDER_DATA, domain, timestamp.strftime('%Y-%m-%d'))
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = page_id_to_path(page_id, domain, timestamp)
    with open(filename, 'w') as f:
        f.write(page_source.encode('utf-8'))


def crawl_and_store_page(url, user_agent=CHROME_USER_AGENT):
    if lookup_page(url) is not None:
        page_source = crawl_page(url, user_agent)
        store_page(url, page_source, user_agent)


# Analysis


def get_links(soup):
    links = [a['href'] for a in soup.findAll('a', href=True)]
    urls = [url for url in links if url.startswith('http')]
    return urls


def get_links_by_pageid(pageid):
    soup = BeautifulSoup(load_page(pageid))
    return get_links(soup)


def load_page_metadata(page_id):
    con = mdb.connect('localhost', 'shxreader', 'shxreader', 'shxreader')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        prepared_statement = "select * from crawler where id = %s"
        r = cur.execute(prepared_statement, (page_id, ))
        if r > 0:
            return cur.fetchone()


def load_page(page_id):
    d = load_page_metadata(page_id)
    if d is not None:
        domain = d['domain']
        datestamp = datetime.fromtimestamp(d['crawl_time'])
        filename = page_id_to_path(page_id, domain, datestamp)
        with open(filename) as f:
            return f.read()


if __name__ == '__main__':
    crawl_and_store_page(
        'http://stackoverflow.com/questions/2548493/in-python-after-i-insert-into-mysqldb-how-do-i-get-the-id')
