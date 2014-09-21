"""API to send articles to shx
"""
import requests
NEWS_UPLOAD_ENDPOINT = 'http://sandhill.exchange/news/upload'


def post_to_shx(organizaton, url, headline):
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
    r = requests.post(NEWS_UPLOAD_ENDPOINT, data=json.dumps(payload))
