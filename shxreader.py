#!/usr/bin/env python
"""SHXReader
"""
from random import shuffle
import owler.crawl as owler_crawler
from owler import ORGANIZATION_TO_URL
import shx.api as shx_api


def run():
    owler_crawler.run()
    organization = ORGANIZATION_TO_URL.keys()
    shuffle(organization)
    for organization in organization:
        results = owler_crawler.get_articles(organization)
        for r in results:
            print r
            shx_api.upload_news(r)


def main():
    run()


if __name__ == '__main__':
    main()
