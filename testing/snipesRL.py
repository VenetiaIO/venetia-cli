import requests
import random
import string
def loadProxy():
    try:
        with open(f'./data/gb.txt', 'r') as proxyIn:
            try:
                proxyInput = proxyIn.read().splitlines()
            except:
                return None
    except:
        return None

    if len(proxyInput) == 0:
        return None
    proxyList = [i for i in proxyInput]
    p = random.choice(proxyList)
    p = p.split(':')
    try:
        proxies = {
            'http': f'http://{p[2]}:{p[3]}@{p[0]}:{p[1]}',
            'https': f'https://{p[2]}:{p[3]}@{p[0]}:{p[1]}'
        }
    except:
        proxies = {
            'http': f'http://{p[0]}:{p[1]}',
            'https': f'https://{p[0]}:{p[1]}'
        }
    return proxies

p = loadProxy()
for i in range(10):
    headers = {
        'authority': 'www.snipes.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.snipes.com',
        'referer':'https://www.snipes.com/login',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    r = requests.post('https://www.snipes.com/add-product?format=ajax'.format(),headers=headers,proxies=p,data={
        'pid': '0001380185649800000004',
        'options': [],
        'quantity': 1
    })
    print('STATUS: [{}]'.format(r.status_code))