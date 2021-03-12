import requests,json,re,time,random,aiohttp,asyncio,httpx,os,csv,sys
from bs4 import BeautifulSoup
import urllib3
from urllib3.exceptions import InsecureRequestWarning 
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from logger import logger
# from utils.webhook import discord
# from utils.log import log
# from utils.datadome import datadome
# from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies, updateConsoleTitle,scraper, footlocker_snare)

SITE = 'Footlocker'
class Footlocker():

    def __init__(self, task, taskName, rowNumber):
        self.task = task
        self.session = requests.session()
        self.taskID = taskName
        self.rowNumber = rowNumber
        self.blocked = False

        # profile = loadProfile(self.task["PROFILE"])
        profile = {
            "countryCode":"GB"
        }
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()

        self.countryCode = profile['countryCode'].lower()

        # self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
        self.proxies = None
        self.baseSku = self.task['PRODUCT']

        if self.countryCode == 'fr':
            self.baseUrl = 'https://www.footlocker.fr'
            self.baseUrl2 = 'https://www.footlocker.de/INTERSHOP/web/FLE/Footlocker-Footlocker_FR-Site/en_GB/-/EUR/'
        if self.countryCode == 'de':
            self.baseUrl = 'https://www.footlocker.de'
            self.baseUrl2 = 'https://www.footlocker.de/INTERSHOP/web/FLE/Footlocker-Footlocker_DE-Site/de_DE/-/EUR/'
        if self.countryCode == 'nl':
            self.baseUrl = 'https://www.footlocker.nl'
            self.baseUrl2 = 'https://www.footlocker.de/INTERSHOP/web/FLE/Footlocker-Footlocker_NL-Site/en_GB/-/EUR/'
        if self.countryCode == 'gb':
            self.baseUrl = 'https://www.footlocker.co.uk'
            self.baseUrl2 = 'https://www.footlocker.co.uk/INTERSHOP/web/FLE/Footlocker-Footlocker_GB-Site/en_GB/-/GBP/'
        if self.countryCode == 'au':
            self.baseUrl = 'https://www.footlocker.com.au'
            self.baseUrl2 = 'https://www.footlocker.com.au/INTERSHOP/web/FLE/Footlocker-Footlocker_AU-Site/en_GB/-/AUD/'
        if self.countryCode == 'sg':
            self.baseUrl = 'https://www.footlocker.co.uk'
            self.baseUrl2 = 'https://www.footlocker.sg/INTERSHOP/web/FLE/FootlockerAsiaPacific-Footlocker_SG-Site/en_GB/-/SGD/'
        if self.countryCode == 'my':
            self.baseUrl = 'https://www.footlocker.my'
            self.baseUrl2 = 'https://www.footlocker.my/INTERSHOP/web/FLE/FootlockerAsiaPacific-Footlocker_MY-Site/en_GB/-/MYR/'
        if self.countryCode == 'hk':
            self.baseUrl = 'https://www.footlocker.hk'
            self.baseUrl2 = 'https://www.footlocker.hk/INTERSHOP/web/FLE/FootlockerAsiaPacific-Footlocker_HK-Site/en_GB/-/HKD/'

        self.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'

    async def build_proxy(self):
        self.proxy = None
        if self.proxies == [] or not self.proxies:
            return None
        self.px = random.choice(self.proxies)
        self.splitted = self.px.split(':')
        if len(self.splitted) == 2:
            self.proxy = 'http://{}'.format(self.px)
            return None
        
        elif len(self.splitted) == 4:
            self.proxy = 'http://{}:{}@{}:{}'.format(self.splitted[2], self.splitted[3], self.splitted[0], self.splitted[1])
            return None
        else:
            await self.error('Invalid proxy: "{}", rotating'.format(self.px))
            return None

    async def tasks(self):
        # await self.build_proxy()
        
        async with httpx.AsyncClient(proxies=self.proxies,timeout=None) as self.session:
            await self.log()
            await self.req()
            # await self.scrape()
            # await self.atc()
            # await self.getCheckout()
            # await self.submitShipping()
            # await self.submit_payment()

    async def retrieveSizes(self):
        while True:
            logger.prepare(SITE,self.taskID,'Getting product data...')
            self.start = time.time()
            self.relayCat = 'Relay42_Category'  #soup.find('input',{'value':'Product Pages'})['name']
            self.productImage = f'https://images.footlocker.com/is/image/FLEU/{self.baseSku}_01?wid=763&hei=538&fmt=png-alpha'
            # self.session.get(self.baseUrl)
            try:
                retrieveSizes = self.session.get(f'{self.baseUrl2}ViewProduct-ProductVariationSelect?BaseSKU={self.baseSku}&InventoryServerity=ProductDetail',headers={
                    "accept": "application/json, text/javascript, */*; q=0.01",
                    "accept-language": "en-US,en;q=0.9",
                    "sec-ch-ua": "\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "x-requested-with": "XMLHttpRequest",
                    "user-agent":self.userAgent
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

            if retrieveSizes.status_code == 503:
                logger.info(SITE,self.taskID,'Queue...')
                time.sleep(10)
                continue

            if retrieveSizes.status_code == 404:
                logger.error(SITE,self.taskid,'Sold Out. Retrying...')
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

            if retrieveSizes.status_code == 403:
                logger.error(SITE,self.taskID,'Blocked by DataDome (Solving Challenge...)')
                try:
                    challengeUrl = retrieveSizes.json()['url']
                    cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'])
                    while cookie['cookie'] == None:
                        cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'])
                        
                    del self.session.cookies["datadome"]
                    # cookie_obj = requests.cookies.create_cookie(domain=self.baseUrl.split('www')[1],name='datadome',value=cookie['cookie'])
                    self.session.cookies.set('datadome',cookie['cookie'])
                    continue

                except Exception as e:
                    print()
                    logger.error(SITE,self.taskID,'Failed to get challenge url. Sleeping...')
                    await asyncio.sleep(int(self.task["DELAY"]))
                    continue

            try:
                data = retrieveSizes.json()
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to get product data. Retrying...')
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                await asyncio.sleep(int(self.task["DELAY"]))
                continue
            
            if retrieveSizes.status_code == 200:
                if 'sold out' in retrieveSizes.text.lower():
                    logger.error(SITE,self.taskID,'Sold Out. Retrying...')
                    await asyncio.sleep(int(self.task["DELAY"]))
                    continue

                try:
                    htmlContent = data['content'].replace('\n','').replace("\\", "")
                except Exception as e:
                    log.info(e)
                    logger.error(SITE,self.taskID,'Failed to get product data. Retrying...')
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    await asyncio.sleep(int(self.task["DELAY"]))
                    continue
                
                try:
                    soup = BeautifulSoup(htmlContent,"html.parser")
                    eu_sizes = soup.find_all('section',{'class':'fl-accordion-tab--content'})[0].find_all('button')
                except:
                    logger.error(SITE,self.taskID,'Sizes Not Found')
                    await asyncio.sleep(int(self.task["DELAY"]))
                    continue

                

                allSizes = []
                sizes = []

                for s in eu_sizes:
                    try:
                        if 'not-available' in s['class']:
                            pass
                        else:
                            size = s.find('span').text
                            sizeSku = s['data-product-size-select-item']
                            allSizes.append('{}:{}'.format(size,sizeSku))
                            sizes.append(size)
                    except:
                        pass

                self.tabgroup = self.baseSku + allSizes[0].split(':')[1]


                if len(sizes) == 0:
                    logger.error(SITE,self.taskID,'Sizes Not Found')
                    await asyncio.sleep(int(self.task["DELAY"]))
                    self.collect()

                    
                if self.task["SIZE"].lower() != "random":
                    if self.task["SIZE"] not in sizes:
                        logger.error(SITE,self.taskID,'Size Not Found')
                        await asyncio.sleep(int(self.task["DELAY"]))
                        self.collect()
                    else:
                        for size in allSizes:
                            if size.split(':')[0] == self.task["SIZE"]:
                                self.size = size.split(':')[0]
                                self.sizeSku = size.split(":")[1]
                                logger.warning(SITE,self.taskID,f'Found Size => {self.size}')

                
                elif self.task["SIZE"].lower() == "random":
                    selected = random.choice(allSizes)
                    self.size = selected.split(":")[0]
                    self.sizeSku = selected.split(":")[1]
                    logger.warning(SITE,self.taskID,f'Found Size => {self.size}')

                self.addToCart()

            else:
                logger.error(SITE,self.taskID,'Failed to get product data. Retrying...')
                await asyncio.sleep(int(self.task["DELAY"]))
                continue


async def main():
    task_list = []
    for i in range(5):
        new_task = asyncio.create_task( Footlocker({"PRODUCT":"289138912"}, 'Task 000' + str(i), i).tasks() )
        task_list.append(new_task)

    print(task_list)
    await asyncio.gather(*task_list)



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
