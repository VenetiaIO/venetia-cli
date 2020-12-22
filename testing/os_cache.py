import requests

link = 'https://www.offspring.co.uk/view/product/offspring_catalog/5,21/4002896664'

for i in range(15):
    try:
        retrieve = requests.get(link,headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-languag': 'en-US,en;q=0.9'
        })
    except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
        pass

    print(retrieve.headers['X-Cache-Action'])