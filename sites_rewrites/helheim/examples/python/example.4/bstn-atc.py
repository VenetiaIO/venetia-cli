#!/usr/bin/python3
import re
import cloudscraper

from helheim import helheim, isChallenge

# ------------------------------------------------------------------------------- #

def injection(session, response):
    if isChallenge(response):
        return helheim('your_api_key_here', session, response)
    else:
        return response

# ------------------------------------------------------------------------------- #

session = cloudsession.create_session(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'mobile': False
    },
    requestPostHook=injection
)

# ------------------------------------------------------------------------------- #

baseURL = 'https://www.bstn.com'

# ------------------------------------------------------------------------------- #
# Get page that has the fingerprint challenge and the form key (after solving)
response = session.get(f'{baseURL}/eu_it/p/hi-tec-hts-bw-infinity-k010003-011-0108963')

# ------------------------------------------------------------------------------- #
# ATC

response = session.post(
    f"{baseURL}/eu_it/amasty_cart/cart/add/",
    data={
        'product': 51574,
        'selected_configurable_option': '',
        'related_product': '',
        'item': 51574,
        'alert_type': '',
        'form_key': session.cookies['form_key'], # form_key is popualed into cookies via helheim automatically
        'super_attribute[203]': 6341,
        'super_attribute[205]': 6364,
        'super_attribute[204]': 6339,
        'qty': 1,
        'kpsdkCt': session.kpf['x-kpsdk-ct'], # kpf is populated by helheim automatically
        'kpsdkFp': session.kpf['x-kpsdk-fp'],
        'challengeID': session.kpf['challengeID'],
        'challengeAnswer': session.kpf['challengeAnswer'],
        'product_page': True
    },
    headers={
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': f'{baseURL}/eu_it/p/hi-tec-hts-bw-infinity-k010003-011-0108963'
    }
)

# ------------------------------------------------------------------------------- #
# get Checkout page that contains challenge trigger so helheim solves it...

response = session.get(f'{baseURL}/eu_it/checkout/')

# ------------------------------------------------------------------------------- #

cartID = re.search(
    r'''"quoteData":{"entity_id":"(\w+)",''',
    response.text,
    re.M | re.S
).group(1)

print(f"cart id -> {cartID}")

# ------------------------------------------------------------------------------- #

response = session.post(
    f"{baseURL}/eu_it/rest/eu_it/V1/customers/isEmailAvailable",
    json={
        'customerEmail': 'blah123433@blah.com'
    },
    headers={
        'X-Requested-With': 'XMLHttpRequest',
    }
)

# ------------------------------------------------------------------------------- #

response = session.post(
    f"{baseURL}/eu_it/rest/eu_it/V1/guest-carts/{cartID}/estimate-shipping-methods",
    json={
        "address": {
            "street": ["blah","32"],
            "city":"blah blah",
            "region":"",
            "country_id": "DE",
            "postcode":"21234",
            "firstname":"blah",
            "lastname":"",
            "company":"",
            "telephone":"blah",
            "custom_attributes": [{"attribute_code":"gender","value":"1"}]
        }
    },
    headers={
        'X-Requested-With': 'XMLHttpRequest'
    }
)

# ------------------------------------------------------------------------------- #
# etc... etc...

