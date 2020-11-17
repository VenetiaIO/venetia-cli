#!/usr/bin/python3

import cloudscraper
from helheim import helheim

# ------------------------------------------------------------------------------- #

def injection(session, response):
    if session.is_New_IUAM_Challenge(response) \
    or session.is_New_Captcha_Challenge(response):
        return helheim('place_your_apiKey_here', session, response)
    else:
        return response

# ------------------------------------------------------------------------------- #

scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'mobile': False,
        'platform': 'windows'
        #'platform': 'darwin'
    },
    requestPostHook=injection,
    debug=False
)

print(scraper.get('https://www.sneakersnstuff.com/en/product/42337/adidas-700').status_code)

