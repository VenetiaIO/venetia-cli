from helheim_cffi import ffi

import json
import cloudscraper
import sys
import os

sys.path.append(os.getcwd())
from helheim import helheim, isChallenge

# ------------------------------------------------------------------------------- #

def injection(session, response):
    if isChallenge(response):
        return helheim('place_your_apiKey_here', session, response)
    else:
        return response

# ------------------------------------------------------------------------------- #

@ffi.def_extern()
def getURL(url):
    session = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'mobile': False,
            'platform': 'windows'
        },
        requestPostHook=injection,
        allow_brotli=False # node GOT cant handle brotli
    )

    response = session.get(ffi.string(url).decode())

    return ffi.new(
        'char []',
        json.dumps(
            {
                'headers': session.headers,
                'cookies': session.cookies.get_dict()
            },
            indent=4
        ).encode()
    )

