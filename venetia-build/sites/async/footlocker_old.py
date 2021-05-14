import requests,json,re,time,random,aiohttp,asyncio,httpx,os,csv,sys
from bs4 import BeautifulSoup
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

        if self.countryCode == 'fr':
            self.baseUrl = 'https://www.footlocker.fr'
            self.baseUrl2 = 'https://www.footlocker.de/INTERSHOP/web/FLE/Footlocker-Footlocker_FR-Site/en_GB/-/EUR/'
        elif self.countryCode == 'de':
            self.baseUrl = 'https://www.footlocker.de'
            self.baseUrl2 = 'https://www.footlocker.de/INTERSHOP/web/FLE/Footlocker-Footlocker_DE-Site/de_DE/-/EUR/'
        elif self.countryCode == 'nl':
            self.baseUrl = 'https://www.footlocker.nl'
            self.baseUrl2 = 'https://www.footlocker.de/INTERSHOP/web/FLE/Footlocker-Footlocker_NL-Site/en_GB/-/EUR/'
        elif self.countryCode == 'gb':
            self.baseUrl = 'https://www.footlocker.co.uk'
            self.baseUrl2 = 'https://www.footlocker.co.uk/INTERSHOP/web/FLE/Footlocker-Footlocker_GB-Site/en_GB/-/GBP/'
        elif self.countryCode == 'au':
            self.baseUrl = 'https://www.footlocker.com.au'
            self.baseUrl2 = 'https://www.footlocker.com.au/INTERSHOP/web/FLE/Footlocker-Footlocker_AU-Site/en_GB/-/AUD/'
        elif self.countryCode == 'sg':
            self.baseUrl = 'https://www.footlocker.co.uk'
            self.baseUrl2 = 'https://www.footlocker.sg/INTERSHOP/web/FLE/FootlockerAsiaPacific-Footlocker_SG-Site/en_GB/-/SGD/'
        elif self.countryCode == 'my':
            self.baseUrl = 'https://www.footlocker.my'
            self.baseUrl2 = 'https://www.footlocker.my/INTERSHOP/web/FLE/FootlockerAsiaPacific-Footlocker_MY-Site/en_GB/-/MYR/'
        elif self.countryCode == 'hk':
            self.baseUrl = 'https://www.footlocker.hk'
            self.baseUrl2 = 'https://www.footlocker.hk/INTERSHOP/web/FLE/FootlockerAsiaPacific-Footlocker_HK-Site/en_GB/-/HKD/'
        else:
            await logger.error(SITE,self.taskID,'Region Not Supported')
            await asyncio.sleep(10)
            sys.exit()
            
        self.proxies = await loadProxy(self.task['PROXIES'],self.taskID,SITE)
        async with httpx.AsyncClient(proxies=self.proxies,timeout=None) as self.session:
            await self.retrieveSizes()
            await self.addToCart()
            await self.checkoutDispatch()
            await self.submitShipping()
            await self.submitPayment()

    async def rotateProxy(self):
        self.proxies = await loadProxy(self.task['PROXIES'],self.taskID,SITE)
        async with httpx.AsyncClient(proxies=self.proxies,timeout=None, cookies=self.session.cookies.jar) as self.session:
            return

    async def retrieveSizes(self):
        while True:
            await logger.prepare(SITE,self.taskID,'Getting product data...')
            
            self.relayCat = 'Relay42_Category'  #soup.find('input',{'value':'Product Pages'})['name']
            self.productImage = f'https://images.footlocker.com/is/image/FLEU/{self.baseSku}_01?wid=763&hei=538&fmt=png-alpha'
            # self.session.get(self.baseUrl)
            try:
                retrieveSizes = await self.session.get(f'{self.baseUrl2}ViewProduct-ProductVariationSelect?BaseSKU={self.baseSku}&InventoryServerity=ProductDetail',headers={
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
                await logger.error(SITE,self.taskID,'Error: {}'.format(e))
                await self.rotateProxy()
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

            if retrieveSizes.status_code == 503:
                await logger.info(SITE,self.taskID,'Queue...')
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

            elif retrieveSizes.status_code == 404:
                await logger.error(SITE,self.taskid,'Sold Out. Retrying...')
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

            elif retrieveSizes.status_code == 403:
                if 'nginx' in retrieveSizes.text:
                    await logger.error(SITE,self.taskID,'Blocked. Rotating Proxy')
                    await asyncio.sleep(int(self.task["DELAY"]))
                    await self.rotateProxy()
                    continue
                else:
                    await logger.error(SITE,self.taskID,'Blocked by DataDome (Solving Challenge...)')
                    try:
                        
                        challengeUrl = retrieveSizes.json()['url']
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

            
            if retrieveSizes.status_code == 200:
                self.start = time.time()
                try:
                    data = retrieveSizes.json()
                except Exception as e:
                    log.info(e)
                    await logger.error(SITE,self.taskID,'Failed to get product data. Retrying...')
                    await self.rotateProxy()
                    await asyncio.sleep(int(self.task["DELAY"]))
                    continue
            
                if 'sold out' in retrieveSizes.text.lower():
                    await logger.error(SITE,self.taskID,'Sold Out. Retrying...')
                    await asyncio.sleep(int(self.task["DELAY"]))
                    continue

                try:
                    htmlContent = data['content'].replace('\n','').replace("\\", "")
                except Exception as e:
                    log.info(e)
                    await logger.error(SITE,self.taskID,'Failed to get product data. Retrying...')
                    await self.rotateProxy()
                    await asyncio.sleep(int(self.task["DELAY"]))
                    continue
                
                try:
                    soup = BeautifulSoup(htmlContent,"html.parser")
                    eu_sizes = soup.find_all('section',{'class':'fl-accordion-tab--content'})[0].find_all('button')
                except:
                    await logger.error(SITE,self.taskID,'Sizes Not Found')
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

                # self.addToCart()
                return

            else:
                await logger.error(SITE,self.taskID,'Failed to get product data. Retrying...')
                await asyncio.sleep(int(self.task["DELAY"]))
                continue
    

    async def addToCart(self):
        while True:
            await logger.prepare(SITE,self.taskID,'Carting product...')
            params = {
                'Ajax': True,
                self.relayCat: 'Category Pages',
                f'acctab-tabgroup-{self.tabgroup}': None,
                f'Quantity_{self.sizeSku}': 1,
                'SKU': self.sizeSku
            }

            try:
                atcResponse = await self.session.post(f'{self.baseUrl}/en/addtocart',params=params,headers={
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
                try:
                    self.syncToken = atcResponse.text.split('ViewCart-Checkout?SynchronizerToken=')[1].split('\\"')[0]
                    self.productPrice = atcResponse.text.split('price:\\"')[1].split('\\"')[0]
                except Exception:
                    await logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
                    await asyncio.sleep(int(self.task["DELAY"]))
                    continue

                await updateConsoleTitle(True,False,SITE)
                await logger.warning(SITE,self.taskID,'Successfully carted product')
                # self.checkoutDispatch()
                return

            else:
                await logger.error(SITE,self.taskID,f'Failed to cart [{str(atcResponse.status_code)}]. Retrying...')
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

    async def checkoutDispatch(self):
        while True:
            await logger.prepare(SITE,self.taskID,'Getting checkout data...')

            try:
                checkoutOverviewPage = self.session.get(f'{self.baseUrl}/en/checkout-overview?SynchronizerToken=' + self.syncToken,headers={
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "accept-language": "en-US,en;q=0.9",
                    "sec-ch-ua": "\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-fetch-dest": "document",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "same-origin",
                    "sec-fetch-user": "?1",
                    "upgrade-insecure-requests": "1",
                    "user-agent":self.userAgent
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                await logger.error(SITE,self.taskID,'Error: {}'.format(e))
                await self.rotateProxy()
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

            if checkoutOverviewPage.status_code == 503:
                await logger.info(SITE,self.taskID,'Queue...')
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

            elif checkoutOverviewPage.status_code == 403:
                if 'nginx' in checkoutOverviewPage.text:
                    await logger.error(SITE,self.taskID,'Blocked. Rotating Proxy')
                    await asyncio.sleep(int(self.task["DELAY"]))
                    await self.rotateProxy()
                    continue
                else:
                    await logger.error(SITE,self.taskID,'Blocked by DataDome (Solving Challenge...)')
                    try:
                        
                        challengeUrl = checkoutOverviewPage.json()['url']
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

            elif checkoutOverviewPage.status_code == 200 or checkoutOverviewPage.status_code == 302:
                self.referer = checkoutOverviewPage.url
                try:

                    soup = BeautifulSoup(checkoutOverviewPage.text, "html.parser")
                    self.PaymentServiceSelection = soup.find('input',{'name':'PaymentServiceSelection'})['value']
                    self.shipMethodUUID = soup.find('input',{'name':'ShippingMethodUUID'})['value']
                    self.shippingAddressId = soup.find('input',{'name':'shipping_AddressID'})['value']
                    # billingAddressId = soup.find('input',{'name':'billing_AddressID'})['value']
                except Exception as e:
                    await log.info(e)
                    await logger.error(SITE,self.taskID,'Failed to get checkout data. Retrying...')
                    await asyncio.sleep(int(self.task["DELAY"]))
                    continue

                await logger.warning(SITE,self.taskID,'Got checkout data')
                return

            else:
                await logger.error(SITE,self.taskID,f'Failed to get checkout data [{str(checkoutOverviewPage.status_code)}]. Retrying...')
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

    async def submitShipping(self):
        while True:
            profile = loadProfile(self.task["PROFILE"])
            if profile == None:
                await logger.error(SITE,self.taskID,'Profile Not Found.')
                time.sleep(10)
                sys.exit()

            await logger.prepare(SITE,self.taskID,'Submitting Shipping...')
            form = "SynchronizerToken={}&isshippingaddress=&billing_Title=common.account.salutation.mr.text&billing_FirstName={}&billing_LastName={}&billing_CountryCode={}&billing_Address1={}&billing_Address2={}&billing_Address3={}&billing_City={}&billing_PostalCode={}&billing_PhoneHome={}&billing_BirthdayRequired=true&billing_Birthday_Day={}&billing_Birthday_Month={}&billing_Birthday_Year={}&email_Email={}&billing_ShippingAddressSameAsBilling=true&isshippingaddress=&shipping_Title=common.account.salutation.mr.text&shipping_FirstName=&shipping_LastName=&SearchTerm=&shipping_CountryCode={}&shipping_Address1=&shipping_Address2=&shipping_Address3=&shipping_City=&shipping_PostalCode=&shipping_PhoneHome=&shipping_AddressID={}&CheckoutRegisterForm_Password=&promotionCode=&PaymentServiceSelection={}&UserDeviceTypeForPaymentRedirect=Desktop&UserDeviceFingerprintForPaymentRedirect={}&ShippingMethodUUID={}&termsAndConditions=on&GDPRDataComplianceRequired=true&sendOrder=".format(
                self.syncToken,
                profile['firstName'],
                profile['lastName'],
                profile['countryCode'],
                profile['addressOne'],
                profile['house'],
                profile['addressTwo'],
                profile['city'],
                profile['zip'],
                profile['phone'],
                random.randint(1,25),#day
                random.randint(1,12), #month
                random.randint(1970,2000), #year
                profile['email'],
                profile['countryCode'],
                self.shippingAddressId,
                self.PaymentServiceSelection,
                self.deviceId,
                self.shipMethodUUID
            )
            try:
                checkoutOverviewDispatch = self.session.post(f'{self.baseUrl2}ViewCheckoutOverview-Dispatch',data=form,headers={
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "accept-language": "en-US,en;q=0.9",
                    "accept-encoding": "gzip, deflate, br",
                    "cache-control": "max-age=0",
                    "content-type": "application/x-www-form-urlencoded",
                    "sec-ch-ua": "\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-fetch-dest": "document",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "same-origin",
                    "sec-fetch-user": "?1",
                    "upgrade-insecure-requests": "1",
                    "referer":self.referer,
                    "user-agent":self.userAgent
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                await logger.error(SITE,self.taskID,'Error: {}'.format(e))
                await self.rotateProxy()
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

            if checkoutOverviewDispatch.status_code == 503:
                await logger.info(SITE,self.taskID,'Queue...')
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

            elif checkoutOverviewDispatch.status_code == 403:
                if 'nginx' in checkoutOverviewDispatch.text:
                    await logger.error(SITE,self.taskID,'Blocked. Rotating Proxy')
                    await asyncio.sleep(int(self.task["DELAY"]))
                    await self.rotateProxy()
                    continue
                else:
                    await logger.error(SITE,self.taskID,'Blocked by DataDome (Solving Challenge...)')
                    try:
                        
                        challengeUrl = checkoutOverviewDispatch.json()['url']
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

            elif checkoutOverviewDispatch.status_code == 200 and 'OrderID' in checkoutOverviewDispatch.url or checkoutOverviewDispatch.status_code == 302 and 'OrderID' in checkoutOverviewDispatch.url:                
                self.responseText = checkoutOverviewDispatch.text
                self.responseUrl = checkoutOverviewDispatch.url

                await logger.warning(SITE,self.taskID,'Submitted Shipping')
                return

            else:
                await logger.error(SITE,self.taskID,f'Failed to submit shipping [{str(checkoutOverviewDispatch.status_code)}]. Retrying...')
                await asyncio.sleep(int(self.task["DELAY"]))
                continue

    async def submitPayment(self):
        while True:

            profile = loadProfile(self.task["PROFILE"])
            if profile == None:
                await logger.error(SITE,self.taskID,'Profile Not Found.')
                time.sleep(10)
                sys.exit()

            await logger.prepare(SITE,self.taskID,'Submitting Payment...')
            
            payload = {}
            try:
                soup = BeautifulSoup(self.responseText,"html.parser")
                self.adyeninputs = soup.find_all("input")
                for item in self.adyeninputs:
                    payload.update({item["name"]:item["value"]})
                
            except:
                await self.error("Error loading payment form")
                await asyncio.sleep(self.delay)
                continue



            try:
                payment = self.session.post('https://live.adyen.com/hpp/pay.shtml',data=payload,headers={
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "accept-language": "en-US,en;q=0.9",
                    "cache-control": "max-age=0",
                    "content-type": "application/x-www-form-urlencoded",
                    "sec-ch-ua": "\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-fetch-dest": "document",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "cross-site",
                    "upgrade-insecure-requests": "1",
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

                if self.task['PAYMENT'].lower().strip() == "paypal":
                    payload["displayGroup"] = "paypal"
                    payload["paypal.storeOcDetails"] = 'false'
                    try:
                        del payload["brandName"]
                    except:
                        pass

                    try:
                        del payload["back"]
                    except:
                        pass

                    payload["brandCode"] = 'paypal'
                    payload["shopperBehaviorLog"] = {"numberBind":"1","holderNameBind":"1","cvcBind":"1","deactivate":"1","activate":"1"}
                    payload["dfValue"] = 'ryEGX8eZpJ0030000000000000BTWDfYZVR30089146776cVB94iKzBGA0ghUVGkxk5S16Goh5Mk0045zgp4q8JSa00000qZkTE00000q6IQbnyNfpEC4FlSABmQ:40'
                
                    try:
                        pp_req = await self.session.post("https://live.adyen.com/hpp/redirectPayPal.shtml",data=payload,headers={
                            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                            "accept-language": "en-US,en;q=0.9",
                            "cache-control": "max-age=0",
                            "content-type": "application/x-www-form-urlencoded",
                            "sec-ch-ua": "\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"",
                            "sec-ch-ua-mobile": "?0",
                            "sec-fetch-dest": "document",
                            "sec-fetch-mode": "navigate",
                            "sec-fetch-site": "cross-site",
                            "upgrade-insecure-requests": "1",
                            "user-agent":self.userAgent
                        })
                    except Exception as e:
                        await self.error(f"Error getting PayPal Url - {e}")
                        await asyncio.sleep(self.delay)
                        continue

                    if "paypal" in str(self.ppreq.url):
                        self.end = time.time() - self.start
                        await logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')
                        await updateConsoleTitle(False,True,SITE)

                        url = await storeCookies(pp_req.url,self.session, self.productTitle, self.productImage, self.productPrice)

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
                        await self.error("Error getting PayPal Url")
                        await asyncio.sleep(self.delay)
                        continue

                else:
                    try:
                        payload["brandName"]
                    except:
                        pass

                    try:
                        payload["pay"]
                        payload["back"]
                    except:
                        pass

                    payload["brandCode"] = 'brandCodeUndef'
                    payload["displayGroup"] = "card"
                    payload["card.cardNumber"] = profile['card']['cardNumber']
                    payload["card.cardHolderName"] = "{} {}".format(profile['firstName'], profile['lastName'])
                    payload["card.cvcCode"] = profile['card']['cardCVV']
                    payload["card.expiryMonth"] = profile['card']['cardMonth']
                    payload["card.expiryYear"] = profile['card']['cardYear']
                    payload["shopperBehaviorLog"] = {"numberBind":"1","holderNameBind":"1","cvcBind":"1","deactivate":"3","activate":"2","numberFieldFocusCount":"2","numberFieldLog":"fo@42,cl@42,cl@261,bl@347,fo@494,Cd@498,KL@499,Cu@500,ch@512,bl@512","numberFieldClickCount":"2","numberFieldBlurCount":"2","numberFieldKeyCount":"2","numberFieldChangeCount":"1","numberFieldEvHa":"total=0","holderNameFieldFocusCount":"1","holderNameFieldLog":"fo@512,cl@512,Sd@522,KL@525,KL@526,Su@526,KL@527,KL@528,Ks@530,Sd@531,Su@534,Kb@535,Kb@536,Kb@538,Kb@539,KL@543,KL@544,KL@545,Ks@548,Sd@549,KL@550,Su@551,KL@551,KL@553,KL@555,KL@556,KL@557,KL@558,KL@559,KU@560,ch@560,bl@560","holderNameFieldClickCount":"1","holderNameFieldKeyCount":"25","holderNameUnkKeysFieldLog":"9@560","holderNameFieldChangeCount":"1","holderNameFieldEvHa":"total=0","holderNameFieldBlurCount":"1","cvcFieldFocusCount":"1","cvcFieldLog":"fo@624,cl@625,KN@653,KN@656,KN@657,ch@672,bl@672","cvcFieldClickCount":"1","cvcFieldKeyCount":"3","cvcFieldChangeCount":"1","cvcFieldEvHa":"total=0","cvcFieldBlurCount":"1"}

                return

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
