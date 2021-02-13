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
from urllib.parse import unquote

from utils.logger import logger
from utils.webhook import discord
from utils.log import log
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies, updateConsoleTitle,scraper)
SITE = 'AMBUSH'


class AMBUSH:
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

    def __init__(self, task,taskName, rowNumber):
        self.task = task
        self.session = requests.session()
        self.taskID = taskName
        self.rowNumber = rowNumber

        twoCap = loadSettings()["2Captcha"]

        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        self.countryCode = profile['countryCode']
        # self.session = scraper()
        threading.Thread(target=self.task_checker,daemon=True).start()
        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)


        self.collect()

    def collect(self):
        logger.prepare(SITE,self.taskID,'Getting product page...')
        try:
            retrieve = self.session.get(self.task["PRODUCT"], headers={
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'referer': 'https://www.google.com/',
                'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.collect()

        if retrieve.status_code == 200:
            self.start = time.time()
            logger.warning(SITE,self.taskID,'Got product page')
            try:
                logger.prepare(SITE,self.taskID,'Getting product data...')
                soup = BeautifulSoup(retrieve.text, "html.parser")
                regex = r"__PRELOADED_STATE__ = {(.+)}"
                matches = re.search(regex, retrieve.text, re.MULTILINE)
                if matches:
                    self.urlRegion = retrieve.text.split('window.initialI18nStore = {"')[1].split('"')[0]
                    self.currency = retrieve.text.split('"priceCurrency":"')[1].split('"')[0]
                    prodData = json.loads(matches.group().split('__PRELOADED_STATE__ = ')[1])
                    self.productId = [*prodData['entities']['products'].keys()][0]
                    self.productImage = prodData['entities']['products'][self.productId]['images'][0]['url']
                    self.productPrice = prodData['entities']['products'][self.productId]['price']['formatted']['includingTaxes']
                    self.productTitle = prodData['entities']['products'][self.productId]['shortDescription']
                    availableSizes = prodData['entities']['products'][self.productId]['sizes']

                    allSizes = []
                    sizes = []
                    for s in availableSizes:
                        allSizes.append(s)
                        sizes.append(s["name"])
    
                    if len(sizes) == 0:
                        logger.error(SITE,self.taskID,'Size Not Found')
                        time.sleep(int(self.task["DELAY"]))
                        self.collect()

                        
                    if self.task["SIZE"].lower() != "random":
                        if self.task["SIZE"] not in sizes:
                            logger.error(SITE,self.taskID,'Size Not Found')
                            time.sleep(int(self.task["DELAY"]))
                            self.collect()
                        else:
                            for size in allSizes:
                                if size['name']== self.task["SIZE"]:
                                    self.selectedSize = size
                                    self.size = self.selectedSize['name']
                                    logger.warning(SITE,self.taskID,f'Found Size => {self.size}')
        
                    
                    elif self.task["SIZE"].lower() == "random":
                        self.selectedSize = random.choice(allSizes)
                        self.size = self.selectedSize['name']
                        logger.warning(SITE,self.taskID,f'Found Size => {self.size}')
                    

                        
            except Exception as e:
               log.info(e)
               logger.error(SITE,self.taskID,'Failed to scrape page (Most likely out of stock). Retrying...')
               time.sleep(int(self.task["DELAY"]))
               self.collect()

            if self.task['ACCOUNT EMAIL'] != "":
                self.login()
            else:
                self.addToCart()

        else:
            try:
                status = retrieve.status_code
            except:
                status = 'Unknown'
            logger.error(SITE,self.taskID,f'Failed to get product page => {status}. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.collect()

    def login(self):
        logger.prepare(SITE,self.taskID,'Logging in...')
        try:
            payload = {
                "username":self.task['ACCOUNT EMAIL'],
                "password":self.task['ACCOUNT PASSWORD'],
                "rememberMe":True,
            }
            response = self.session.post('https://www.ambushdesign.com/api/legacy/v1/account/login',json=payload, headers={
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US',
                'referer': 'https://www.ambushdesign.com/',
                'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'content-type': 'application/json',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
                'ff-country': self.countryCode.upper(),
                'ff-currency': self.currency
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.login()
        
        if response.status_code == 200 or response.status_code == 201:
            logger.warning(SITE,self.taskID,'Successfully Logged in')
            self.addToCart()
        else:
            logger.error(SITE,self.taskID,'Failed to login. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.login()


    def addToCart(self):
        logger.prepare(SITE,self.taskID,'Carting products...')

        try:
            me_response = self.session.get('https://www.ambushdesign.com/api/legacy/v1/users/me', headers={
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'referer': 'https://www.ambushdesign.com/',
                'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

        if me_response.status_code == 200:
            try:
                self.bagResponse = me_response.json()
            except:
                logger.error(SITE,self.taskID,'Failed to cart products')
                time.sleep(int(self.task["DELAY"]))
                self.addToCart()
                
        else:
            logger.error(SITE,self.taskID,'Failed to cart products')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

        try:
            bagId = self.bagResponse['bagId']
            self.bagId = bagId
            payload = {
                "customAttributes":"",
                "merchantId":self.selectedSize['stock'][0]['merchantId'],
                "productId":self.productId,
                "quantity":1,
                "scale":self.selectedSize['scale'],
                "size":self.selectedSize['id']
            }
            cart_response = self.session.post(f'https://www.ambushdesign.com/api/commerce/v1/bags/{bagId}/items',json=payload, headers={
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'referer': 'https://www.ambushdesign.com/',
                'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'content-type': 'application/json',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
                'ff-country': self.countryCode.upper(),
                'ff-currency': self.currency
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

        if cart_response.status_code == 200:
            try:
                cart_response.json()
                cart_response.json()['count']
            except:
                logger.error(SITE,self.taskID,'Failed to cart products')
                time.sleep(int(self.task["DELAY"]))
                self.addToCart()
            
            if int(cart_response.json()['count']) > 0:
                updateConsoleTitle(True,False,SITE)
                logger.warning(SITE,self.taskID,'Successfully Carted')
                self.guestCheckout()

            else:
                logger.error(SITE,self.taskID,'Failed to cart products')
                time.sleep(int(self.task["DELAY"]))
                self.addToCart()
        
        else:
            logger.error(SITE,self.taskID,'Failed to cart products')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

    
    def guestCheckout(self):
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()

        logger.prepare(SITE,self.taskID,'Setting guest checkout...')
        try:
            bagId = self.bagResponse['bagId']
            payload = {
                "bagId":bagId,
                "guestUserEmail":profile['email'],
                "usePaymentIntent":True
            }
            response = self.session.post('https://www.ambushdesign.com/api/checkout/v1/orders',json=payload, headers={
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US',
                'referer': 'https://www.ambushdesign.com/',
                'origin': 'https://www.ambushdesign.com',
                'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'content-type': 'application/json',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
                'ff-country': self.countryCode.upper(),
                'ff-currency': self.currency,
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin"
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.guestCheckout()
    

        if response.status_code == 200 or response.status_code == 201:
            try:
                response.json()
                self.countryData = response.json()['checkoutOrder']['billingAddress']['country']
                self.countryName = response.json()['checkoutOrder']['billingAddress']['country']['name']
                self.countryId = response.json()['checkoutOrder']['countryId']
                self.id = response.json()['id']
            except:
                logger.error(SITE,self.taskID,'Failed to set guest checkout')
                time.sleep(int(self.task["DELAY"]))
                self.guestCheckout()


            logger.warning(SITE,self.taskID,'Successfully set guest checkout')
            self.shipping()

        else:
            logger.error(SITE,self.taskID,'Failed to set guest checkout')
            time.sleep(int(self.task["DELAY"]))
            self.guestCheckout()
    
    def shipping(self):
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()

        logger.prepare(SITE,self.taskID,'Setting shipping...')
        try:
            bagId = self.bagResponse['bagId']
            payload = {
                "shippingAddress":{
                    "firstName":profile['firstName'],
                    "lastName":profile['lastName'],
                    "country":{
                        "name":self.countryName,
                        "id":self.countryId
                    },
                    "addressLine1":profile['house'],
                    "addressLine2":profile['addressOne'],
                    "addressLine3":profile['addressTwo'],
                    "city":{
                        "name":profile['city']
                    },
                    "state":{
                        "name":profile['region']
                    },
                    "zipCode":profile['zip'],
                    "phone":profile['phone']
                },
                "billingAddress":{
                    "firstName":profile['firstName'],
                    "lastName":profile['lastName'],
                    "country":{
                        "name":self.countryName,
                        "id":self.countryId
                    },
                    "addressLine1":profile['house'],
                    "addressLine2":profile['addressOne'],
                    "addressLine3":profile['addressTwo'],
                    "city":{
                        "name":profile['city']
                    },
                    "state":{
                        "name":profile['region']
                    },
                    "zipCode":profile['zip'],
                    "phone":profile['phone']
                }
            }
            response = self.session.patch(f'https://www.ambushdesign.com/api/checkout/v1/orders/{self.id}',json=payload, headers={
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US',
                'referer': 'https://www.ambushdesign.com/',
                'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'content-type': 'application/json',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
                'ff-country': self.countryCode.upper(),
                'ff-currency': self.currency
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.shipping()

        if response.status_code == 200:
            try:
                response.json()
                self.shippingMethod_ = response.json()['shippingOptions'][0]
            except:
                logger.error(SITE,self.taskID,'Failed to set shipping')
                time.sleep(int(self.task["DELAY"]))
                self.shipping()

            logger.warning(SITE,self.taskID,'Set shipping')
            self.shippingMethod()
        
        else:
            logger.error(SITE,self.taskID,'Failed to set shipping')
            time.sleep(int(self.task["DELAY"]))
            self.shipping()

    
    def shippingMethod(self):
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()

        logger.prepare(SITE,self.taskID,'Setting shipping method...')
        try:
            bagId = self.bagResponse['bagId']
            payload = {
                "shippingOption":{
                    "discount":self.shippingMethod_['discount'],
                    "merchants":self.shippingMethod_['merchants'],
                    "price":self.shippingMethod_['price'],
                    "formattedPrice":self.shippingMethod_['formattedPrice'],
                    "shippingCostType":self.shippingMethod_['shippingCostType'],
                    "shippingService":{
                        "description":self.shippingMethod_['shippingService']['description'],
                        "id":self.shippingMethod_['shippingService']['id'],
                        "name":self.shippingMethod_['shippingService']['name'],
                        "type":self.shippingMethod_['shippingService']['type'],
                        "minEstimatedDeliveryHour":self.shippingMethod_['shippingService']['minEstimatedDeliveryHour'],
                        "maxEstimatedDeliveryHour":self.shippingMethod_['shippingService']['maxEstimatedDeliveryHour'],
                        "trackingCodes":self.shippingMethod_['shippingService']['trackingCodes']
                    },
                    "shippingWithoutCapped":self.shippingMethod_['shippingWithoutCapped'],
                    "baseFlatRate":self.shippingMethod_['baseFlatRate']
                }
            }
            response = self.session.patch(f'https://www.ambushdesign.com/api/checkout/v1/orders/{self.id}',json=payload, headers={
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US',
                'referer': 'https://www.ambushdesign.com/',
                'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'content-type': 'application/json',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
                'ff-country': self.countryCode.upper(),
                'ff-currency': self.currency
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.shipping()

        if response.status_code == 200:
            try:
                response.json()
                self.grandTotal = response.json()['checkoutOrder']['grandTotal']
            except:
                logger.error(SITE,self.taskID,'Failed to set shipping method')
                time.sleep(int(self.task["DELAY"]))
                self.shipping()

            logger.warning(SITE,self.taskID,'Set shipping method')
            self.submitBilling()

        
        else:
            logger.error(SITE,self.taskID,'Failed to set shipping method')
            time.sleep(int(self.task["DELAY"]))
            self.shipping()

    
    def submitBilling(self):
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()

        try:

            payload = {
                "billingAddress": {
                    "city": { "countryId": self.countryId, "id": 0, "name": profile['city'] },
                    "country": self.countryData,
                    "lastName": profile['lastName'],
                    "state": { "countryId": 0, "id": 0, "code": profile['region'], "name": profile['region'] },
                    "userId": 0,
                    "isDefaultBillingAddress": False,
                    "isDefaultShippingAddress": False,
                    "addressLine1":profile['house'],
                    "addressLine2":profile['addressOne'] + ' ' + profile['addressTwo'],
                    "firstName":profile['firstName'],
                    "phone":profile['phone'],
                    "zipCode":profile['zip']
                }
            }


            response = self.session.patch(f'https://www.ambushdesign.com/api/checkout/v1/orders/{self.id}',json=payload, headers={
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US',
                'referer': 'https://www.ambushdesign.com/',
                'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'content-type': 'application/json',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
                'ff-country': self.countryCode.upper(),
                'ff-currency': self.currency
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.submitBilling()

        if response.status_code == 200:
            try:
                response.json()
                self.paymentIntentId = response.json()['checkoutOrder']['paymentIntentId']
            except:
                logger.error(SITE,self.taskID,'Failed to submit payment intent')
                time.sleep(int(self.task["DELAY"]))
                self.submitBilling()

            self.paypal()
        else:
            logger.error(SITE,self.taskID,'Failed to submit payment intent')
            time.sleep(int(self.task["DELAY"]))
            self.submitBilling()



    def paypal(self):
        logger.prepare(SITE,self.taskID,'Getting checkout link...')
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()

        try:
            bagId = self.bagResponse['bagId']
            payload = {
                "method":"PayPal",
                "option":"PayPalExp",
                "createToken":False,
                "payer":{
                    "id":json.loads(unquote(unquote(self.session.cookies['ctx'])))['u'],
                    "firstName":profile['firstName'],
                    "lastName":profile['lastName'],
                    "email":profile['email']
                    ,"birthDate":None,
                    "address":{
                        "city":{
                            "countryId":self.countryId,
                            "id":0,
                            "name":profile['city']
                        },
                        "country":self.countryData,
                        "id":"00000000-0000-0000-0000-000000000000",
                        "lastName":profile['lastName'],
                        "state":{
                            "countryId":0,
                            "id":0,
                            "code":profile['region'],
                            "name":profile['region']
                        },
                        "userId":0,
                        "isDefaultBillingAddress":False,
                        "isDefaultShippingAddress":False,
                        "addressLine1":profile['house'],
                        "addressLine2":profile['addressOne'] + ' ' + profile['addressTwo'],
                        "firstName":profile['firstName'],
                        "phone":profile['phone'],
                        "zipCode":profile['zip']
                    }
                },
                "amounts":[{"value":int(self.grandTotal)}],
                "data":{}
            }

            response = self.session.post(f'https://www.ambushdesign.com/api/payment/v1/intents/{self.paymentIntentId}/instruments',json=payload, headers={
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US',
                'referer': 'https://www.ambushdesign.com/',
                'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'content-type': 'application/json',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
                'ff-country': self.countryCode.upper(),
                'ff-currency': self.currency
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.paypal()

        
        response = self.session.post(f'https://www.ambushdesign.com/api/checkout/v1/orders/{self.id}/charges',json={"cancelUrl":f"https://www.ambushdesign.com/{self.urlRegion}/commerce/checkout","returnUrl":f"https://www.ambushdesign.com/{self.urlRegion}/checkoutdetails?orderid={self.id}"},headers={
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US',
            'referer': 'https://www.ambushdesign.com/',
            'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
            'ff-country': self.countryCode.upper(),
            'ff-currency': self.currency
        })
        if response.status_code == 200 or response.status_code == 201:
            self.end = time.time() - self.start
            try:
                response.json()
                redirectUrl = response.json()['redirectUrl']
            except:
                logger.error(SITE,self.taskID,'Failed to get checkout link')
                time.sleep(int(self.task["DELAY"]))
                self.paypal()

            updateConsoleTitle(False,True,SITE)
            logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')

            url = storeCookies(redirectUrl,self.session,self.productTitle,self.productImage,self.productPrice)
            
            sendNotification(SITE,self.productTitle)
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
                    speed=self.end
                )
                while True:
                    pass
            except:
                logger.secondary(SITE,self.taskID,'Failed to send webhook. Checkout here ==> {}'.format(url))

        else:
            logger.error(SITE,self.taskID,'Failed to get checkout link')
            time.sleep(int(self.task["DELAY"]))
            self.paypal()
