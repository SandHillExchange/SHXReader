#!/usr/bin/env python
import rss.feeds as rss_feeds
from redis import Redis
from rq import Queue
import crawler.spider as spyder
from crawler.spider import crawl_and_store_page
from urlparse import urlparse
from crawler import DOMAINS_TO_IGNORE


def queue_urls(urls):
    urls = filter_urls(urls)
    q = Queue(connection=Redis())
    for url in urls:
        if spyder.lookup_page(url) is None:
            result = q.enqueue(crawl_and_store_page, url)


def filter_urls(urls):
    urls = [url for url in urls if urlparse(url).netloc not in DOMAINS_TO_IGNORE]
    return urls


def crawl_deeper(domain):
    results = spyder.lookup_by_domain(domain)
    known_urls = set([r['url'] for r in results])
    urls = set()
    for r in results:
        urls = urls.union({url for url in spyder.get_links_by_pageid(r['id']) if url not in known_urls})
    return urls


def main():
    from rss import STANDARD_FEEDS
    for k in STANDARD_FEEDS:
        print k
        feed_url = STANDARD_FEEDS[k]
        urls = rss_feeds.urls_from_xml_feed(feed_url)
        queue_urls(urls)


    urls = rss_feeds.hacker_news()
    queue_urls(urls)


if __name__ == '__main__':
    main()
