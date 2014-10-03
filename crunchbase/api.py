""" Crunchbase API Library
"""
import json
from crunchbase import API_KEY


def fetch_json(identifier_url, identifier):
    url = identifier_url(identifier)
    result = urlfetch.fetch(url)
    if result.status_code == 200:
        return json.loads(result.content)


def organization_url(organization, user_key=API_KEY):
    """ generate organization api request url """
    return 'http://api.crunchbase.com/v/2/organization/%s?user_key=%s' % (organization, user_key)


def image_url(organization, user_key=API_KEY):
    """ generate image api request url """
    return 'http://api.crunchbase.com/v/2/organization/%s/primary_image?user_key=%s' % (organization, user_key)


def fetch_organization(organization):
    """ retrieve information about organization """
    return fetch_json(organization_url, organization)


def funding_round_url(uuid, user_key=API_KEY):
    """ generate funding round api request url """
    return "http://api.crunchbase.com/v/2/funding-round/%s?user_key=%s" % (uuid, user_key)


def fetch_funding_round(uuid):
    """ retrieve information about funding round """
    return fetch_json(funding_round_url, uuid)


def fetch_logo_url(organization):
    """ retrieve org logo url location """
    return fetch_json(image_url, organization)
