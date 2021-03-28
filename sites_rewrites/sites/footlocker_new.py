import requests
from bs4 import BeautifulSoup
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
from datetime import timezone, datetime
import uuid

from utils.captcha import captcha
from utils.logger import logger
from utils.webhook import Webhook
from utils.log import log
from utils.datadome import datadome
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
class FOOTLOCKER_NEW:
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
            self.session = requests.session()
            # self.session = scraper()
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
            self.error('Region Not Supported')
            time.sleep(10)
            sys.exit()

        # self.baseSite = 'http://gocyberit.com.global.prod.fastly.net'
        self.lastServed = None
        self.tasks()

    def tasks(self):
            
        self.retrieveSizes()
        self.sess()
        self.addToCart()

        self.quickCheckout()
       
        # self.setEmail()
        # self.submitShipping()
        self.paypal()

        self.sendToDiscord()



    def retrieveSizes(self):
        while True:
            self.prepare('Getting product data...')
            
            self.relayCat = 'Relay42_Category'  #soup.find('input',{'value':'Product Pages'})['name']

            # self.session.get(self.baseUrl)
            # url = '{}/en/product/{}/{}.html'.format(self.baseUrl, self.task['PRODUCT'], self.task['PRODUCT'])
            url = '{}/api/products/pdp/{}?timestamp={}'.format(self.baseUrl, self.task['PRODUCT'], int(datetime.now(tz=timezone.utc).timestamp() * 1000))
            try:
                retrieveSizes = self.session.get(url,headers={
                    'host':self.baseUrl.split('https://')[1],
                    'origin':self.baseUrl,
                    "user-agent":self.userAgent,
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
                    'sec-fetch-dest': 'empty'
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
                    try:
                        
                        challengeUrl = retrieveSizes.json()['url']
                        cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        while cookie['cookie'] == None:
                            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                            cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        
                        del self.session.cookies['datadome']
                        self.session.cookies.set('datadome',cookie['cookie'], domain=self.baseUrl.split('https://www')[1])
                        continue

                    except Exception as e:
                        self.error('Failed to solve challenge. Sleeping...')
                        time.sleep(int(self.task["DELAY"]))
                        continue

            
            if retrieveSizes.status_code == 200:
                self.start = time.time()
                try:
                    productData = json.loads(retrieveSizes.text)
                    # url = retrieveSizes.text.split('"@id":"')[1].split('"')[0]
                    # regex = r"window.footlocker.STATE_FROM_SERVER = {(.+)}"
                    # matches = re.search(regex, retrieveSizes.text, re.MULTILINE)
                    # productData = json.loads(matches.group().split('window.footlocker.STATE_FROM_SERVER = ')[1])
                    # eu_sizes = productData['details']['sizes'][url.split(self.baseUrl)[1]]

                    # self.webhookData['price'] = str(productData['details']['data'][url.split(self.baseUrl)[1]][0]['price']['formattedValue'])
                    # self.webhookData['product'] = str(productData['details']['product'][url.split(self.baseUrl)[1]]['name'])
                    eu_sizes = productData['sellableUnits']
                    self.webhookData['price'] = str(productData['variantAttributes'][0]['price']['formattedValue'])
                    self.webhookData['product'] = str(productData['name'])
                    self.webhookData['image'] = f'https://images.footlocker.com/is/image/FLEU/{self.baseSku}_01?wid=763&hei=538&fmt=png-alpha'

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


                allSizes = []
                sizes = []

                for s in eu_sizes:
                    try:
                        sizes.append(s['attributes'][0]['value'])
                        allSizes.append('{}:{}'.format(s['attributes'][0]['value'], s['attributes'][0]['id']))
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
                print(retrieveSizes.text)
                self.error(f'Failed to get product data [{str(retrieveSizes.status_code)}]. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                continue

    def sess(self):
        while True:
            self.prepare('Getting session...')

            s_headers = {
                'host':self.baseUrl.split('https://')[1],
                'origin':self.baseUrl,
                "user-agent":self.userAgent,
                'upgrade-insecure-requests': '1',
                'x-fl-request-id': str(uuid.uuid1()),
                "x-api-lang": "en-GB",
                'cache-control': 'private, no-cache, no-store, must-revalidate, max-age=0, stale-while-revalidate=0',
                'pragma': 'no-cache',
                'Connection': 'close',
                "accept": "application/json",
                'fastly-ff':''
                # "accept-encoding": "gzip, deflate, br",
            }

            if self.lastServed != None:
                s_headers['fastly-ff'] = str(self.lastServed)


            try:
                response = self.session.get(f'{self.baseUrl}/api/session?timestamp={int(datetime.now(tz=timezone.utc).timestamp() * 1000)}',headers=s_headers)
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue

            if response.headers['X-Served-By']:
                self.lastServed = response.headers['X-Served-By']
            else:
                self.lastServed = None
            

            if response.status_code == 503:
                self.info('Queue...')
                time.sleep(int(self.task["DELAY"]))
                continue

            elif response.status_code == 403:
                if 'nginx' in response.text:
                    self.error('Blocked. Rotating Proxy')
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    continue
                else:
                    self.error('Blocked by DataDome (Solving Challenge...)')
                    try:
                        
                        challengeUrl = response.json()['url']
                        cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        while cookie['cookie'] == None:
                            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                            cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        
                        del self.session.cookies['datadome']
                        self.session.cookies.set('datadome',cookie['cookie'], domain=self.baseUrl.split('https://www')[1])
                        continue

                    except Exception as e:
                        self.error('Failed to solve challenge. Sleeping...')
                        time.sleep(int(self.task["DELAY"]))
                        continue

            elif response.status_code == 200:
                try:
                    self.csrf = response.json()['data']['csrfToken']
                except Exception:
                    self.error('Failed to session [failed to parse response]. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    continue

                self.warning('Got session')
                # self.checkoutDispatch()
                return

            else:
                self.error(f'Failed to get session [{str(response.status_code)}]. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                continue
    

    def addToCart(self):
        while True:
            self.prepare('Carting product...')
            data = {"productQuantity":1,"productId":self.sizeSku}

            atc_headers = {
                "user-agent":self.userAgent,
                'host':self.baseUrl.split('https://')[1],
                'origin':self.baseUrl,
                'upgrade-insecure-requests': '1',
                # 'host': self.baseUrl,
                'x-fl-request-id': str(uuid.uuid1()),
                "x-api-lang": "en-GB",
                "x-csrf-token": self.csrf,
                "x-fl-productid": self.sizeSku,
                'cache-control': 'private, no-cache, no-store, must-revalidate, max-age=0, stale-while-revalidate=0',
                'pragma': 'no-cache',
                'Connection': 'close',
                "accept": "application/json",
                # "accept-encoding": "gzip, deflate, br",
                'fastly-ff':''
            }

            if self.lastServed != None:
                atc_headers['fastly-ff'] = str(self.lastServed)

            try:
                atcResponse = self.session.post(f'{self.baseUrl}/api/users/carts/current/entries?timestamp={int(datetime.now(tz=timezone.utc).timestamp() * 1000)}',
                json=data,headers=atc_headers)
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue
            

            if atcResponse.headers['X-Served-By']:
                self.lastServed = atcResponse.headers['X-Served-By']
            else:
                self.lastServed = None
            
            

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
                    try:
                        
                        challengeUrl = atcResponse.json()['url']
                        cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        while cookie['cookie'] == None:
                            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                            cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        
                        del self.session.cookies['datadome']
                        self.session.cookies.set('datadome',cookie['cookie'], domain=self.baseUrl.split('https://www')[1])
                        continue

                    except Exception as e:
                        self.error('Failed to solve challenge. Sleeping...')
                        time.sleep(int(self.task["DELAY"]))
                        continue

            elif atcResponse.status_code == 200:

                updateConsoleTitle(True,False,SITE)
                self.success("Added to cart!")
                # self.checkoutDispatch()
                return

            else:
                print(atcResponse.text)
                self.error(f'Failed to cart [{str(atcResponse.status_code)}]. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                continue

    def quickCheckout(self):
        while True:
            self.prepare('Submitting shipping...')
            data = {
                "checkoutType": 'EXPRESS',
                "nonce": str(uuid.uuid1()),
                "details": {
                    "email": self.profile['email'],
                    "firstName": self.profile['firstName'],
                    "lastName": self.profile['lastName'],
                    "payerId": str(uuid.uuid1()),
                    "shippingAddress": {
                        "recipientName": self.profile['firstName'] +' '+ self.profile['lastName'],
                        "line1": '{} {}'.format(self.profile['house'], self.profile['addressOne']),
                        "line2": self.profile['addressTwo'],
                        "city": self.profile['city'],
                        # "state": state.shortCode,
                        "postalCode": self.profile['zip'],
                        "countryCode": self.profile['countryCode'],
                        "countryCodeAlpha2": self.profile['countryCode'],
                        "locality": self.profile['city'],
                        # "region": state.shortCode
                    },
                    "phone": self.profile['phone'],
                    "countryCode": self.profile['countryCode'],
                    "billingAddress": {
                        "recipientName": self.profile['firstName'] +' '+ self.profile['lastName'],
                        "line1": '{} {}'.format(self.profile['house'], self.profile['addressOne']),
                        "line2": self.profile['addressTwo'],
                        "city": self.profile['city'],
                        # "state": state.shortCode,
                        "postalCode": self.profile['zip'],
                        "countryCode": self.profile['countryCode'],
                        "countryCodeAlpha2": self.profile['countryCode'],
                        "locality": self.profile['city'],
                        # "region": state.shortCode
                    }

                },
                "type": 'PayPalAccount'
            }


            try:   
                response = self.session.post(f'{self.baseUrl}/api/users/carts/current/paypal?timestamp={int(datetime.now(tz=timezone.utc).timestamp() * 1000)}',
                json=data,headers={
                    'host':self.baseUrl.split('https://')[1],
                    'origin':self.baseUrl,
                    "user-agent":self.userAgent,
                    'upgrade-insecure-requests': '1',
                    # 'host': self.baseUrl,
                    'x-fl-request-id': str(uuid.uuid1()),
                    "x-api-lang": "en-GB",
                    "x-csrf-token": self.csrf,
                    'cache-control': 'private, no-cache, no-store, must-revalidate, max-age=0, stale-while-revalidate=0',
                    'pragma': 'no-cache',
                    'Connection': 'close',
                    "accept": "application/json",
                    'referer':self.baseUrl +'/cart',
                    # "accept-encoding": "gzip, deflate, br",
                    "accept-language": "en-US"
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue


            

            if response.status_code == 503:
                self.info('Queue...')
                time.sleep(int(self.task["DELAY"]))
                continue

            elif response.status_code == 403:
                if 'nginx' in response.text:
                    self.error('Blocked. Rotating Proxy')
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    continue
                else:
                    self.error('Blocked by DataDome (Solving Challenge...)')
                    try:
                        
                        challengeUrl = response.json()['url']
                        cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        while cookie['cookie'] == None:
                            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                            cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        
                        del self.session.cookies['datadome']
                        self.session.cookies.set('datadome',cookie['cookie'], domain=self.baseUrl.split('https://www')[1])
                        continue

                    except Exception as e:
                        self.error('Failed to solve challenge. Sleeping...')
                        time.sleep(int(self.task["DELAY"]))
                        continue

            elif response.status_code == 200:

                self.warning('Successfully set shipping')
                # self.checkoutDispatch()
                return

            else:
                self.error(f'Failed to set shipping [{str(response.status_code)}]. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                continue

    def setEmail(self):
        while True:
            self.prepare('Setting email...')


            try:
                response = self.session.put('{}/api/users/carts/current/email/{}?timestamp={}'.format(
                    self.baseUrl, self.profile['email'], int(datetime.now(tz=timezone.utc).timestamp() * 1000)
                ),headers={
                    'host':self.baseUrl.split('https://')[1],
                    'origin':self.baseUrl,
                    'x-csrf-token':self.csrf,
                    'x-api-lang':'en-GB',
                    'accept-language':'en-GB,en;q=0.9',
                    'sec-ch-ua-mobile':'?0',
                    'user-agent':self.userAgent,
                    'accept':'application/json',
                    'x-fl-request-id':str(uuid.uuid1()),
                    'sec-fetch-site':'same-origin',
                    'sec-fetch-mode':'cors',
                    'sec-fetch-dest':'empty',
                    'referer':f'{self.baseUrl}/en/checkout',
                    'accept-encoding':'gzip, deflate, br'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue



            if response.status_code == 503:
                self.info('Queue...')
                time.sleep(int(self.task["DELAY"]))
                continue

            elif response.status_code == 403:
                if 'nginx' in response.text:
                    self.error('Blocked. Rotating Proxy')
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    continue
                else:
                    self.error('Blocked by DataDome (Solving Challenge...)')
                    try:
                        
                        challengeUrl = response.json()['url']
                        cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        while cookie['cookie'] == None:
                            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                            cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        
                        del self.session.cookies['datadome']
                        self.session.cookies.set('datadome',cookie['cookie'], domain=self.baseUrl.split('https://www')[1])
                        continue

                    except Exception as e:
                        self.error('Failed to solve challenge. Sleeping...')
                        time.sleep(int(self.task["DELAY"]))
                        continue

            elif response.status_code == 200:

                self.warning('Set email')
                # self.checkoutDispatch()
                return

            else:
                self.error(f'Failed to set email [{str(response.status_code)}]. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                continue

    def submitShipping(self):
        while True:
            self.prepare('Submitting Shipping...')


            try:


                data = {
                    "shippingAddress":{
                        "setAsDefaultBilling":False,
                        "setAsDefaultShipping":False,
                        "firstName":self.profile['firstName'],
                        "lastName":self.profile['lastName'],
                        "email":self.profile['email'],
                        "phone":self.profile['phone'],
                        "country":{
                            "isocode":self.profile['countryCode'].upper(),
                            "name":self.profile['country'].title()
                        },
                        "id":None,
                        "setAsBilling":True,
                        "type":"default",
                        "line1":self.profile['addressOne'] + ' ' + self.profile['addressTwo'],
                        "line2":self.profile['house'],
                        "companyName":"",
                        "postalCode":self.profile['zip'],
                        "town":self.profile['city'],
                        "shippingAddress":True
                    }
                }

            except:
                self.error('Failed to construct shipping form. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                continue

            try:
                checkoutOverviewDispatch = self.session.post('{}/api/users/carts/current/addresses/shipping?timestamp={}'.format(self.baseUrl, int(datetime.now(tz=timezone.utc).timestamp() * 1000)),
                json=data,headers={
                    'host':self.baseUrl.split('https://')[1],
                    'origin':self.baseUrl,
                    'x-csrf-token':self.csrf,
                    'x-api-lang':'en-GB',
                    'accept-language':'en-GB,en;q=0.9',
                    'sec-ch-ua-mobile':'?0',
                    'user-agent':self.userAgent,
                    'accept':'application/json',
                    'content-type':'application/json',
                    'x-fl-request-id':str(uuid.uuid1()),
                    'sec-fetch-site':'same-origin',
                    'sec-fetch-mode':'cors',
                    'sec-fetch-dest':'empty',
                    'referer':f'{self.baseUrl}/en/checkout',
                    # 'accept-encoding':'gzip, deflate, br'
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
                    try:
                        
                        challengeUrl = checkoutOverviewDispatch.json()['url']
                        cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        while cookie['cookie'] == None:
                            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                            cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        
                        del self.session.cookies['datadome']
                        self.session.cookies.set('datadome',cookie['cookie'], domain=self.baseUrl.split('https://www')[1])
                        continue

                    except Exception as e:
                        self.error('Failed to solve challenge. Sleeping...')
                        time.sleep(int(self.task["DELAY"]))
                        continue

            elif checkoutOverviewDispatch.status_code in [200,201]:                
                self.warning('Submitted Shipping')
                return

            else:
                self.error(f'Failed to submit shipping [{str(checkoutOverviewDispatch.status_code)}]. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                continue

    def paypal(self):
        while True:
            self.prepare('Getting paypal checkout...')
            try:
                response = self.session.get('{}/apigate/payment/methods?channel=WEB&timestamp={}'.format(
                    self.baseUrl, int(datetime.now(tz=timezone.utc).timestamp() * 1000)
                ),headers={
                    "user-agent":self.userAgent,
                    'host':self.baseUrl.split('https://')[1],
                    'origin':self.baseUrl,
                    'upgrade-insecure-requests': '1',
                    # 'host': self.baseUrl,
                    'x-fl-request-id': str(uuid.uuid1()),
                    "x-api-lang": "en-GB",
                    "x-csrf-token": self.csrf,
                    "x-fl-productid": self.sizeSku,
                    'cache-control': 'private, no-cache, no-store, must-revalidate, max-age=0, stale-while-revalidate=0',
                    'pragma': 'no-cache',
                    'Connection': 'close',
                    "accept": "application/json",
                    # "accept-encoding": "gzip, deflate, br",
                    "accept-language": "en-US",
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-user': '?1',
                    'sec-fetch-dest': 'empty'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue

            if response.status_code == 503:
                self.info('Queue...')
                time.sleep(int(self.task["DELAY"]))
                continue

            elif response.status_code == 403:
                if 'nginx' in response.text:
                    self.error('Blocked. Rotating Proxy')
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    continue
                else:
                    self.error('Blocked by DataDome (Solving Challenge...)')
                    try:
                        
                        challengeUrl = response.json()['url']
                        cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        while cookie['cookie'] == None:
                            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                            cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl, self.baseUrl, self.userAgent, self.task['PROXIES'], self.proxies)
                        
                        del self.session.cookies['datadome']
                        self.session.cookies.set('datadome',cookie['cookie'], domain=self.baseUrl.split('https://www')[1])
                        continue

                    except Exception as e:
                        self.error('Failed to solve challenge. Sleeping...')
                        time.sleep(int(self.task["DELAY"]))
                        continue

            elif response.status_code == 200:
                try:
                    self.tokenizationKey = response.json()[1]['key']
                    self.gatewayMerchantId = response.json()[1]['gatewayMerchantId']
                    self.currency = response.json()[1]['currency']

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
                        "line1": self.profile['addressOne'],
                        "line2": self.profile['house'],
                        "city": self.profile['city'],
                        "postalCode": self.profile['zip'],
                        "countryCode": self.profile['countryCode'].upper(),
                        "phone": self.profile['phone'],
                        "recipientName": self.profile['firstName'] + ' ' + self.profile['lastName'],
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
                    self.error("failed to get paypal checkout [error parsing response]")
                    time.sleep(int(self.task["DELAY"]))
                    continue

                try:
                    response2 = self.session.post('https://api.braintreegateway.com/merchants/rfbkw27jcwmw2xgp/client_api/v1/paypal_hermes/create_payment_resource',
                    json=braintreeData,headers={
                        "Accept": "*/*",
                        "accept-language": "en-GB,en;q=0.9",
                        "content-type": "application/json",
                        'Referer':self.baseUrl,
                        "User-Agent":self.userAgent
                    })
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    log.info(e)
                    self.error(f"error: {str(e)}")
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    time.sleep(int(self.task["DELAY"]))
                    continue
                

                if response2.status_code in [200,201,302]:
                    try:
                        paypalRedirect = response2.json()['paymentResource']['redirectUrl']
                    except:
                        self.error("failed to get paypal checkout [error parsing response]")
                        time.sleep(int(self.task["DELAY"]))
                        continue

                    self.end = time.time() - self.start
                    self.webhookData['speed'] = self.end

                    self.success('Got paypal checkout')
                    updateConsoleTitle(False,True,SITE)

                    self.webhookData['url'] = storeCookies(
                        paypalRedirect,
                        self.session,
                        self.webhookData['product'],
                        self.webhookData['image'],
                        self.webhookData['price']
                    )
                    return

                else:
                    self.error(f'Failed to get paypal checkout [{str(response.status_code)}]. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    continue

            else:
                self.error(f'Failed to get paypal checkout [{str(response.status_code)}]. Retrying...')
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
                    region=self.countryCode,
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


