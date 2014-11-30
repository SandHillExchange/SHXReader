
# coding: utf-8

# In[373]:

import nltk
from nltk.tokenize import sent_tokenize 
from nltk.util import ngrams
from nltk import word_tokenize
from collections import Counter
from nltk.corpus import stopwords
import pandas as pd
import os
from bz2 import BZ2File
import itertools
from bs4 import BeautifulSoup
import random
import re


# In[374]:

def extract(soup):
    d = {}
    d['title'] = soup.find('title').getText()
    canonial_url = soup.find('link', {'rel': 'canonical'})
    d['canonical_url'] = canonial_url['href'] if canonial_url else None
    soup = soup.find('div', {'class': 'article-entry'})
    if soup is None:
        return d
    [s.extract() for s in soup('script')]
    # techcrunch
    [s.extract() for s in soup.findAll('ul', {'class': 'social-list'})]
    [s.extract() for s in soup.findAll('div', {'class': 'l-sidebar'})]
    [s.extract() for s in soup('nav')]
    [s.extract() for s in soup.findAll('div', {'class': 'footer-social'})]
    text = soup.getText()
    # cleaning
    d['text'] = '\n'.join([l.strip().encode('utf-8') for l in text.split('\n') if len(l.strip()) > 0])
    return d


# In[375]:

filename = random.choice(os.listdir('/tmp/techcrunch.com/2014-10-04/'))
with BZ2File('/tmp/techcrunch.com/2014-10-04/' + filename) as f:
    soup = BeautifulSoup(f.read())


# In[376]:

pages_text = extract(soup)
with open('/tmp/soup.html', 'w') as f:
    f.write(str(soup))
print pages_text['text']


# In[377]:

pages = {}
for dirpath, dirnames, filenames in os.walk('/tmp/techcrunch.com/'):
    for name in filenames:
        filename = os.path.join(dirpath, name)
        with BZ2File(filename) as f:
            soup = BeautifulSoup(f.read())
            d = extract(soup)
            if d['canonical_url'] is not None:
                pages[d['canonical_url']] = d


# In[549]:

GOLDEN_FUNDING_SET = {
    'http://techcrunch.com/2013/10/08/luminate-health-raises-1m-to-make-patient-lab-results-comprehensible/': True,
    'http://techcrunch.com/2013/12/06/play-i-raises-1-4m-from-the-crowd-for-toy-robots-that-make-programming-kid-friendly-will-hit-stores-near-you-next-summer/': True,
    'http://techcrunch.com/2014/04/22/owlet-the-smart-baby-bootie-raises-1-85-million/': True,
    'http://techcrunch.com/2014/07/09/adheretech-raises-1-75-million-in-series-a/': True,
    'http://techcrunch.com/2014/09/17/splice-music-collaboration/': True,
    'http://techcrunch.com/2014/09/23/traxpay-raises-15m-teams-with-mastercard-to-be-the-paypal-of-the-b2b-world/': True,
    'http://techcrunch.com/2014/10/01/eve-raises-2-3m-to-rethink-programming/': True,
    'http://techcrunch.com/2014/10/03/crunchweek-windows-10-reddit-raises-a-fat-round-and-netflix-backs-adam-sandler/': True,
    'http://techcrunch.com/2014/10/03/estify-raises-1-5-million-to-roll-out-insurance-software-for-auto-repair/': True,
    'http://techcrunch.com/2014/10/03/investors-stay-silent-after-wonga-fiasco/': False,
    'http://techcrunch.com/2014/10/03/sourcery-raises-2-5m-to-connect-kitchens-and-local-food-suppliers/': True,
    'http://techcrunch.com/2014/10/03/yahoo-acquires-mobile-messaging-app-messageme/': False,
    'http://techcrunch.com/2014/09/30/shared-inbox-front-pulls-3-1-million-to-optimize-your-email-workflow/': True,
    'http://techcrunch.com/2014/11/04/gigya-raises-from-intel-capital/': True,
    'http://techcrunch.com/2014/11/11/chromecast-multiplayer-family-games/': False,
    'http://techcrunch.com/2014/07/29/fly-or-die-tinder-moments/': False,
    'http://techcrunch.com/2014/10/06/what-is-happening-to-bitcoin-right-now/': False,
    'http://techcrunch.com/2014/10/08/avaamo/': True,
    'http://techcrunch.com/2014/11/04/the-backbone-of-american-elections-pen-and-paper/': False,
    'http://techcrunch.com/2014/10/21/cloudflares-co-founders-talk-co-founders-investors-and-losing-at-tc-disrupt/': False,
    'http://techcrunch.com/2014/11/01/can-french-robotics-save-the-industry/': False,
    'http://techcrunch.com/2014/10/17/modcloth-hit-by-second-round-of-layoffs/': False,
    'http://techcrunch.com/2014/11/05/david-chang-maple/': True,
    'http://techcrunch.com/2014/10/09/amazons-dynamodb-gets-hugely-expanded-free-tier-and-native-json-support/': False,
    'http://techcrunch.com/2014/11/18/messaging-app-viber-takes-a-step-into-social-networking-with-new-public-chats-feature/': False,
    'http://techcrunch.com/2014/11/10/boop-messaging/': False,
    'http://techcrunch.com/2014/10/11/apple-pay-and-digital-currency-mean-time-is-running-out-for-physical-cash/': False,
    'http://techcrunch.com/2014/10/11/navigating-the-entrepreneurs-path/': False,
    'http://techcrunch.com/2014/10/07/yahoo-lays-off-employees-in-india-reportedly-up-to-2000-affected/': False,
    'http://techcrunch.com/2014/11/04/dasher-teams-up-with-venmo-to-bring-peer-to-peer-payments-to-its-messaging-app/': False,
    'http://techcrunch.com/2014/11/20/fastpay-funding-2/': True,
    'http://techcrunch.com/2014/11/12/microsoft-updates-visual-studio-2013-previews-next-major-release/': False,
    'http://techcrunch.com/2014/11/05/encoding-com-harmonic/': True,
    'http://techcrunch.com/2014/11/18/you-say-zomato/': True,
    'http://techcrunch.com/2014/11/13/kanvas-debuts-an-ios-keyboard-that-lets-you-send-decorated-photos-stickers-and-gifs-or-even-just-text/': False,
    'http://techcrunch.com/2014/11/04/checkoutsmart/' : True, 
    'http://techcrunch.com/2014/11/19/airware-ge/': True,
    'http://techcrunch.com/2014/11/09/99co/': True,
    'http://techcrunch.com/2014/11/10/coca-cola-hopes-its-startup-incubator-is-the-real-thing/': False,
    'http://techcrunch.com/2014/11/14/coinbase-desparately-seeking-series-c/': True,
    'http://techcrunch.com/2014/10/22/amazon-gets-more-enterprise-friendly-with-launch-of-aws-directory-service/': False,
    'http://techcrunch.com/2014/11/10/microsoft-office-apps-skyrocket-to-the-top-of-the-app-store-following-pricing-changes/':False,
    'http://techcrunch.com/2014/10/19/psa-you-wont-be-able-to-upgrade-the-new-mac-minis-ram-yourself/': False,
    'http://techcrunch.com/2014/11/04/chosen/': True,
    'http://techcrunch.com/2014/11/20/following-pressure-from-u-s-senate-uber-hires-data-privacy-expert-to-review-companys-policies/': False,
    'http://techcrunch.com/2014/11/12/vida-raises-1-3-million-for-socially-responsible-e-commerce/': True,
    'http://techcrunch.com/2014/10/05/pay-with-facebook-messenger/': False,
    'http://techcrunch.com/2014/10/06/ebay-to-host-live-art-auctions-on-new-site/': False,
    'http://techcrunch.com/2014/10/11/8-things-about-hardware-crowdfunding-we-learned-from-20-campaigns/': False,
    'http://techcrunch.com/2014/11/13/tubemogul-soars-14-after-reporting-strong-q3-revenue-of-27-4m-smaller-than-expected-loss/': False,
    'http://techcrunch.com/2014/10/20/grabtaxi-raises-65-million-to-increase-the-competition-with-uber-in-southeast-asia/': True,
    'http://techcrunch.com/2014/10/28/the-us-breeds-the-most-unicorns-but-the-rest-of-the-world-is-catching-up/': False,
    'http://techcrunch.com/2014/10/16/twitpic-couldnt-find-an-acquirer-will-shut-down-after-all-on-oct-25th/': False,
    'http://techcrunch.com/2014/10/07/israeli-startup-scene-thriving-despite-conflict/': False,
}


# In[550]:

def funding_features(article):
    title = article['title']
    d = {'has(series)': False, 'title_has(raises)': False}
    article_lowercase = article['text'].lower()
    d['title_starts_with(number)'] = True if re.match('\d', title) else False
    if re.search('series \w', article_lowercase) is not None:
        d['has(series)'] = True
    if re.search('raises', title.lower()) is not None:
        d['title_has(raises)'] = True
    unigrams = nltk.word_tokenize(article_lowercase.decode('utf-8'))
    c = Counter(unigrams)
    words = ['funding', 'investment', 'million', 'capital', 'raise', 
             'acquires','customer','support','shipping',
             'acquisition',
             'announced',
             'co-founder',
             'users',
             'download',
             'companies', 'businesses','report','trend','data','region',
             'strategic',
             'project','raising',
             'raised', 'talk', 'round', 'seed', 
             'angel','angels','investor','investors',
              'trading','shares','analyst','expectations',
              'valulation','venture',
              'free', 'partners','scientists','developer',
             'layoffs', 'i', 'you', 'cuts', 'app', 'billion', 'upgrade','facebook','ceo']
    for w in words:
        d['has(' + w + ')'] = w in c
    N = len(unigrams)
    d['length(<250)'] = True if N < 250 else False
    d['length(250-350)'] = True if N >= 250 and N < 350 else False
    d['length(350-500)'] = True if N >= 350 and N < 500 else False
    d['length(500-750)'] = True if N >= 500 and N < 750 else False
    d['length(750-1000)'] = True if N >= 750 and N < 1000 else False
    d['length(1000+)'] = True if N >= 1000 else False
    return d


# In[551]:

featuresets = [(funding_features(pages[url]), GOLDEN_FUNDING_SET[url]) for url in GOLDEN_FUNDING_SET]
random.shuffle(featuresets)
train_set, test_set = featuresets[:int(round(len(featuresets)*0.8))], featuresets[int(round(len(featuresets)*0.8)):]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))


# In[552]:

urls = [url for url in pages if 'text' in pages[url] and classifier.classify(funding_features(pages[url]))]
print len(urls)


# In[553]:

random.sample(urls, 10)


# In[542]:

filename = random.choice([os.path.join(dirpath, name) for dirpath, dirnames, filenames in os.walk('/tmp/techcrunch.com/')     for name in filenames])

with BZ2File(filename) as f:
    soup = BeautifulSoup(f.read())
    d = extract(soup)
d['canonical_url'], classifier.classify(funding_features(d)), funding_features(d),


# In[538]:

classifier.show_most_informative_features(10)


# In[543]:

len(pages)


# In[ ]:



