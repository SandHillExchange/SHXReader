import os
import time
import calendar
import requests
from urlparse import urlparse
from datetime import datetime
import MySQLdb as mdb
from bz2 import BZ2File
from crawler import CHROME_USER_AGENT
from bs4 import BeautifulSoup
from crawler.ratelimiter import rate_limited
from nltk.tokenize import sent_tokenize
from nltk.util import ngrams
from nltk import word_tokenize
from collections import Counter
from nltk.corpus import stopwords
import itertools


SPIDER_DATA = '/mnt/shxreader/spider/data'


def page_id_to_path(page_id, domain, timestamp):
    return '%s/%s/%s/%s.bz2' % (SPIDER_DATA, domain, timestamp.strftime('%Y-%m-%d'), page_id)


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
    with BZ2File(filename, 'w') as f:
        f.write(page_source.encode('utf-8'))


def crawl_and_store_page(url, user_agent=CHROME_USER_AGENT):
    if lookup_page(url) is None:
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


def get_text(soup):
    [s.extract() for s in soup('script')]
    text = soup.getText()
    # cleaning
    text = '\n'.join([l.strip() for l in text.split('\n') if len(l.strip()) > 0])
    return text


stop = stopwords.words('english')


def ngram_count(text, n=1):
    l = []
    sentences = [sent_tokenize(s) for s in text.split('\n')]
    sentences = itertools.chain(*sentences)
    for s in sentences:
        valid_grams = [' '.join(gram) for gram in ngrams(word_tokenize(s), n) if gram[0] not in stop and gram[-1] not in stop]
        l.extend(valid_grams)
    return l


if __name__ == '__main__':
    crawl_and_store_page(
        'http://stackoverflow.com/questions/2548493/in-python-after-i-insert-into-mysqldb-how-do-i-get-the-id')
