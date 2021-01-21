import requests
from datetime import timezone, datetime
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
import uuid
from urllib3.exceptions import HTTPError
import csv

from utils.logger import logger
from utils.webhook import discord
from utils.log import log
from utils.datadome import datadome
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies, updateConsoleTitle,scraper, footlocker_snare)
SITE = 'FOOTLOCKER'


class FOOTLOCKER_NEW:
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
                self.task['PROXIES'] = 'proxies'
                csvFile.close()
            time.sleep(2)
                
    def __init__(self,task,taskName,rowNumber):
        self.task = task
        self.session = requests.session()
        self.taskID = taskName
        self.rowNumber = rowNumber

        twoCap = loadSettings()["2Captcha"]
        # self.session = scraper()
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        self.countryCode = profile['countryCode'].lower()

        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
        self.baseSku = self.task['PRODUCT']

        if self.countryCode == 'it':
            self.baseUrl = 'https://www.footlocker.it'
            self.baseUrl2 = ''
        elif self.countryCode == 'be':
            self.baseUrl = 'https://www.footlocker.be'
            self.baseUrl2 = ''
        elif self.countryCode == 'at':
            self.baseUrl = 'https://www.footlocker.at'
            self.baseUrl2 = ''
        elif self.countryCode == 'lu':
            self.baseUrl = 'https://www.footlocker.lu'
            self.baseUrl2 = ''
        elif self.countryCode == 'cz':
            self.baseUrl = 'https://www.footlocker.cz'
            self.baseUrl2 = ''
        elif self.countryCode == 'dk':
            self.baseUrl = 'https://www.footlocker.dk'
            self.baseUrl2 = ''
        elif self.countryCode == 'pl':
            self.baseUrl = 'https://www.footlocker.pl'
            self.baseUrl2 = ''
        elif self.countryCode == 'gr':
            self.baseUrl = 'https://www.footlocker.gr'
            self.baseUrl2 = ''
        elif self.countryCode == 'pt':
            self.baseUrl = 'https://www.footlocker.pt'
            self.baseUrl2 = ''
        elif self.countryCode == 'hu':
            self.baseUrl = 'https://www.footlocker.hu'
            self.baseUrl2 = ''
        elif self.countryCode == 'es':
            self.baseUrl = 'https://www.footlocker.es'
            self.baseUrl2 = ''
        elif self.countryCode == 'ie':
            self.baseUrl = 'https://www.footlocker.ie'
            self.baseUrl2 = ''
        elif self.countryCode == 'no':
            self.baseUrl = 'https://www.footlocker.no'
            self.baseUrl2 = ''
        elif self.countryCode == 'se':
            self.baseUrl = 'https://www.footlocker.se'
            self.baseUrl2 = ''
        else:
            logger.error(SITE,self.taskID,'Region not supported. Exiting...')
            time.sleep(10)
            sys.exit()
        
        threading.Thread(target=self.task_checker,daemon=True).start()
        self.collect()

    def collect(self):
        logger.prepare(SITE,self.taskID,'Getting product page...')
        url = '{}/en/product/{}/{}.html'.format(self.baseUrl, self.task['PRODUCT'], self.task['PRODUCT'])
        try:
            retrieve = self.session.get(url)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.collect()

        if retrieve.status_code == 503:
            logger.info(SITE,self.taskID,'Queue...')
            time.sleep(10)
            self.retrieveSizes()

        if retrieve.status_code == 403:
            logger.error(SITE,self.taskID,'Blocked by DataDome (Solving Challenge...)')
            try:
                challengeUrl = retrieve.json()['url']
            except:
                logger.error(SITE,self.taskID,'Failed to get challenge url. Sleeping...')
                time.sleep(10)
                self.collect()
            cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl)
            if cookie['cookie'] == None:
                del self.session.cookies["datadome"]
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl)
                

            del self.session.cookies["datadome"]
            self.session.cookies["datadome"] = cookie['cookie']
            self.collect()


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
               log.info(e)
               logger.error(SITE,self.taskID,'Failed to scrape page (Most likely out of stock). Retrying...')
               time.sleep(int(self.task["DELAY"]))
               self.collect()

            allSizes = []
            sizes = []

        
            for s in eu_sizes:
                try:
                    sizes.append(s['name'])
                    allSizes.append('{}:{}'.format(s['name'], s['code']))
                except:
                    pass


            if len(sizes) == 0:
                logger.error(SITE,self.taskID,'Sizes Not Found')
                time.sleep(int(self.task["DELAY"]))
                self.collect()

                
            if self.task["SIZE"].lower() != "random":
                if self.task["SIZE"] not in sizes:
                    logger.error(SITE,self.taskID,'Size Not Found')
                    time.sleep(int(self.task["DELAY"]))
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


            self.footlockerSession()


        else:
            try:
                status = retrieve.status_code
            except:
                status = 'Unknown'
            logger.error(SITE,self.taskID,f'Failed to get product page => {status}. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.collect()

    def footlockerSession(self):
        logger.prepare(SITE,self.taskID,'Getting session')
        try:
            response = self.session.get(f'{self.baseUrl}/api/session?timestamp={int(datetime.now(tz=timezone.utc).timestamp() * 1000)}',headers={
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
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.footlockerSession()

        if response.status_code == 403:
            logger.error(SITE,self.taskID,'Blocked by DataDome (Solving Challenge...)')
            try:
                challengeUrl = response.json()['url']
            except:
                if 'geo.captcha-delivery' in response.text:
                    try:
                        initialCid = response.text.split("'cid':'")[1].split("',")[0]
                        hsh = response.text.split("'hsh':'")[1].split("',")[0]
                        t = response.text.split("'t':'")[1].split("',")[0]
                        s = response.text.split("'s':'")[1].split("',")[0]
                        challengeUrl = '?initialCid={}&referer={}&hash={}&t={}&s={}&cid{}'.format(initialCid, response.url, hsh, t, s)
                    except Exception as e:
                        log.info(e)
                        logger.error(SITE,self.taskID,'Failed to get challenge url. Sleeping...')
                        time.sleep(10)
                        self.footlockerSession()

                    cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl)
                    if cookie['cookie'] == None:
                        del self.session.cookies["datadome"]
                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                        self.footlockerSession()

                    del self.session.cookies["datadome"]
                    self.session.cookies["datadome"] = cookie['cookie']
                    self.footlockerSession()
                
                else:
                    logger.error(SITE,self.taskID,'Blocked. Sleeping...')
                    time.sleep(10)
                    self.footlockerSession()


                

        # response headers
        # {'Connection': 'keep-alive', 'Server': 'nginx', 'Content-Type': 'application/json', 'breadcrumbId': 'ID-0bca6f96fc0c-1608376547437-1-4514227', 'CDN-Loop': 'Fastly, Fastly, Fastly, Fastly', 'Fastly-Client': '1', 'Fastly-Client-IP': '185.225.156.98', 'fastly-csi-request-id': '1609855924ad6b6376e5e1c85aba612db2a14ca1130285633aedd517472be0497a2ec586f3', 'Fastly-FF': 'vqP8CmUiE4YwMfWvmo2n56G8O131xmrylumhDt9V38E=!LON!cache-lon4255-LON, vqP8CmUiE4YwMfWvmo2n56G8O131xmrylumhDt9V38E=!LON!cache-lon4251-LON, vqP8CmUiE4YwMfWvmo2n56G8O131xmrylumhDt9V38E=!FRA!cache-fra19138-FRA, vqP8CmUiE4YwMfWvmo2n56G8O131xmrylumhDt9V38E=!FRA!cache-fra19158-FRA', 'Fastly-Orig-Accept-Encoding': 'gzip', 'fastly-soc-x-request-id': '1609855924ad6b6376e5e1c85aba612db2a14ca1130285633aedd517472be0497a2ec586f3', 'Fastly-SSL': '1', 'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"', 'sec-ch-ua-mobile': '?0', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'Set-Cookie': 'JSESSIONID=zaqifdyq641tcq2r9ne4dm1n.fzcxwefapipdb238881; Path=/; HTTPOnly', 'True-Client-IP': '185.225.156.98', 'var-tld': 'it', 'X-Akamai-Device-Characteristics': 'is_mobile=false;is_tablet=false', 'X-Akamai-Edgescape': 'country_code=GB,zip=dl2 2bq', 'X-API-GATEWAY-VERSION': '1.0.2099', 'x-api-lang': 'en-GB', 'X-COUNTRY-CODE': 'GB', 'x-fl-asnum': '34119', 'X-FL-Request-ID': 'ngx476c4e00b300962ca9effca983a63375', 'X-FLAPI-SESSION-ID': 'zaqifdyq641tcq2r9ne4dm1n.fzcxwefapipdb238881', 'X-FOOTLOCKER-NEWRELIC-TRANSACTION-NAME': '/{siteId}/session', 'X-Forwarded-For': '185.225.156.98, 157.52.69.51, 185.31.18.58, 10.226.129.22', 'X-Forwarded-Host': 'www.footlocker.it, www.footlocker.it', 'X-Method': 'GET', 'X-PerimeterX-Client-IP': '185.225.156.98', 'X-ZIPCODE': 'dl2 2bq', 'locid': '7677f39b-154b-478a-827d-fb72197e9b9d-ses', 'Content-Encoding': 'gzip', 'Accept-Ranges': 'bytes', 'Via': '1.1 varnish, 1.1 varnish', 'Date': 'Tue, 05 Jan 2021 14:12:03 GMT', 'X-Served-By': 'cache-fra19138-FRA, cache-lon4255-LON', 'X-Cache': 'MISS, MISS', 'X-Cache-Hits': '0, 0', 'X-Timer': 'S1609855924.683253,VS0,VE40', 'X-FL-EDGE': 'Fastly', 'transfer-encoding': 'chunked'}
        if response.status_code == 200:
            try:
                self.csrf = response.json()['data']['csrfToken']
            except:
                logger.error(SITE,self.taskID,'Failed to get session')
                time.sleep(int(self.task["DELAY"]))
                self.footlockerSession()

            logger.warning(SITE,self.taskID,'Got session')
            self.addToCart()
        else:
            logger.error(SITE,self.taskID,'Failed to get session')
            time.sleep(int(self.task["DELAY"]))
            self.footlockerSession()
            

    def addToCart(self):
        logger.prepare(SITE,self.taskID,'Carting product...')
        data = {"productQuantity":1,"productId":self.sizeSku}

        try:
            atcResponse = self.session.post(f'{self.baseUrl}/api/users/carts/current/entries?timestamp={int(datetime.now(tz=timezone.utc).timestamp() * 1000)}',json=data,headers={
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
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()


        if atcResponse.status_code == 403:
            logger.error(SITE,self.taskID,'Blocked by DataDome (Solving Challenge...)')
            try:
                challengeUrl = atcResponse.json()['url']
            except:
                if 'geo.captcha-delivery' in atcResponse.text:
                    try:
                        initialCid = atcResponse.text.split("'cid':'")[1].split("',")[0]
                        hsh = atcResponse.text.split("'hsh':'")[1].split("',")[0]
                        t = atcResponse.text.split("'t':'")[1].split("',")[0]
                        s = atcResponse.text.split("'s':'")[1].split("',")[0]
                        challengeUrl = '?initialCid={}&referer={}&hash={}&t={}&s={}&cid{}'.format(initialCid, atcResponse.url, hsh, t, s)
                    except Exception as e:
                        log.info(e)
                        logger.error(SITE,self.taskID,'Failed to get challenge url. Sleeping...')
                        time.sleep(10)
                        self.addToCart()

                    cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl)
                    if cookie['cookie'] == None:
                        del self.session.cookies["datadome"]
                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                        self.addToCart()

                    del self.session.cookies["datadome"]
                    self.session.cookies["datadome"] = cookie['cookie']
                    self.addToCart()
                
                else:
                    logger.error(SITE,self.taskID,'Blocked. Sleeping...')
                    time.sleep(10)
                    self.addToCart()



        elif atcResponse.status_code == 200:
            logger.warning(SITE,self.taskID,'Successfully carted product')
            self.setEmail()

        elif atcResponse.status_code == 531:
            logger.error(SITE,self.taskID,'Failed to cart (OOS). Retrying...')
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()


    def setEmail(self):
        logger.prepare(SITE,self.taskID,'Setting email...')

        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        self.countryCode = profile['countryCode'].lower()

        try:
            emailPage = self.session.put('{}/api/users/carts/current/email/{}?timestamp={}'.format(self.baseUrl, profile['email'], int(datetime.now(tz=timezone.utc).timestamp() * 1000)),headers={
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
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.setEmail()

        if emailPage.status_code ==403:
            logger.error(SITE,self.taskID,'Blocked by DataDome (Solving Challenge...)')
            try:
                challengeUrl = emailPage.json()['url']
            except:
                if 'geo.captcha-delivery' in emailPage.text:
                    try:
                        initialCid = emailPage.text.split("'cid':'")[1].split("',")[0]
                        hsh = emailPage.text.split("'hsh':'")[1].split("',")[0]
                        t = emailPage.text.split("'t':'")[1].split("',")[0]
                        s = emailPage.text.split("'s':'")[1].split("',")[0]
                        challengeUrl = '?initialCid={}&referer={}&hash={}&t={}&s={}&cid{}'.format(initialCid, emailPage.url, hsh, t, s)
                    except Exception as e:
                        log.info(e)
                        logger.error(SITE,self.taskID,'Failed to get challenge url. Sleeping...')
                        time.sleep(10)
                        self.setEmail()

                    cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl)
                    if cookie['cookie'] == None:
                        del self.session.cookies["datadome"]
                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                        self.setEmail()

                    del self.session.cookies["datadome"]
                    self.session.cookies["datadome"] = cookie['cookie']
                    self.setEmail()
                
                else:
                    logger.error(SITE,self.taskID,'Blocked. Sleeping...')
                    time.sleep(10)
                    self.setEmail()

        if emailPage.status_code in [200,302]:
            logger.warning(SITE,self.taskID,'Email set')
            self.shipping() 

        else:
            logger.error(SITE,self.taskID,'Failed to set email. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.setEmail()

    def shipping(self):
        logger.prepare(SITE,self.taskID,'Submitting shipping...')

        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()

        data = {"shippingAddress":{"setAsDefaultBilling":False,"setAsDefaultShipping":False,"firstName":profile['firstName'],"lastName":profile['lastName'],"email":profile['email'],"phone":profile['phone'],"country":{"isocode":profile['countryCode'].upper(),"name":profile['country'].title()},"id":None,"setAsBilling":True,"type":"default","line1":profile['addressOne'] + ' ' + profile['addressTwo'],"line2":profile['house'],"companyName":"","postalCode":profile['zip'],"town":profile['city'],"shippingAddress":True}}

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
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.shipping()

        if shippingAddress.status_code == 403:
            logger.error(SITE,self.taskID,'Blocked by DataDome (Solving Challenge...)')
            try:
                challengeUrl = shippingAddress.json()['url']
            except:
                if 'geo.captcha-delivery' in shippingAddress.text:
                    try:
                        initialCid = shippingAddress.text.split("'cid':'")[1].split("',")[0]
                        hsh = shippingAddress.text.split("'hsh':'")[1].split("',")[0]
                        t = shippingAddress.text.split("'t':'")[1].split("',")[0]
                        s = shippingAddress.text.split("'s':'")[1].split("',")[0]
                        challengeUrl = '?initialCid={}&referer={}&hash={}&t={}&s={}&cid{}'.format(initialCid, shippingAddress.url, hsh, t, s)
                    except Exception as e:
                        log.info(e)
                        logger.error(SITE,self.taskID,'Failed to get challenge url. Sleeping...')
                        time.sleep(10)
                        self.shipping()

                    cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl)
                    if cookie['cookie'] == None:
                        del self.session.cookies["datadome"]
                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                        self.shipping()

                    del self.session.cookies["datadome"]
                    self.session.cookies["datadome"] = cookie['cookie']
                    self.shipping()

                else:
                    logger.error(SITE,self.taskID,'Blocked. Sleeping...')
                    time.sleep(10)
                    self.shipping()

        data = {"setAsDefaultBilling":False,"setAsDefaultShipping":False,"firstName":profile['firstName'],"lastName":profile['lastName'],"email":profile['email'],"phone":profile['phone'],"country":{"isocode":profile['countryCode'].upper(),"name":profile['country'].title()},"id":None,"setAsBilling":False,"type":"default","line1":profile['addressOne'] + ' ' + profile['addressTwo'],"line2":profile['house'],"companyName":"","postalCode":profile['zip'],"town":profile['city'],"shippingAddress":True}

        try:
            billingAddress = self.session.post('{}/api/users/carts/current/set-billing?timestamp={}'.format(self.baseUrl, int(datetime.now(tz=timezone.utc).timestamp() * 1000)),json=data,headers={
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
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.shipping()

        if billingAddress.status_code == 403:
            logger.error(SITE,self.taskID,'Blocked by DataDome (Solving Challenge...)')
            try:
                challengeUrl = billingAddress.json()['url']
            except:
                if 'geo.captcha-delivery' in billingAddress.text:
                    try:
                        initialCid = billingAddress.text.split("'cid':'")[1].split("',")[0]
                        hsh = billingAddress.text.split("'hsh':'")[1].split("',")[0]
                        t = billingAddress.text.split("'t':'")[1].split("',")[0]
                        s = billingAddress.text.split("'s':'")[1].split("',")[0]
                        challengeUrl = '?initialCid={}&referer={}&hash={}&t={}&s={}&cid{}'.format(initialCid, billingAddress.url, hsh, t, s)
                    except Exception as e:
                        log.info(e)
                        logger.error(SITE,self.taskID,'Failed to get challenge url. Sleeping...')
                        time.sleep(10)
                        self.shipping()

                    cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl)
                    if cookie['cookie'] == None:
                        del self.session.cookies["datadome"]
                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                        self.shipping()
    
                    del self.session.cookies["datadome"]
                    self.session.cookies["datadome"] = cookie['cookie']
                    self.shipping()

                else:
                    logger.error(SITE,self.taskID,'Blocked. Sleeping...')
                    time.sleep(10)
                    self.shipping()


        # print(billingAddress.status_code, shippingAddress.status_code)
        if billingAddress.status_code == 200 and shippingAddress.status_code == 201:
            logger.warning(SITE,self.taskID,'Shipping submitted')
            self.paypal()
        else:
            logger.error(SITE,self.taskID,'Failed to submit shipping. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.shipping()



    def paypal(self):
        logger.prepare(SITE,self.taskID,'Getting paypal link...')

        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        try:
            paymentMethods = self.session.get('{}/apigate/payment/methods?channel=WEB&timestamp={}'.format(self.baseUrl, int(datetime.now(tz=timezone.utc).timestamp() * 1000)),headers={
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
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.paypal()

        if paymentMethods.status_code == 403:
            logger.error(SITE,self.taskID,'Blocked by DataDome (Solving Challenge...)')
            try:
                challengeUrl = paymentMethods.json()['url']
            except:
                if 'geo.captcha-delivery' in paymentMethods.text:
                    try:
                        initialCid = paymentMethods.text.split("'cid':'")[1].split("',")[0]
                        hsh = paymentMethods.text.split("'hsh':'")[1].split("',")[0]
                        t = paymentMethods.text.split("'t':'")[1].split("',")[0]
                        s = paymentMethods.text.split("'s':'")[1].split("',")[0]
                        challengeUrl = '?initialCid={}&referer={}&hash={}&t={}&s={}&cid{}'.format(initialCid, paymentMethods.url, hsh, t, s)
                    except Exception as e:
                        log.info(e)
                        logger.error(SITE,self.taskID,'Failed to get challenge url. Sleeping...')
                        time.sleep(10)
                        self.paypal()

                    cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl)
                    if cookie['cookie'] == None:
                        del self.session.cookies["datadome"]
                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                        self.paypal()
    
                    del self.session.cookies["datadome"]
                    self.session.cookies["datadome"] = cookie['cookie']
                    self.paypal()

                else:
                    logger.error(SITE,self.taskID,'Blocked. Sleeping...')
                    time.sleep(10)
                    self.paypal()
        
        if paymentMethods.status_code == 200:
            self.tokenizationKey = paymentMethods.json()[1]['key']
            self.gatewayMerchantId = paymentMethods.json()[1]['gatewayMerchantId']
            self.currency = paymentMethods.json()[1]['currency']

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

        try:
            paymentResource = self.session.post('https://api.braintreegateway.com/merchants/rfbkw27jcwmw2xgp/client_api/v1/paypal_hermes/create_payment_resource',json=braintreeData,headers={
                "Accept": "*/*",
                "accept-language": "en-GB,en;q=0.9",
                "content-type": "application/json",
                "sec-ch-ua": "\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"",
                # "x-api-lang": "en-GB",
                # "x-csrf-token": self.csrf,
                # "x-fl-productid": self.sizeSku,
                # "x-fl-request-id": "45a40be0-4f57-11eb-87a1-a1e3b40a67ba"
                'Referer':self.baseUrl,
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.paypal()

        try:
            paypalRedirect = paymentResource.json()['paymentResource']['redirectUrl']
        except:
            logger.error(SITE,self.taskID,'Failed to get paypal link. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.paypal()


        logger.warning(SITE,self.taskID, 'Got paypal link')
        self.end = time.time() - self.start
        
        updateConsoleTitle(False,True,SITE)
        logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')
        url = storeCookies(paypalRedirect,self.session, self.productTitle, self.productImage, self.productPrice)
        
        try:
            discord.success(
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
            sendNotification(SITE,self.productTitle)
            while True:
                pass
        except Exception as e:
            log.info(e)
            logger.alert(SITE,self.taskID,'Failed to send webhook. Checkout here ==> {}'.format(url))






   
# logger.warning(SITE,self.taskID, 'Got paypal link')
# self.end = int(datetime.now(tz=timezone.utc).timestamp() * 1000) - self.start
# 
# updateConsoleTitle(False,True,SITE)
# logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')
# url = storeCookies(paypalRedirect.url,self.session, self.productTitle, self.productImage, self.productPrice)
# 
# try:
    # discord.success(
        # webhook=loadSettings()["webhook"],
        # site=SITE,
        # url=url,
        # image=self.productImage,
        # title=self.productTitle,
        # size=self.size,
        # price=self.productPrice,
        # paymentMethod='PayPal',
        # profile=self.task["PROFILE"],
        # product=self.task["PRODUCT"],
        # proxy=self.session.proxies,
        # speed=self.end,
        # region=self.countryCode
    # )
    # sendNotification(SITE,self.productTitle)
    # while True:
        # pass
# except Exception as e:
    # log.info(e)
    # logger.alert(SITE,self.taskID,'Failed to send webhook. Checkout here ==> {}'.format(url))
        





