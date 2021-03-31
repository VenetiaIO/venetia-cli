import requests
from bs4 import BeautifulSoup
import datetime
import threading
import random
import sys
import time
import re
import json
import os
import base64
import cloudscraper
import string
from urllib3.exceptions import HTTPError
import csv
import tls as client
from requests_toolbelt import MultipartEncoder

from utils.captcha import captcha
from utils.logger import logger
from utils.webhook import Webhook
from utils.log import log
from utils.datadome import datadome
from utils.threeDS import threeDSecure
from utils.functions import (
    loadSettings,
    loadProfile,
    loadProxy,
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
import utils.config as config


SITE = 'FOOTLOCKER'
class FOOTLOCKER_OLD:
    def success(self,message):
        logger.success(SITE,self.taskID,message)
    def error(self,message):
        logger.error(SITE,self.taskID,message)
    def prepare(self,message):
        logger.prepare(SITE,self.taskID,message)
    def warning(self,message):
        logger.warning(SITE,self.taskID,message)
    def info(self,message):
        logger.info(SITE,self.taskID,message)
    def secondary(self,message):
        logger.secondary(SITE,self.taskID,message)
    def alert(self,message):
        logger.alert(SITE,self.taskID,message)


    def task_checker(self):
        originalTask = self.task
        while True:
            with open('./{}/tasks.csv'.format(SITE.lower()),'r') as csvFile:
                csv_reader = csv.DictReader(csvFile)
                row = [row for idx, row in enumerate(csv_reader) if idx in (self.rowNumber,self.rowNumber)]
                self.task = row[0]
                try:
                    self.task['ACCOUNT EMAIL'] = originalTask['ACCOUNT EMAIL']
                    self.task['ACCOUNT PASSWORD'] = originalTask['ACCOUNT PASSWORD']
                except:
                    pass
                csvFile.close()

            time.sleep(2)


    def __init__(self, task, taskName, rowNumber):
        self.task = task
        self.session = requests.session()
        self.taskID = taskName
        self.rowNumber = rowNumber
        self.blocked = False

        if self.rowNumber != 'qt': 
            threading.Thread(target=self.task_checker,daemon=True).start()

        self.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'

        try:
            # self.session = client.Session(browser=client.Fingerprint.CHROME_83)
            # self.session = scraper()
            self.session = requests.session()
        except Exception as e:
            self.error(f'error => {e}')
            self.__init__(task,taskName,rowNumber)


        self.webhookData = {
            "site":SITE,
            "product":"n/a",
            "size":"n/a",
            "image":"https://i.imgur.com/VqWvzDN.png",
            "price":"0",
            "profile":self.task['PROFILE'],
            "speed":0,
            "url":"https://venetiacli.io",
            "paymentMethod":"n/a",
            "proxy":"n/a",
            "product_url":self.task['PRODUCT']
        }

        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)

        self.profile = loadProfile(self.task["PROFILE"])
        if self.profile == None:
            self.error("Profile Not found. Exiting...")
            time.sleep(10)
            sys.exit()

        self.countryCode = self.profile['countryCode'].lower()
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
            self.error('Region Not Supported')
            time.sleep(10)
            sys.exit()

        self.tasks()

    def tasks(self):
            
        self.retrieveSizes()
        self.addToCart()
        self.checkoutDispatch()
        self.submitShipping()
        self.submitPayment()

        if self.task['PAYMENT'].lower().strip() == "card":
            self.card()

        self.sendToDiscord()

    def solveDD(self, response):
        try:
            challengeUrl = response.json()['url']

            challenge = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'])
            while challenge['cookie'] == None:
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                challenge = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'])
            
            del self.session.cookies['datadome']
            # self.session.cookies.set('datadome',challenge['cookie'], domain=self.baseUrl.split('https://www')[1])
            print('datadome',challenge['cookie'])
            self.session.cookies.set('datadome',challenge['cookie'])
            return

        except Exception as e:
            log.info(e)
            self.error('Failed to solve challenge. Sleeping...')
            time.sleep(int(self.task["DELAY"]))
            return

    def retrieveSizes(self):
        while True:
            self.prepare('Getting product data...')
            
            self.relayCat = 'Relay42_Category'  #soup.find('input',{'value':'Product Pages'})['name']
            self.webhookData['image'] = f'https://images.footlocker.com/is/image/FLEU/{self.baseSku}_01?wid=763&hei=538&fmt=png-alpha'
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
                self.error(f"error: {str(e)}")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue

            if retrieveSizes.status_code == 503:
                self.info('Queue...')
                
                time.sleep(int(self.task["DELAY"]))
                continue

            elif retrieveSizes.status_code == 404:
                self.error('Sold Out. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                continue

            elif retrieveSizes.status_code == 403:
                if 'nginx' in retrieveSizes.text:
                    self.error('Blocked. Rotating Proxy')
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    continue
                else:
                    self.error('Blocked by DataDome (Solving Challenge...)')
                    self.solveDD(retrieveSizes)

            
            if retrieveSizes.status_code == 200:

                try:
                    response = self.session.get(self.baseUrl,headers={
                        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "user-agent":self.userAgent
                    })
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    log.info(e)
                    self.error(f"error: {str(e)}")
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    time.sleep(int(self.task["DELAY"]))
                    continue

                self.start = time.time()
                try:
                    data = retrieveSizes.json()
                except Exception as e:
                    log.info(e)
                    self.error('Failed to get product data. Retrying...')
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    time.sleep(int(self.task["DELAY"]))
                    continue
            
                if 'sold out' in retrieveSizes.text.lower():
                    self.error('Sold Out. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    continue

                try:
                    htmlContent = data['content'].replace('\n','').replace("\\", "")
                except Exception as e:
                    log.info(e)
                    self.error('Failed to get product data. Retrying...')
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    time.sleep(int(self.task["DELAY"]))
                    continue
                
                try:
                    soup = BeautifulSoup(htmlContent,"html.parser")
                    soup2 = BeautifulSoup(response.text, "html.parser")

                    self.syncToken = soup2.find('input',{'name':'SynchronizerToken'})['value']
                    eu_sizes = soup.find_all('section',{'class':'fl-accordion-tab--content'})[0].find_all('button')
                except:
                    self.error('Sizes Not Found')
                    time.sleep(int(self.task["DELAY"]))
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
                    self.error('Sizes Not Found')
                    time.sleep(int(self.task["DELAY"]))
                    continue

                    
                if self.task["SIZE"].lower() != "random":
                    if self.task["SIZE"] not in sizes:
                        self.error('Size Not Found')
                        time.sleep(int(self.task["DELAY"]))
                        continue
                    else:
                        for size in allSizes:
                            if size.split(':')[0] == self.task["SIZE"]:
                                self.size = size.split(':')[0]
                                self.sizeSku = size.split(":")[1]
                                self.warning(f'Found Size => {self.size}')

                
                else:
                    selected = random.choice(allSizes)
                    self.size = selected.split(":")[0]
                    self.sizeSku = selected.split(":")[1]
                    self.warning(f'Found Size => {self.size}')

                # self.addToCart()
                return

            else:
                self.error('Failed to get product data. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                continue
    
    def addToCart(self):
        while True:
            self.prepare('Carting product...')
            params = {
                'SynchronizerToken':self.syncToken,
                'Ajax': True,
                self.relayCat: 'Product Pages',
                f'acctab-tabgroup-{self.tabgroup}': None,
                f'Quantity_{self.sizeSku}': 1,
                'SKU': self.sizeSku
            }

            try:
                atcResponse = self.session.post(f'{self.baseUrl}/en/addtocart',params=params,headers={
                    "accept": "application/json, text/javascript, */*; q=0.01",
                    "accept-language": "en-US,en;q=0.9",
                    "x-requested-with": "XMLHttpRequest",
                    "user-agent":self.userAgent,
                    "origin": "https://www.footlocker.co.uk"
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue

            if atcResponse.status_code == 503:
                self.info('Queue...')
                time.sleep(int(self.task["DELAY"]))
                continue

            elif atcResponse.status_code == 403:
                if 'nginx' in atcResponse.text:
                    self.error('Blocked. Rotating Proxy')
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    continue
                else:
                    self.error('Blocked by DataDome (Solving Challenge...)')
                    self.solveDD(atcResponse)

            elif atcResponse.status_code == 200:
                try:
                    self.syncToken = atcResponse.text.split('ViewCart-Checkout?SynchronizerToken=')[1].split('\\"')[0]
                    self.productPrice = atcResponse.text.split('price:\\"')[1].split('\\"')[0]
                except Exception:
                    self.error('Failed to cart. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    continue

                updateConsoleTitle(True,False,SITE)
                self.success("Added to cart!")
                # self.checkoutDispatch()
                return

            else:
                self.error(f'Failed to cart [{str(atcResponse.status_code)}]. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                continue

    def checkoutDispatch(self):
        while True:
            self.prepare('Getting checkout data...')

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
                self.error(f"error: {str(e)}")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue

            if checkoutOverviewPage.status_code == 503:
                self.info('Queue...')
                time.sleep(int(self.task["DELAY"]))
                continue

            elif checkoutOverviewPage.status_code == 403:
                if 'nginx' in checkoutOverviewPage.text:
                    self.error('Blocked. Rotating Proxy')
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    continue
                else:
                    self.error('Blocked by DataDome (Solving Challenge...)')
                    self.solveDD(checkoutOverviewPage)

            elif checkoutOverviewPage.status_code == 200 or checkoutOverviewPage.status_code == 302:
                self.referer = checkoutOverviewPage.url
                try:

                    soup = BeautifulSoup(checkoutOverviewPage.text, "html.parser")
                    self.PaymentServiceSelection = soup.find('input',{'name':'PaymentServiceSelection'})['value']
                    self.shipMethodUUID = soup.find('input',{'name':'ShippingMethodUUID'})['value']
                    self.shippingAddressId = soup.find('input',{'name':'shipping_AddressID'})['value']
                    # billingAddressId = soup.find('input',{'name':'billing_AddressID'})['value']
                except Exception as e:
                    log.info(e)
                    self.error('Failed to get checkout data. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    continue

                self.warning('Got checkout data')
                return

            else:
                self.error(f'Failed to get checkout data [{str(checkoutOverviewPage.status_code)}]. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                continue

    def submitShipping(self):
        while True:
            self.prepare('Submitting Shipping...')



            try:
                
                form = "SynchronizerToken={}&isshippingaddress=&billing_Title=common.account.salutation.mr.text&billing_FirstName={}&billing_LastName={}&billing_CountryCode={}&billing_Address1={}&billing_Address2={}&billing_Address3={}&billing_City={}&billing_PostalCode={}&billing_PhoneHome={}&billing_BirthdayRequired=true&billing_Birthday_Day={}&billing_Birthday_Month={}&billing_Birthday_Year={}&email_Email={}&billing_ShippingAddressSameAsBilling=true&isshippingaddress=&shipping_Title=common.account.salutation.mr.text&shipping_FirstName=&shipping_LastName=&SearchTerm=&shipping_CountryCode={}&shipping_Address1=&shipping_Address2=&shipping_Address3=&shipping_City=&shipping_PostalCode=&shipping_PhoneHome=&shipping_AddressID={}&CheckoutRegisterForm_Password=&promotionCode=&PaymentServiceSelection={}&UserDeviceTypeForPaymentRedirect=Desktop&UserDeviceFingerprintForPaymentRedirect={}&ShippingMethodUUID={}&termsAndConditions=on&GDPRDataComplianceRequired=true&sendOrder=".format(
                    self.syncToken,
                    self.profile['firstName'],
                    self.profile['lastName'],
                    self.profile['countryCode'],
                    self.profile['addressOne'],
                    self.profile['house'],
                    self.profile['addressTwo'],
                    self.profile['city'],
                    self.profile['zip'],
                    self.profile['phone'],
                    random.randint(1,25),#day
                    random.randint(1,12), #month
                    random.randint(1970,2000), #year
                    self.profile['email'],
                    self.profile['countryCode'],
                    self.shippingAddressId,
                    self.PaymentServiceSelection,
                    footlocker_snare(self.baseUrl),
                    self.shipMethodUUID
                )
            except:
                self.error('Failed to construct shipping form. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                continue

            
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
                self.error(f"error: {str(e)}")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue

            if checkoutOverviewDispatch.status_code == 503:
                self.info('Queue...')
                time.sleep(int(self.task["DELAY"]))
                continue

            elif checkoutOverviewDispatch.status_code == 403:
                if 'nginx' in checkoutOverviewDispatch.text:
                    self.error('Blocked. Rotating Proxy')
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    continue
                else:
                    self.error('Blocked by DataDome (Solving Challenge...)')
                    self.solveDD(checkoutOverviewDispatch)

            elif checkoutOverviewDispatch.status_code == 200 and 'OrderID' in checkoutOverviewDispatch.url or checkoutOverviewDispatch.status_code == 302 and 'OrderID' in checkoutOverviewDispatch.url:                
                self.responseText = checkoutOverviewDispatch.text
                self.responseUrl = checkoutOverviewDispatch.url

                self.warning('Submitted Shipping')
                return

            else:
                self.error(f'Failed to submit shipping [{str(checkoutOverviewDispatch.status_code)}]. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                continue

    def submitPayment(self):
        while True:

            self.prepare('Submitting Payment...')
            
            payload = {}
            try:
                soup = BeautifulSoup(self.responseText,"html.parser")
                self.adyeninputs = soup.find_all("input")
                for item in self.adyeninputs:
                    payload.update({item["name"]:item["value"]})

                self.webhookData['product'] = payload['riskdata.basket.item1.productTitle']
                self.webhookData['price'] = '{} {}'.format(self.productPrice, payload['currencyCode'])
                
            except:
                self.error("Error loading payment form")
                time.sleep(int(self.task["DELAY"]))
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
                self.error(f"error: {str(e)}")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue

            if payment.status_code == 503:
                self.info('Queue...')
                time.sleep(int(self.task["DELAY"]))
                continue

            elif payment.status_code == 403:
                if 'nginx' in payment.text:
                    self.error('Blocked. Rotating Proxy')
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    continue
                else:
                    self.error('Blocked by DataDome (Solving Challenge...)')
                    self.solveDD(payment)

            elif payment.status_code == 200 :                
                self.success('Payment Submitted')

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

                    self.prepare("Getting paypal checkout...")
                    try:
                        pp_req = self.session.post("https://live.adyen.com/hpp/redirectPayPal.shtml",data=payload,headers={
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
                        log.info(e)
                        self.error(f"error: {str(e)}")
                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                        time.sleep(int(self.task["DELAY"]))
                        continue

                    if "paypal" in str(pp_req.url):
                        self.success("Got paypal checkout!")
                        updateConsoleTitle(False,True,SITE)
                        self.end = time.time() - self.start
                        self.webhookData['speed'] = self.end
                        self.webhookData['url'] = storeCookies(
                            pp_req.url,
                            self.session,
                            self.webhookData['product'],
                            self.webhookData['image'],
                            self.webhookData['price']
                        )
                        return
                      
                            
                    else:
                        self.error("Error getting PayPal Url")
                        time.sleep(int(self.task["DELAY"]))
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
                    payload["card.cardNumber"] = self.profile['card']['cardNumber']
                    payload["card.cardHolderName"] = "{} {}".format(self.profile['firstName'], self.profile['lastName'])
                    payload["card.cvcCode"] = self.profile['card']['cardCVV']
                    payload["card.expiryMonth"] = self.profile['card']['cardMonth']
                    payload["card.expiryYear"] = self.profile['card']['cardYear']
                    payload["shopperBehaviorLog"] = {"numberBind":"1","holderNameBind":"1","cvcBind":"1","deactivate":"3","activate":"2","numberFieldFocusCount":"2","numberFieldLog":"fo@42,cl@42,cl@261,bl@347,fo@494,Cd@498,KL@499,Cu@500,ch@512,bl@512","numberFieldClickCount":"2","numberFieldBlurCount":"2","numberFieldKeyCount":"2","numberFieldChangeCount":"1","numberFieldEvHa":"total=0","holderNameFieldFocusCount":"1","holderNameFieldLog":"fo@512,cl@512,Sd@522,KL@525,KL@526,Su@526,KL@527,KL@528,Ks@530,Sd@531,Su@534,Kb@535,Kb@536,Kb@538,Kb@539,KL@543,KL@544,KL@545,Ks@548,Sd@549,KL@550,Su@551,KL@551,KL@553,KL@555,KL@556,KL@557,KL@558,KL@559,KU@560,ch@560,bl@560","holderNameFieldClickCount":"1","holderNameFieldKeyCount":"25","holderNameUnkKeysFieldLog":"9@560","holderNameFieldChangeCount":"1","holderNameFieldEvHa":"total=0","holderNameFieldBlurCount":"1","cvcFieldFocusCount":"1","cvcFieldLog":"fo@624,cl@625,KN@653,KN@656,KN@657,ch@672,bl@672","cvcFieldClickCount":"1","cvcFieldKeyCount":"3","cvcFieldChangeCount":"1","cvcFieldEvHa":"total=0","cvcFieldBlurCount":"1"}

                    self.ccPayload = payload

                return

            else:
                self.error(f'Failed to submit payment [{str(payment.status_code)}]. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                continue

    def card(self):
        while True:
            self.prepare("Getting card checkout...")

            try:
                response = self.session.post("https://live.adyen.com/hpp/completeCard.shtml",data=self.ccPayload,headers={
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
                log.info(e)
                self.error(f"error: {str(e)}")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue

            if response.status_code == 200:

                try:
                    payerAuth = self.session.get(response.url, headers={
                        'Referer':'https://live.adyen.com/hpp/pay.shtml',
                        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'User-Agent': self.userAgent,
                    })
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    log.info(e)
                    self.error(f"error: {str(e)}")
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    time.sleep(int(self.task["DELAY"]))
                    continue

                try:
                    soup = BeautifulSoup(payerAuth.text, "html.parser")
                    self.pareq = soup.find('input',{'name':'PaReq'})['value']
                    self.MD= soup.find('input',{'name':'MD'})['value']
                except:
                    logger.error(SITE,self.taskID,'Failed to get card checkout [failed to parse response]. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    continue
                    
                self.Dpayload = {
                    "TermUrl":"https://live.adyen.com/hpp/complete3dIntermediate.shtml",
                    "PaReq":self.pareq,
                    "MD":self.MD,
                    "shopperBehaviorLog":""
                }

                three_d_data = threeDSecure.solve(
                    self.session,
                    self.profile,
                    self.Dpayload,
                    self.webhookData,
                    self.taskID,
                    self.baseUrl
                )
                if three_d_data == False:
                    self.error("Checkout Failed (3DS Declined or Failed). Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue

                try:
                    response2 = self.session.post('https://live.adyen.com/hpp/complete3dIntermediate.shtml',headers={
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                        'content-type': 'application/x-www-form-urlencoded',
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'origin': 'https://verifiedbyvisa.acs.touchtechpayments.com',
                        'referer':'https://verifiedbyvisa.acs.touchtechpayments.com/v1/payerAuthentication',
                    }, data=three_d_data)
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    log.info(e)
                    self.error(f"error: {str(e)}")
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    time.sleep(int(self.task["DELAY"]))
                    continue

                if response2.status_code in [200,302]:
                    try:
                        response3 = self.session.post('https://live.adyen.com/hpp/complete3d.shtml',data=three_d_data,headers={
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                            'content-type': 'application/x-www-form-urlencoded',
                            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                            'origin': 'https://verifiedbyvisa.acs.touchtechpayments.com',
                            'referer':'https://live.adyen.com/hpp/complete3dIntermediate.shtml',
                        })
                    except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                        log.info(e)
                        self.error(f"error: {str(e)}")
                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                        time.sleep(int(self.task["DELAY"]))
                        continue

                    if response3.status_code in [200,302]:

                        self.success("Checkout successful")
                        updateConsoleTitle(False,True,SITE)
                        self.end = time.time() - self.start
                        self.webhookData['speed'] = self.end

                        print(response3.url)
                        return

                else:
                    self.error(f'Failed to get card checkout [{str(response.status_code)}]. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    continue
            
            else:
                self.error(f'Failed to get card checkout [{str(response.status_code)}]. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                continue
    
    
    def sendToDiscord(self):
        while True:
            
            self.webhookData['proxy'] = self.session.proxies

            sendNotification(SITE,self.webhookData['product'])

            try:
                Webhook.success(
                    webhook=loadSettings()["webhook"],
                    site=SITE,
                    url=self.webhookData['url'],
                    image=self.webhookData['image'],
                    title=self.webhookData['product'],
                    size=self.size,
                    price=self.webhookData['price'],
                    paymentMethod=self.task['PAYMENT'].strip().title(),
                    product=self.webhookData['product_url'],
                    profile=self.task["PROFILE"],
                    proxy=self.webhookData['proxy'],
                    speed=self.webhookData['speed']
                )
                self.secondary("Sent to discord!")
                while True:
                    pass
            except:
                self.alert("Failed to send webhook. Checkout here ==> {}".format(self.webhookData['url']))


