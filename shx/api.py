"""API to send articles to shx
"""
import requests
import json
NEWS_UPLOAD_ENDPOINT = 'http://sandhill.exchange/news/upload'


def upload_news(d):
    """Sends article information to shx

    Parameters
    ----------
    organizaton : str
        crunchbase organization name
    url : str
        url of article
    headline : str
        headline to display with url
    """
    payload = locals()
    try:
        json_data = json.dumps(d)
    except UnicodeDecodeError:
        json_data = json.dumps(d, ensure_ascii=False)
    r = requests.post(NEWS_UPLOAD_ENDPOINT, data=json_data)
