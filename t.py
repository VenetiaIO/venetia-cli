# import requests
# from tls.client import Session
# import requests
# from bs4 import BeautifulSoup

# print("session")
# session = Session()
# print("got session")
# for i in range(1):
#     url = f'https://www.footasylum.com/page/login/'
#     r = session.get(url,{})
#     soup = BeautifulSoup(r.text, "html.parser")
#     pre = soup.find('input',{'name':'prelog'})["value"]
    
#     payload = "target=&targetar=&pf_id=&sku=&rdPassword=LOGIN&prelog={}&lookup_Validate=1&email2={}&password={}".format(
#         pre,
#         "charliebottomley15@gmail.com",
#         "Cab200310"
#     )

#     response = session.post('https://www.footasylum.com/page/login/',headers={
#         'origin': 'https://www.footasylum.com',
#         'referer': 'https://www.footasylum.com/page/login/',
#         'sec-fetch-dest': 'document',
#         'sec-fetch-mode': 'navigate',
#         'sec-fetch-site': 'same-origin',
#         'sec-fetch-user': '?1',
#         'upgrade-insecure-requests': '1',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#         'accept-encoding': 'gzip, deflate, br',
#         'accept-language': 'en-US,en;q=0.9',
#         'content-type': 'application/x-www-form-urlencoded',
#     },data=payload)
#     # print(vars(response))

from utils.capMonster import capMonster

r = capMonster.v2('6LccSjEUAAAAANCPhaM2c-WiRxCZ5CzsjR_vd8uX', 'https://www.footlocker.co.uk/', 'proxies', 'FOOTLOCKER','UK')
print(r)