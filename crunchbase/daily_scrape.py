#!/usr/bin/env python
import calendar
import urllib
import datetime
import time
import json
import MySQLdb as mdb
import urllib3
import time


""" Daily scrapping to populate database manually
http://zetcode.com/db/mysqlpython/

Crunchbase API
    50 calls per minute, 2,500 calls per day

MySQL schema

CREATE TABLE `organization` (
    permalink VARCHAR(128),
    last_updated INT,
    data TEXT,
    PRIMARY KEY (permalink)
);

CREATE TABLE `funding_round` (
    uuid VARCHAR(128),
    last_updated INT,
    data TEXT,
    PRIMARY KEY (uuid)
);

select permalink, last_updated, FROM_UNIXTIME(last_updated) from organization order by last_updated asc limit 20;

select uuid, last_updated, FROM_UNIXTIME(last_updated) from funding_round;

Backup
$ mysqldump crunchbase > crunchbase.sql -uroot

"""


API_KEY = '630c1e7df986a42da0cdbfa3e10013f2' # Warren's API Key
DB_USERNAME = 'crunchbase'
DB_PASSWORD = 'crunchbase'
DB_TABLE = 'crunchbase'
RATE_LIMIT = 50.0/60.0*0.85 # qps or 50 calls per minute, 2,500 calls per day

http = urllib3.PoolManager()


def fetch_json(identifier_url, identifier):
    """ fetch data from crunchbase api with rate limit
    """
    url = identifier_url(identifier)
    start_time = time.time()
    r = http.request('GET', url)
    elapsed_time = time.time() - start_time
    min_time = 1.0/RATE_LIMIT
    if (elapsed_time < min_time):
        time.sleep(min_time - elapsed_time)
    return json.loads(r.data)


def organizations_url(parameters, user_key=API_KEY):
    page_num = parameters['page']
    order = parameters['order']
    return "http://api.crunchbase.com/v/2/organizations?user_key=%s&page=%i&order=%s" % (user_key, page_num, order)


def fetch_organizations(page_num=1, order='updated_at+DESC'):
    """ retrieve information about organizations """
    return fetch_json(organizations_url, {'page': page_num, 'order': order})


def organization_url(organization, user_key=API_KEY):
    """ generate organization api request url """
    return 'http://api.crunchbase.com/v/2/organization/%s?user_key=%s' % (organization, user_key)


def fetch_organization(organization):
    """ retrieve information about organization """
    return fetch_json(organization_url, organization)


def funding_round_url(uuid, user_key=API_KEY):
    """ generate funding round api request url """
    return "http://api.crunchbase.com/v/2/funding-round/%s?user_key=%s" % (uuid, user_key)


def fetch_funding_round(uuid):
    """ retrieve information about funding round """
    return fetch_json(funding_round_url, uuid)


def download_organizations(filename):
    with open(filename, 'w') as fout:
        fout.write('%s\n' % json.dumps(fetch_organizations(page)))


def update_organizations():
    for i in range(0, 10):
        d = fetch_organizations(i)
        con = mdb.connect('localhost', DB_USERNAME, DB_PASSWORD, DB_TABLE);
        cur = con.cursor()
        try:
            count = 0
            for item in d['data']['items']:
                count = count + 1
                organization = item[u'path'].replace('organization/', '').encode('utf-8')
                updated_at = item[u'updated_at']
                try:
                    update_organization(cur, organization, updated_at)
                    if count%10 == 0:
                        con.commit()
                except ValueError:
                    print 'error for ' + organization
        finally:
            con.commit()
            con.close()


def update_organization(cur, organization, updated_at):
    print organization
    cur.execute("SELECT last_updated from organization where permalink=%s", organization)
    result = cur.fetchone()
    fetch = False
    if result is None:
        fetch = True
    else:
        last_updated = result[0]
        if int(updated_at) > int(last_updated):
            fetch = True
    if fetch:
        # new entry
        d = fetch_organization(organization)
        # handle case where there is an error
        if 'data' not in d:
            return
        if 'response' in d['data'] and d['data']['response'] == False:
            return
        if 'properties' not in d['data']:
            return
        last_updated = d['data']['properties']['updated_at']
        cur.execute("INSERT INTO organization (permalink, last_updated, data) values (%s, %s, %s) ON DUPLICATE KEY UPDATE last_updated=VALUES(last_updated), data=VALUES(data)", (organization, last_updated, json.dumps(d)))
        # update funding rounds
        update_funding_round_from_organization_dict(cur, d)


def update_funding_round(cur, uuid, updated_at):
    print uuid
    cur.execute("SELECT last_updated from funding_round where uuid=%s", uuid)
    result = cur.fetchone()
    fetch = False
    if result is None:
        fetch = True
    else:
        last_updated = result[0]
        if int(updated_at) > int(last_updated):
            fetch = True
    if fetch:
        # new entry
        d = fetch_funding_round(uuid)
        last_updated = d['data']['properties']['updated_at']
        cur.execute("INSERT INTO funding_round (uuid, last_updated, data) values (%s, %s, %s) ON DUPLICATE KEY UPDATE last_updated=VALUES(last_updated), data=VALUES(data)", (uuid, last_updated, json.dumps(d)))


def update_funding_round_from_organization_dict(cur, d):
    if u'funding_rounds' in d[u'data'][u'relationships']:
        for item in d[u'data'][u'relationships'][u'funding_rounds'][u'items']:
            uuid = item[u'path'].replace('funding-round/','')
            updated_at = item[u'updated_at']
            update_funding_round(cur, uuid, updated_at)


def update_funding_round_for_organization(cur, organization):
    cur.execute("SELECT data from organization where permalink=%s", organization)
    result = cur.fetchone()
    if result is None:
        return
    d = json.loads(result[0])
    update_funding_round_from_organization_dict(cur, d)


def main():
    print 'daily scrape'
    update_organizations()
    # get organizations
    # timestamp = calendar.timegm(time.gmtime())
    # timestamp = 1404884824
    # filename = 'organizations-%i.tsv' % timestamp
    # download_organizations(filename)

    # organization = 'talnts-inc'
    # d = fetch_organization(organization)
    # with open('organization-%i.tsv' % timestamp, 'w') as fout:
        # fout.write('%s\t%s\n' % (organization, json.dumps(d)))


if __name__ == '__main__':
    main()
