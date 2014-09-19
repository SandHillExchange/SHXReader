from birdy.twitter import UserClient

import json
import logging

twitter_handle = 'SandHillXchange'
CONSUMER_KEY = 'b4VtpaXXJgoCiClAmogUZuvmW'
CONSUMER_SECRET = 'HAcuMk5ASRfhTqm4MqzJTKx8qkRzJhd5CPvrnGAiF4xhkj8xsP'
ACCESS_TOKEN = '135160644-oVs1EjTHyAHQ1JHKncLZ6bDI5vFGRmeW1qv2bbqF'
ACCESS_TOKEN_SECRET = 'pE42r9i3alXpATMPrnlJ36eRsQz6jWRhqVal66TRNDr2o'

def fetch_twitter():
    client = UserClient(CONSUMER_KEY,
                    CONSUMER_SECRET,
                    ACCESS_TOKEN,
                    ACCESS_TOKEN_SECRET)
    response = client.api.statuses.user_timeline.get(screen_name=twitter_handle, count=10)
    return response.data
