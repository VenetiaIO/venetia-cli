import requests
link = 'https://www.offspring.co.uk/view/product/offspring_catalog/5,1/4002896664'


success = 0
failed = 0
for i in range(100):
    try:
        currentVal = link.split('/offspring_catalog/')[1].split(',')[1].split('/')[0]
        link = link.replace(f'{currentVal}/',f'{i}/')
        retrieve = requests.get(link,headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-languag': 'en-US,en;q=0.9'
        })
        if retrieve.status_code == 200:
            success = success + 1
        if retrieve.status_code == 404:
            failed = failed + 1
        print('[{}] - Status: {}'.format(i, retrieve.status_code))
        # print(f'{i} | STATUS: ' + retrieve.status_code)
    except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
        print(e)


print("STATS")
print("TOTAL: 100")
print("FAILED: " + str(failed))
print("SUCCESS: " + str(success))
