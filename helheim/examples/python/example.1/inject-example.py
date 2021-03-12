#!/usr/bin/python3

# ------------------------------------------------------------------------------- #

import cloudscraper

# import'able helheim exceptions if you want to trap specific errors.
from helheim.exceptions import (
    HelheimException,
    HelheimSolveError,
    HelheimRuntimeError,
    HelheimSaaSError,
    HelheimSaaSBalance,
    HelheimVersion
)

from helheim import helheim, isChallenge

# ------------------------------------------------------------------------------- #

def injection(session, response):
    '''
    # use 'ignore' paramter to not trigger helheim....
    # (some sites put BFM into their overloaded pages etc)
    if isChallenge(
        response,
        ignore=[
            {
                'status_code': [403, 503], # list or int
                'text': ['text on page to match', ...] # list or str
            },
            {
                ...
            }
        ]
    ):
    '''
    if isChallenge(response):
        return helheim('place_your_apiKey_here', session, response)
    else:
        return response

# ------------------------------------------------------------------------------- #

# Documentation for cloudscraper https://github.com/venomous/cloudscraper/

session = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome', # we want a chrome user-agent
        'mobile': False, # pretend to be a desktop by disabling mobile user-agents
        'platform': 'windows' # pretend to be 'windows' or 'darwin' by only giving this type of OS for user-agents
    },
    requestPostHook=injection,
    # Add a hCaptcha provider if you need to solve hCaptcha
    #captcha={
    #    'provider': '...',
    #    'api_key': '....'
    #}
)

# ------------------------------------------------------------------------------- #

# uncomment the following if you don't want to solve BFM (Bot Fight Mode)
# https://blog.cloudflare.com/cleaning-up-bad-bots/
# session.disableBFM = True

# ------------------------------------------------------------------------------- #

# uncomment the following if you don't want to solve KPF
# session.disableKPF = True

# ------------------------------------------------------------------------------- #

# helheim is designed to NOT inherit the headers, proxies params on a request, it will only access the session.
# if you require to manually set the User-Agent or proxies, set them on the session not in the get().

# ie session.headers['User-Agent'] = '....'
# ie session.proxies = {'https': 'http://myproxy:8080'}

# ------------------------------------------------------------------------------- #

print(session.get('https://www.sneakersnstuff.com/en/product/42337/adidas-700').status_code)

