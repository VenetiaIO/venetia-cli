import requests
import uuid
from datetime import timezone, datetime

session = requests.session()
lastServed = None
for i in range(20):
    heads = {
        'host':'www.footlocker.co.uk',
        'origin':'https://www.footlocker.co.uk',
        "user-agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'upgrade-insecure-requests': '1',
        'x-fl-request-id': str(uuid.uuid1()),
        'cache-control': 'private, no-cache, no-store, must-revalidate, max-age=0, stale-while-revalidate=0',
        'pragma': 'no-cache',
        'Connection': 'close',
        "accept": "application/json",
        "accept-language": "en-US",
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'empty',
        'fastly-ff':''
    }
    if lastServed != None:
        heads['fastly-ff'] = str(lastServed)
    

    # self.session.get(self.baseUrl)
    # url = '{}/en/product/{}/{}.html'.format(self.baseUrl, self.task['PRODUCT'], self.task['PRODUCT'])
    url = '{}/api/products/pdp/{}?timestamp={}'.format('https://www.footlocker.co.uk', '314206076904', int(datetime.now(tz=timezone.utc).timestamp() * 1000))
    try:
        retrieveSizes = session.get(url,headers=heads)
    except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
        print(e)
    
    if retrieveSizes.headers['X-Served-By']:
        lastServed = retrieveSizes.headers['X-Served-By']
    else:
        lastServed = None


    print('{} <===> {}'.format(retrieveSizes.status_code,retrieveSizes.headers['X-Cache']))

