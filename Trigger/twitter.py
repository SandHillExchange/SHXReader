from birdy.twitter import UserClient

import json
import logging

CONSUMER_KEY = 'b4VtpaXXJgoCiClAmogUZuvmW'
CONSUMER_SECRET = 'HAcuMk5ASRfhTqm4MqzJTKx8qkRzJhd5CPvrnGAiF4xhkj8xsP'
ACCESS_TOKEN = '135160644-oVs1EjTHyAHQ1JHKncLZ6bDI5vFGRmeW1qv2bbqF'
ACCESS_TOKEN_SECRET = 'pE42r9i3alXpATMPrnlJ36eRsQz6jWRhqVal66TRNDr2o'

""" Fetch all tweets since a certain ID. We need to store the last id fetched
    for each company
"""

def fetch_twitter(twitter_handle, since):
    client = UserClient(CONSUMER_KEY,
                    CONSUMER_SECRET,
                    ACCESS_TOKEN,
                    ACCESS_TOKEN_SECRET)
    response = client.api.statuses.user_timeline.get(screen_name=twitter_handle, since_id=since)
    return response.data

def parse_twitter(data):
    """ search for urls in a tweet """
    entities = data.get('entities')
    if entities:
        urls = entities.get('urls')
        links = []
        for u in urls:
            if u.get('url'):
                links.append(u.get('url'))
        if len(links >0 ):
            return links
    return None
