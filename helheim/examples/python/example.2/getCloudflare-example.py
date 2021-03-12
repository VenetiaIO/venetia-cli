#!/usr/bin/python3

# ------------------------------------------------------------------------------- #

import argparse
import cloudscraper
import json

from helheim import helheim, isChallenge

# ------------------------------------------------------------------------------- #

def injection(session, response):
    if isChallenge(response):
        return helheim('place_your_apiKey_here', session, response)
    else:
        return response

# ------------------------------------------------------------------------------- #

parser = argparse.ArgumentParser(description='Helheim Example.')
parser.add_argument('-u', '--url', action='store', type=str, help='URL with IUAM / hCaptcha', required=True)
parser.add_argument('-p', '--proxy', action='store', type=str, help='proxy to use.', required=False)
parser.add_argument('-a', '--agent', action='store', type=str, help='User-Agent to use.', required=False)
parser.add_argument('-c', '--captcha', action='store', type=str, help='captcha parmeters in json format.', required=False)
parser.add_argument('-d', '--debug', action='store_true', help='Enable Debug', required=False, default=False)
parser.add_argument('--no-bfm', action='store_true', help='disable Bot Fight Mode', required=False, default=False)

args = parser.parse_args()

# ------------------------------------------------------------------------------- #

session = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'mobile': False,
        'platform': 'windows' # 'windows' or 'darwin'
    },
    requestPostHook=injection,
    captcha={} if not args.captcha else json.loads(args.captcha.replace("'", '"')),
    debug=args.debug
)

# ------------------------------------------------------------------------------- #

if args.no_bfm:
    session.disableBFM = True

# ------------------------------------------------------------------------------- #

if args.agent:
    session.headers['User-Agent'] = args.agent

# ------------------------------------------------------------------------------- #

if args.proxy:
    session.proxies = {
        'https': args.proxy,
        'https': args.proxy
    }

# ------------------------------------------------------------------------------- #

response = session.get(args.url)

print(
    json.dumps(
        {
            'headers': session.headers,
            'cookies': session.cookies.get_dict()
        },
        indent=4
    )
)

