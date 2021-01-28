#!/usr/bin/python3

# ------------------------------------------------------------------------------- #

import cloudscraper
from helheim import helheim

# import'able helheim exceptions if you want to trap specific errors.
from helheim.exceptions import (
    HelheimException,
    HelheimSolveError,
    HelheimRuntimeError,
    HelheimSaaSError,
    HelheimSaaSBalance,
    HelheimVersion
)

# ------------------------------------------------------------------------------- #

def injection(session, response):
    if session.is_New_IUAM_Challenge(response) \
    or session.is_New_Captcha_Challenge(response) \
    or session.is_BFM_Challenge(response):
        return helheim('place_your_apiKey_here', session, response)
    else:
        return response

# ------------------------------------------------------------------------------- #

# Documentation for cloudscraper https://github.com/venomous/cloudscraper/

session = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'mobile': False,
        'platform': 'windows' # 'windows' or 'darwin' 
    },
    requestPostHook=injection,
    debug=False,
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

# helheim is designed to NOT inherit the headers, proxies params on a request, it will only access the session.
# if you require to manually set the User-Agent or proxies, set them on the session not in the get().

# ie session.headers['User-Agent'] = '....'
# ie session.proxies = {'https': 'http://myproxy:8080'}

# ------------------------------------------------------------------------------- #

print(session.get('https://www.sneakersnstuff.com/en/product/42337/adidas-700').status_code)

