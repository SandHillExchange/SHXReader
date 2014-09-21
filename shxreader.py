#!/usr/bin/env python
"""SHXReader
"""
import owler.crawl as owler_crawler
import shx.api as shx_api

def run():
    # owler_crawler.run()
    results = owler_crawler.get_articles('warby-parker')
    for r in results:
        print r
        shx_api.upload_news(r['organization'], r['url'], r['headline'], r['timestamp'])
        break


def main():
    run()


if __name__ == '__main__':
    main()
