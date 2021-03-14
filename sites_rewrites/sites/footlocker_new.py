import requests,json,re,time,random,aiohttp,asyncio,httpx,os,csv,sys,uuid
from bs4 import BeautifulSoup
from datetime import timezone, datetime
import urllib3
from urllib3.exceptions import InsecureRequestWarning 
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from utils.logger import logger
from utils.webhook import Webhook
from utils.log import log
from utils.datadome import datadome
from utils.functions import (
    loadSettings,
    loadProxy,
    loadProfile,
    createId,
    loadCookie,
    loadToken,
    sendNotification,
    injection,
    storeCookies,
    updateConsoleTitle,
    scraper,
    footlocker_snare
)

SITE = 'Footlocker'
class FOOTLOCKER_OLD():

    def __init__(self, task, taskName, rowNumber):
        self.task = task
        self.session = requests.session()
        self.taskID = taskName
        self.rowNumber = rowNumber
        self.blocked = False

        self.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'

    # async def loadProxy(self):
    #     self.proxy = None
    #     if self.proxies == [] or not self.proxies:
    #         return None
    #     self.px = random.choice(self.proxies)
    #     self.splitted = self.px.split(':')
    #     print(self.px)
    #     if len(self.splitted) == 2:
    #         self.proxy = 'http://{}'.format(self.px)
    #         return
        
    #     elif len(self.splitted) == 4:
    #         self.proxy = 'http://{}:{}@{}:{}'.format(self.splitted[2], self.splitted[3], self.splitted[0], self.splitted[1])
    #         return
    #     else:
    #         await self.error('Invalid proxy: "{}", rotating'.format(self.px))
    #         return

    async def tasks(self):
        profile = await loadProfile(self.task["PROFILE"])
        if profile == None:
            await logger.error(SITE,self.taskID,'Profile Not Found.')
            await asyncio.sleep(10)
            sys.exit()

        self.countryCode = profile['countryCode'].lower()

        self.proxies = None
        self.baseSku = self.task['PRODUCT']

        if self.countryCode == 'it':
            self.baseUrl = 'https://www.footlocker.it'
        elif self.countryCode == 'be':
            self.baseUrl = 'https://www.footlocker.be'
        elif self.countryCode == 'at':
            self.baseUrl = 'https://www.footlocker.at'
        elif self.countryCode == 'lu':
            self.baseUrl = 'https://www.footlocker.lu'
        elif self.countryCode == 'cz':
            self.baseUrl = 'https://www.footlocker.cz'
        elif self.countryCode == 'dk':
            self.baseUrl = 'https://www.footlocker.dk'
        elif self.countryCode == 'pl':
            self.baseUrl = 'https://www.footlocker.pl'
        elif self.countryCode == 'gr':
            self.baseUrl = 'https://www.footlocker.gr'
        elif self.countryCode == 'pt':
            self.baseUrl = 'https://www.footlocker.pt'
        elif self.countryCode == 'hu':
            self.baseUrl = 'https://www.footlocker.hu'
        elif self.countryCode == 'es':
            self.baseUrl = 'https://www.footlocker.es'
        elif self.countryCode == 'ie':
            self.baseUrl = 'https://www.footlocker.ie'
        elif self.countryCode == 'no':
            self.baseUrl = 'https://www.footlocker.no'
        elif self.countryCode == 'se':
            self.baseUrl = 'https://www.footlocker.se'
        elif self.countryCode == 'de':
            self.baseUrl = 'https://www.footlocker.de'
        else:
            await logger.error(SITE,self.taskID,'Region Not Supported')
            await asyncio.sleep(10)
            sys.exit()
            
        self.proxies = await loadProxy(self.task['PROXIES'],self.taskID,SITE)
        async with httpx.AsyncClient(proxies=self.proxies,timeout=None) as self.session:
            await self.collect()
            await self.footlockerSession()
            await self.addToCart()
            await self.setEmail()
            await self.submitShipping()
            await self.paypal()

    async def rotateProxy(self):
        self.proxies = await loadProxy(self.task['PROXIES'],self.taskID,SITE)
        async with httpx.AsyncClient(proxies=self.proxies,timeout=None, cookies=self.session.cookies.jar) as self.session:
            return

    async def collect(self):
        while True:
            await logger.prepare(SITE,self.taskID,'Getting product data...')
            self.start = time.time()
            self.relayCat = 'Relay42_Category'  #soup.find('input',{'value':'Product Pages'})['name']
            self.productImage = f'https://images.footlocker.com/is/image/FLEU/{self.baseSku}_01?wid=763&hei=538&fmt=png-alpha'
            # self.session.get(self.baseUrl)
            url = '{}/en/product/{}/{}.html'.format(self.baseUrl, self.task['PRODUCT'], self.task['PRODUCT'])
            try:
                retrieve = await self.session.get(url,headers={
                    "user-agent":self.userAgent
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                await logger.error(SITE,self.taskID,'Error: {}'.format(e))
                await self.rotateProxy()
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

            if retrieve.status_code == 503:
                await logger.info(SITE,self.taskID,'Queue...')
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

            elif retrieve.status_code == 404:
                await logger.error(SITE,self.taskid,'Sold Out. Retrying...')
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

            elif retrieve.status_code == 403:
                if 'nginx' in retrieve.text:
                    await logger.error(SITE,self.taskID,'Blocked. Rotating Proxy')
                    await asyncio.sleep(int(self.task["DELAY"]))
                    await self.rotateProxy()
                    continue
                else:
                    await logger.error(SITE,self.taskID,'Blocked by DataDome (Solving Challenge...)')
                    try:
                        
                        challengeUrl = retrieve.json()['url']
                        cookie = await datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        while cookie['cookie'] == None:
                            await self.rotateProxy()
                            cookie = await datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        
                        del self.session.cookies['datadome']
                        self.session.cookies.set('datadome',cookie['cookie'], domain=self.baseUrl.split('https://www')[1])
                        continue

                    except Exception as e:
                        await logger.error(SITE,self.taskID,'Failed to solve challenge. Sleeping...')
                        await asyncio.sleep(int(self.task["DELAY"]))
                        continue

            
            if retrieve.status_code == 200:
                self.start = time.time()
                logger.warning(SITE,self.taskID,'Got product page')
                try:
                    logger.prepare(SITE,self.taskID,'Getting product data...')
                    url = retrieve.text.split('"@id":"')[1].split('"')[0]
                    regex = r"window.footlocker.STATE_FROM_SERVER = {(.+)}"
                    matches = re.search(regex, retrieve.text, re.MULTILINE)
                    productData = json.loads(matches.group().split('window.footlocker.STATE_FROM_SERVER = ')[1])
                    eu_sizes = productData['details']['sizes'][url.split(self.baseUrl)[1]]

                    self.productPrice = productData['details']['data'][url.split(self.baseUrl)[1]][0]['price']['formattedValue']
                    self.productTitle = productData['details']['product'][url.split(self.baseUrl)[1]]['name']
                    self.productImage = f'https://images.footlocker.com/is/image/FLEU/{self.baseSku}_01?wid=763&hei=538&fmt=png-alpha'
                except Exception as e:
                    await log.info(e)
                    await logger.error(SITE,self.taskID,'Failed to scrape page (Most likely out of stock). Retrying...')
                    await asyncio.sleep(int(self.task["DELAY"]))
                    continue

                allSizes = []
                sizes = []

            
                for s in eu_sizes:
                    try:
                        sizes.append(s['name'])
                        allSizes.append('{}:{}'.format(s['name'], s['code']))
                    except:
                        pass


                if len(sizes) == 0:
                    await logger.error(SITE,self.taskID,'Sizes Not Found')
                    await asyncio.sleep(int(self.task["DELAY"]))
                    continue

                    
                if self.task["SIZE"].lower() != "random":
                    if self.task["SIZE"] not in sizes:
                        await logger.error(SITE,self.taskID,'Size Not Found')
                        await asyncio.sleep(int(self.task["DELAY"]))
                        continue
                    else:
                        for size in allSizes:
                            if size.split(':')[0] == self.task["SIZE"]:
                                self.size = size.split(':')[0]
                                self.sizeSku = size.split(":")[1]
                                await logger.warning(SITE,self.taskID,f'Found Size => {self.size}')

                
                elif self.task["SIZE"].lower() == "random":
                    selected = random.choice(allSizes)
                    self.size = selected.split(":")[0]
                    self.sizeSku = selected.split(":")[1]
                    await logger.warning(SITE,self.taskID,f'Found Size => {self.size}')


                return

            else:
                await logger.error(SITE,self.taskID,'Failed to get product data. Retrying...')
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

    async def footlockerSession(self):
        while True:
            await logger.prepare(SITE,self.taskID,'Getting session')
            params = {
                'Ajax': True,
                self.relayCat: 'Category Pages',
                f'acctab-tabgroup-{self.tabgroup}': None,
                f'Quantity_{self.sizeSku}': 1,
                'SKU': self.sizeSku
            }

            try:
                response = await self.session.get(f'{self.baseUrl}/api/session?timestamp={int(datetime.now(tz=timezone.utc).timestamp() * 1000)}',headers={
                    "accept": "application/json",
                    "accept-language": "en-GB,en;q=0.9",
                    "content-type": "application/json",
                    "sec-ch-ua": "\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "x-api-lang": "en-GB",
                    # "x-fl-request-id": "45a40be0-4f57-11eb-87a1-a1e3b40a67ba"
                    "user-agent":self.userAgent
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                await logger.error(SITE,self.taskID,'Error: {}'.format(e))
                await self.rotateProxy()
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

            if response.status_code == 503:
                await logger.info(SITE,self.taskID,'Queue...')
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

            elif response.status_code == 403:
                if 'nginx' in response.text:
                    await logger.error(SITE,self.taskID,'Blocked. Rotating Proxy')
                    await asyncio.sleep(int(self.task["DELAY"]))
                    await self.rotateProxy()
                    continue
                else:
                    await logger.error(SITE,self.taskID,'Blocked by DataDome (Solving Challenge...)')
                    try:
                        
                        challengeUrl = response.json()['url']
                        cookie = await datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        while cookie['cookie'] == None:
                            await self.rotateProxy()
                            cookie = await datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        
                        del self.session.cookies['datadome']
                        self.session.cookies.set('datadome',cookie['cookie'], domain=self.baseUrl.split('https://www')[1])
                        continue

                    except Exception as e:
                        await logger.error(SITE,self.taskID,'Failed to solve challenge. Sleeping...')
                        await asyncio.sleep(int(self.task["DELAY"]))
                        continue

            elif response.status_code == 200:
                try:
                    self.csrf = response.json()['data']['csrfToken']
                except:
                    await logger.error(SITE,self.taskID,'Failed to get session')
                    await asyncio.sleep(int(self.task["DELAY"]))
                    continue

                await logger.warning(SITE,self.taskID,'Got session')
                # self.addToCart()
                return

            else:
                await logger.error(SITE,self.taskID,f'Failed to get session [{str(response.status_code)}]. Retrying...')
                await asyncio.sleep(int(self.task["DELAY"]))
                continue
    

    async def addToCart(self):
        while True:
            await logger.prepare(SITE,self.taskID,'Carting product...')
            data = {"productQuantity":1,"productId":self.sizeSku}

            try:
                atcResponse = await self.session.post(f'{self.baseUrl}/api/users/carts/current/entries?timestamp={int(datetime.now(tz=timezone.utc).timestamp() * 1000)}',json=data,headers={
                    "accept": "application/json",
                    "accept-language": "en-GB,en;q=0.9",
                    "content-type": "application/json",
                    "sec-ch-ua": "\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "x-api-lang": "en-GB",
                    "x-csrf-token": self.csrf,
                    "x-fl-productid": self.sizeSku,
                    # "x-fl-request-id": "45a40be0-4f57-11eb-87a1-a1e3b40a67ba"
                    "user-agent":self.userAgent
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                await logger.error(SITE,self.taskID,'Error: {}'.format(e))
                await self.rotateProxy()
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

            if atcResponse.status_code == 503:
                await logger.info(SITE,self.taskID,'Queue...')
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

            elif atcResponse.status_code == 403:
                if 'nginx' in atcResponse.text:
                    await logger.error(SITE,self.taskID,'Blocked. Rotating Proxy')
                    await asyncio.sleep(int(self.task["DELAY"]))
                    await self.rotateProxy()
                    continue
                else:
                    await logger.error(SITE,self.taskID,'Blocked by DataDome (Solving Challenge...)')
                    try:
                        
                        challengeUrl = atcResponse.json()['url']
                        cookie = await datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        while cookie['cookie'] == None:
                            await self.rotateProxy()
                            cookie = await datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        
                        del self.session.cookies['datadome']
                        self.session.cookies.set('datadome',cookie['cookie'], domain=self.baseUrl.split('https://www')[1])
                        continue

                    except Exception as e:
                        await logger.error(SITE,self.taskID,'Failed to solve challenge. Sleeping...')
                        await asyncio.sleep(int(self.task["DELAY"]))
                        continue

            elif atcResponse.status_code == 200:
                await updateConsoleTitle(True,False,SITE)
                await logger.warning(SITE,self.taskID,'Successfully carted product')
                return

            else:
                await logger.error(SITE,self.taskID,f'Failed to cart [{str(atcResponse.status_code)}]. Retrying...')
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

    async def setEmail(self):
        while True:

            profile = loadProfile(self.task["PROFILE"])
            if profile == None:
                await logger.error(SITE,self.taskID,'Profile Not Found.')
                await asyncio.sleep(10)
                sys.exit()

            await logger.prepare(SITE,self.taskID,'Setting email...')

            try:
                emailPage = await self.session.put('{}/api/users/carts/current/email/{}?timestamp={}'.format(self.baseUrl, profile['email'], int(datetime.now(tz=timezone.utc).timestamp() * 1000)),headers={
                    "accept": "application/json",
                    "accept-language": "en-GB,en;q=0.9",
                    "content-type": "application/json",
                    "sec-ch-ua": "\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "x-api-lang": "en-GB",
                    "x-csrf-token": self.csrf,
                    # "x-fl-productid": self.sizeSku,
                    # "x-fl-request-id": "45a40be0-4f57-11eb-87a1-a1e3b40a67ba"
                    "user-agent":self.userAgent
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                await logger.error(SITE,self.taskID,'Error: {}'.format(e))
                await self.rotateProxy()
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

            if emailPage.status_code == 503:
                await logger.info(SITE,self.taskID,'Queue...')
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

            elif emailPage.status_code == 403:
                if 'nginx' in emailPage.text:
                    await logger.error(SITE,self.taskID,'Blocked. Rotating Proxy')
                    await asyncio.sleep(int(self.task["DELAY"]))
                    await self.rotateProxy()
                    continue
                else:
                    await logger.error(SITE,self.taskID,'Blocked by DataDome (Solving Challenge...)')
                    try:
                        
                        challengeUrl = emailPage.json()['url']
                        cookie = await datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        while cookie['cookie'] == None:
                            await self.rotateProxy()
                            cookie = await datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        
                        del self.session.cookies['datadome']
                        self.session.cookies.set('datadome',cookie['cookie'], domain=self.baseUrl.split('https://www')[1])
                        continue

                    except Exception as e:
                        await logger.error(SITE,self.taskID,'Failed to solve challenge. Sleeping...')
                        await asyncio.sleep(int(self.task["DELAY"]))
                        continue

            elif emailPage.status_code == 200 or emailPage.status_code == 302:
                await logger.warning(SITE,self.taskID,'Email set')
                return

            else:
                await logger.error(SITE,self.taskID,f'Failed to set email [{str(emailPage.status_code)}]. Retrying...')
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

    async def submitShipping(self):
        while True:

            profile = loadProfile(self.task["PROFILE"])
            if profile == None:
                await logger.error(SITE,self.taskID,'Profile Not Found.')
                await asyncio.sleep(10)
                sys.exit()

            await logger.prepare(SITE,self.taskID,'Submitting shipping...')

            data = {
                "shippingAddress":{
                    "setAsDefaultBilling":False,
                    "setAsDefaultShipping":False,
                    "firstName":profile['firstName'],
                    "lastName":profile['lastName'],
                    "email":profile['email'],
                    "phone":profile['phone'],
                    "country":{
                        "isocode":profile['countryCode'].upper(),
                        "name":profile['country'].title()
                    },
                    "id":None,
                    "setAsBilling":True,
                    "type":"default",
                    "line1":profile['addressOne'] + ' ' + profile['addressTwo'],
                    "line2":profile['house'],
                    "companyName":"",
                    "postalCode":profile['zip'],
                    "town":profile['city'],
                    "shippingAddress":True
                }
            }

            try:
                shippingAddress = self.session.post('{}/api/users/carts/current/addresses/shipping?timestamp={}'.format(self.baseUrl, int(datetime.now(tz=timezone.utc).timestamp() * 1000)),json=data,headers={
                    "accept": "application/json",
                    "accept-language": "en-GB,en;q=0.9",
                    "content-type": "application/json",
                    "sec-ch-ua": "\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "x-api-lang": "en-GB",
                    "x-csrf-token": self.csrf,
                    # "x-fl-productid": self.sizeSku,
                    # "x-fl-request-id": "45a40be0-4f57-11eb-87a1-a1e3b40a67ba"
                    "user-agent":self.userAgent
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                await logger.error(SITE,self.taskID,'Error: {}'.format(e))
                await self.rotateProxy()
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

            if shippingAddress.status_code == 503:
                await logger.info(SITE,self.taskID,'Queue...')
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

            elif shippingAddress.status_code == 403:
                if 'nginx' in shippingAddress.text:
                    await logger.error(SITE,self.taskID,'Blocked. Rotating Proxy')
                    await asyncio.sleep(int(self.task["DELAY"]))
                    await self.rotateProxy()
                    continue
                else:
                    await logger.error(SITE,self.taskID,'Blocked by DataDome (Solving Challenge...)')
                    try:
                        
                        challengeUrl = shippingAddress.json()['url']
                        cookie = await datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        while cookie['cookie'] == None:
                            await self.rotateProxy()
                            cookie = await datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        
                        del self.session.cookies['datadome']
                        self.session.cookies.set('datadome',cookie['cookie'], domain=self.baseUrl.split('https://www')[1])
                        continue

                    except Exception as e:
                        await logger.error(SITE,self.taskID,'Failed to solve challenge. Sleeping...')
                        await asyncio.sleep(int(self.task["DELAY"]))
                        continue

            elif shippingAddress.status_code == 200 or shippingAddress.status_code == 201:
                await logger.warning(SITE,self.taskID,'Shipping submitted')
                return

            else:
                await logger.error(SITE,self.taskID,f'Failed to submit shipping [{str(shippingAddress.status_code)}]. Retrying...')
                await asyncio.sleep(int(self.task["DELAY"]))
                continue


    async def paypal(self):
        while True:

            profile = loadProfile(self.task["PROFILE"])
            if profile == None:
                await logger.error(SITE,self.taskID,'Profile Not Found.')
                time.sleep(10)
                sys.exit()

            await logger.prepare(SITE,self.taskID,'Submitting payment...')




            try:
                payment = self.session.get('{}/apigate/payment/methods?channel=WEB&timestamp={}'.format(self.baseUrl, int(datetime.now(tz=timezone.utc).timestamp() * 1000)),headers={
                    "accept": "application/json",
                    "accept-language": "en-GB,en;q=0.9",
                    "content-type": "application/json",
                    "sec-ch-ua": "\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "x-api-lang": "en-GB",
                    "x-csrf-token": self.csrf,
                    # "x-fl-productid": self.sizeSku,
                    # "x-fl-request-id": "45a40be0-4f57-11eb-87a1-a1e3b40a67ba"
                    "user-agent":self.userAgent
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                await logger.error(SITE,self.taskID,'Error: {}'.format(e))
                await self.rotateProxy()
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

            if payment.status_code == 503:
                await logger.info(SITE,self.taskID,'Queue...')
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

            elif payment.status_code == 403:
                if 'nginx' in payment.text:
                    await logger.error(SITE,self.taskID,'Blocked. Rotating Proxy')
                    await asyncio.sleep(int(self.task["DELAY"]))
                    await self.rotateProxy()
                    continue
                else:
                    await logger.error(SITE,self.taskID,'Blocked by DataDome (Solving Challenge...)')
                    try:
                        
                        challengeUrl = payment.json()['url']
                        cookie = await datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        while cookie['cookie'] == None:
                            await self.rotateProxy()
                            cookie = await datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        
                        del self.session.cookies['datadome']
                        self.session.cookies.set('datadome',cookie['cookie'], domain=self.baseUrl.split('https://www')[1])
                        continue

                    except Exception as e:
                        await logger.error(SITE,self.taskID,'Failed to solve challenge. Sleeping...')
                        await asyncio.sleep(int(self.task["DELAY"]))
                        continue

            elif payment.status_code == 200 :                
                await logger.warning(SITE,self.taskID,'Payment Submitted')

                try:
                    self.tokenizationKey = payment.json()[1]['key']
                    self.gatewayMerchantId = payment.json()[1]['gatewayMerchantId']
                    self.currency = payment.json()[1]['currency']

                    braintreeData = {
                        "returnUrl": "x",
                        "cancelUrl": "x",
                        "offerPaypalCredit": False,
                        "experienceProfile": {
                            "brandName": "FootLocker",
                            "noShipping": "false",
                            "addressOverride": False
                        },
                        "amount": 81.96,
                        "currencyIsoCode": self.currency,
                        "intent": "authorize",
                        "line1": profile['addressOne'],
                        "line2": profile['house'],
                        "city": profile['city'],
                        "postalCode": profile['zip'],
                        "countryCode": profile['countryCode'].upper(),
                        "phone": profile['phone'],
                        "recipientName": profile['firstName'] + ' ' + profile['lastName'],
                        "braintreeLibraryVersion": "braintree/web/3.29.0",
                        "_meta": {
                            "merchantAppId": self.baseUrl.split('https://')[1],
                            "platform": "web",
                            "sdkVersion": "3.29.0",
                            "source": "client",
                            "integration": "custom",
                            "integrationType": "custom",
                            "sessionId": str(uuid.uuid4())
                        },
                        "tokenizationKey": self.tokenizationKey   
                    }
                except Exception as e:
                    await log.info(e)
                    await logger.error(SITE,self.taskID,'Failed to submit payment. Retrying...')
                    await asyncio.sleep(int(self.task['DELAY']))

                try:
                    paymentResource = await self.session.post('https://api.braintreegateway.com/merchants/rfbkw27jcwmw2xgp/client_api/v1/paypal_hermes/create_payment_resource',json=braintreeData,headers={
                        "Accept": "*/*",
                        "accept-language": "en-GB,en;q=0.9",
                        "content-type": "application/json",
                        "sec-ch-ua": "\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"",
                        'Referer':self.baseUrl,
                        "User-Agent":self.userAgent
                    })
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    await log.info(e)
                    await logger.error(SITE,self.taskID,'Error: {}'.format(e))
                    await self.rotateProxy()
                    await asyncio.sleep(int(self.task["DELAY"]))
                    continue

                try:
                    paypalRedirect = paymentResource.json()['paymentResource']['redirectUrl']
                except:
                    await logger.error(SITE,self.taskID,'Failed to submit payment. Retrying...')
                    await asyncio.sleep(int(self.task["DELAY"]))
                    continue

                await logger.warning(SITE,self.taskID,'Payment submitted')
                self.end = time.time() - self.start
        
                await updateConsoleTitle(False,True,SITE)
                await logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')
                url = await storeCookies(paypalRedirect,self.session, self.productTitle, self.productImage, self.productPrice)

                try:
                    Webhook.success(
                        webhook=loadSettings()["webhook"],
                        site=SITE,
                        url=url,
                        image=self.productImage,
                        title=self.productTitle,
                        size=self.size,
                        price=self.productPrice,
                        paymentMethod='PayPal',
                        profile=self.task["PROFILE"],
                        product=self.task["PRODUCT"],
                        proxy=self.session.proxies,
                        speed=self.end,
                        region=self.countryCode
                    )
                    await sendNotification(SITE,self.productTitle)
                    while True:
                        pass
                except Exception as e:
                    await log.info(e)
                    await logger.alert(SITE,self.taskID,'Failed to send webhook. Checkout here ==> {}'.format(url))



            else:
                await logger.error(SITE,self.taskID,f'Failed to submit payment [{str(payment.status_code)}]. Retrying...')
                await asyncio.sleep(int(self.task["DELAY"]))
                continue



# async def main():
#     task_list = []
#     for i in range(5):
#         new_task = asyncio.create_task( Footlocker({"PRODUCT":"289138912"}, 'Task 000' + str(i), i).tasks() )
#         task_list.append(new_task)

#     await asyncio.gather(*task_list)



# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
