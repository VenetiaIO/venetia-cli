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
# import cloudscraper
from utils.cloudscraper import cloudscraper

import string

from utils.logger import logger
from utils.webhook import discord
from utils.log import log
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies)
SITE = 'NAKED'



class NAKED:
    def __init__(self, task,taskName):
        self.task = task
        self.sess = requests.session()
        self.taskID = taskName

        twoCap = loadSettings()["2Captcha"]
        self.session = cloudscraper.create_scraper(
            requestPostHook=injection,
            sess=self.sess,
            interpreter='nodejs',
            delay=5,
            browser={
                'browser': 'chrome',
                'mobile': False,
                'platform': 'windows'
                #'platform': 'darwin'
            },
            captcha={
                'provider': '2captcha',
                'api_key': twoCap
            }
        )
        
        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)

        self.collect()

    def collect(self):
        logger.warning(SITE,self.taskID,'Solving Cloudflare...')
        try:
            retrieve = self.session.get(self.task["PRODUCT"])
            logger.success(SITE,self.taskID,'Solved Cloudflare')
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.collect()

        if retrieve.status_code == 200:
            self.start = time.time()
            logger.success(SITE,self.taskID,'Got product page')
            try:
                soup = BeautifulSoup(retrieve.text, "html.parser")
                self.antiCsrf = self.session.cookies["AntiCsrfToken"]
    
                foundSizes = soup.find('select',{'id':'product-form-select'})
                if foundSizes:
                    sizes = []
                    allSizes = []
                    for s in foundSizes:
                        try:
                            if s["value"] == "-1":
                                pass
                            else:
                                sizes.append(s.text.strip())
                                allSizes.append('{}:{}'.format(s.text.strip(),s["value"]))
                        except:
                            pass
    
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
                                if size.split(':')[0] == self.task["SIZE"]:
                                    self.size = size.split(':')[0]
                                    self.sizeId = size.split(':')[1]
                                    logger.success(SITE,self.taskID,f'Found Size => {self.size}')
        
                    
                    elif self.task["SIZE"].lower() == "random":
                        chosen = random.choice(allSizes)
                        self.size = chosen.split(':')[0]
                        self.sizeId = chosen.split(':')[1]
                        logger.success(SITE,self.taskID,f'Found Size => {self.size}')
                
                else:
                    logger.error(SITE,self.taskID,'Size Not Found')
                    time.sleep(int(self.task["DELAY"]))
                    self.collect()
        
            except Exception as e:
               log.info(e)
               logger.error(SITE,self.taskID,'Failed to scrape page (Most likely out of stock). Retrying...')
               time.sleep(int(self.task["DELAY"]))
               self.collect()


            self.addToCart()
        
        if retrieve.status_code == 403:
            logger.error(SITE,self.taskID,f'Failed to get product page => 403. Retrying...')
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.collect()

        else:
            try:
                status = retrieve.status_code
            except:
                status = 'Unknown'
            logger.error(SITE,self.taskID,f'Failed to get product page => {status}. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.collect()

    def addToCart(self):
        logger.prepare(SITE,self.taskID,'Carting Product...')
        payload = {
            '_AntiCsrfToken': self.antiCsrf,
            'id': self.sizeId,
            'partial': 'ajax-cart',
        }

        try:
            postCart = self.session.post('https://www.nakedcph.com/en/cart/add', data=payload, headers={
                'authority': 'www.nakedcph.com',
                'accept-language': 'en-US,en;q=0.9',
                'accept': '*/*',
                'origin': 'https://www.nakedcph.com',
                'referer': self.task["PRODUCT"],
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
                'x-anticsrftoken':self.antiCsrf
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()
    


        if postCart:
            if postCart.status_code == 200:
                logger.success(SITE,self.taskID,'Successfully carted')
                self.shipping()
            else:
                logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                if self.task["SIZE"].lower() == "random":
                    self.collect()
                else:
                    self.addToCart()
        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            if self.task["SIZE"].lower() == "random":
                self.collect()
            else:
                self.addToCart()

    def shipping(self):
        profile = loadProfile(self.task["PROFILE"])
        countryCode = profile["countryCode"]

        params = {
            'partial': 'shipping-quotes',
            'zip': profile["zip"],
            'countryCode': countryCode,
            'skip_layout': '1'
        }
        try:
            shippingQuote = self.session.post('https://www.nakedcph.com/en/webshipr/render', params=params, headers={
                'authority': 'www.nakedcph.com',
                'accept-language': 'en-US,en;q=0.9',
                'accept': '*/*',
                'origin': 'https://www.nakedcph.com',
                'referer': 'https://www.nakedcph.com/en/cart/view',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
                'x-anticsrftoken':self.antiCsrf
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.shipping()

        if shippingQuote.status_code == 200:
            soup = BeautifulSoup(shippingQuote.text,"html.parser")
            method = soup.find('div',{'class':'shipping-quotes has-selected-quote'})
            self.methodId = method.find('div',{'class':'shipping-quote is-selected'})["data-quote-id"]
            self.method = method.find('input',{'name':'webshiprQuoteMethod'})["value"]
            
            params = {
                'id': self.methodId,
                'zip': profile["zip"],
                'partial': 'shipping-quotes',
                'skip_layout': '1'
            }
            print(params)
            try:
                shippingQuote = self.session.post('https://www.nakedcph.com/en/webshipr/setshippingquote', params=params, headers={
                    'authority': 'www.nakedcph.com',
                    'accept-language': 'en-US,en;q=0.9',
                    'origin': 'https://www.nakedcph.com',
                    'accept': '*/*',
                    'referer': 'https://www.nakedcph.com/en/cart/view',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                    'x-anticsrftoken':self.antiCsrf
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.shipping()

            if shippingQuote.status_code == 200:
                logger.success(SITE,self.taskID,'Successfully saved shipping details')
                self.payment()
            else:
                logger.error(SITE,self.taskID,'Failed to save shipping details.Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.shipping()
        
        else:
            logger.error(SITE,self.taskID,'Failed to save shipping details.Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.shipping()


    
    def payment(self):

        try:
            paymentMethod = self.session.post('https://www.nakedcph.com/en/cart/setpaymentmethod', data={'id': '5', 'partial': 'ajax-cart'}, headers={
                'authority': 'www.nakedcph.com',
                'accept-language': 'en-US,en;q=0.9',
                'accept': '*/*',
                'origin': 'https://www.nakedcph.com',
                'referer': 'https://www.nakedcph.com/en/cart/view',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
                'x-anticsrftoken':self.antiCsrf
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.shipping()

        if paymentMethod.status_code == 200:
            logger.success(SITE,self.taskID,'Successfully saved payment details')
            self.process()
        else:
            logger.error(SITE,self.taskID,'Failed to save payment details.Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.shipping()

    def process(self):
        profile = loadProfile(self.task["PROFILE"])
        payload = {
            '_AntiCsrfToken': self.antiCsrf,
            'country': profile["countryCode"],
            'postalCodeQuery': profile["zip"],
            'firstName': profile["firstName"],
            'lastName': profile["lastName"],
            'addressLine2': profile["house"] + " " + profile["addressOne"],
            'postalCode': profile["zip"],
            'city': profile["city"],
            'phoneNumber': profile["phone"],
            'toggle-billing-address': 'on',
            'billingProvince': '-1',
            'billingProvince': '-1',
            'webshiprQuoteMethod': self.method,
            'txvariant': 'card',
            'termsAccepted': True
        }
        print(payload)
        try:
            processP = self.session.post('https://www.nakedcph.com/en/cart/process', data=payload, headers={
                'authority': 'www.nakedcph.com',
                'accept-language': 'en-US,en;q=0.9',
                'origin': 'https://www.nakedcph.com',
                'referer': 'https://www.nakedcph.com/en/cart/view',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.shipping()

        print(processP.headers)
        print(processP.url)
        
        processPaymentResponse = {
            "Response":{
                "Items":[
                    {
                        "Id":2495,
                        "Description":"315115 112 - Nike Sportswear - Air Force 1 '07 37,5",
                        "IsDiscounted":False,
                        "IsOnSale":False,
                        "OriginalPrice":{
                            "ExclVAT":87.5,
                            "InclVAT":105.0,
                            "VATTotal":17.5,
                            "VATRate":20.0
                        },
                        "Price":"105 EUR",
                        "UnitsAvailable":1,
                        "Quantity":1,
                        "SubTotal":{
                            "ExclVAT":87.50000,
                            "InclVAT":105.00000,
                            "VATTotal":17.50000,
                            "VATRate":20.0
                        },
                        "SubTotalVAT":17.50000,
                        "VATRate":20.0
                    }
                ],
                "TotalProductCost":"105 EUR",
                "TotalPaymentFee":"0 EUR",
                "TotalShippingCost":"10 EUR",
                "TotalDesiredAmount":"115 EUR",
                "TotalFormatted":{
                    "InclVAT":"105 EUR",
                    "ExclVAT":"88 EUR"
                }
            },
            "StatusCode":0,
            "Status":"OK"
        }


    def paypal(self):
        pass
        # displayGroup: paypal
        # pay: pay
        # sig: PMEpaNX77xg/s7arIhx3skTdGnE=
        # merchantReference: 1106685
        # brandCode: paypal
        # paymentAmount: 11500
        # currencyCode: EUR
        # shipBeforeDate: 2020-09-21T21:33:03Z
        # skinCode: SfaF16TW
        # merchantAccount: NakedCOM
        # shopperLocale: en
        # stage: pay
        # sessionId: EEUbpMyKsz3HVa57tOvgWzhay/w=
        # orderData: H4sIAAAAAAAEAK2QMQvCMBCFd8H/cGRxKjaW6lIDDjo6WPwBaXPoYW3iJSL996ZSwcEOgtt3994dj1cEXTUIdaO9XwvLBjmhgFcv1HQCUITKmu6F/cAD9WzeRwZ9zeQC2VaoTOZS5iDlAhLY0wWhdJaDf6DmuNkQw85yjSBhlq4gWxbzYL59vd11Gyh0Qskxi2OqMeppDtvj4cMVkX/IXJ7JOWpP/4gyliTC0GSkvnL1BKi47rZ6AQAA
        # sessionValidity: 2020-09-14T21:43:03Z
        # countryCode: GB
        # shopperEmail: charliebottomley15@gmail.com
        # shopperReference: 5590317
        # merchantOrderReference: 736186
        # resURL: https://www.nakedcph.com/adyen/return
        # allowedMethods: paypal
        # originalSession: H4sIAAAAAAAAAIVVXXOiShD9Kyle767yJYZUbdUVMWr8QEVDYvkywgCjA0OGUYK37n+/M0F3iW7u+th9+ni6+/Twj4RSxFwGIig9SBkopW8ShSGkFNLVYsxjMWNZ/rBpbppFUTRSsIeBn8UNnySbJkw3TR9QtmkeESx4aR6TLIN0THyABSFMP/jyP1OBoBRsFLIDFUU+OaSMll0SCJ6+xUNcXQJT1klESnpQlJYsc+CBa039C7K3WnzoQJkFQ0KhDZgIq7Iqf5fN76qyVJUHTXuQtTXHJZD6MUjZQrTMWQRUUWTDuG8Jlj1Kz7RuCB4VY+nVajq+XwmRpqKTrjPhSUIDSPl/Ah4e6PmwU/16nZE6n8yP3YnVfQzuB3xs/cX7aAc8Aw9te0cMb1ZY4GVGXj0NPblj0zTWbuH3nIgxzTT1YKf4vZflahgAx3wpjmNrl8TRo39UBvPuargcJQfjkbN2bNM7wUWxNk9w3lWfAVk6a7eFbNyJx69y4cXBE7BDw04O0/28uG+VO9eK8Zseee/b0+u4ZR4DRemXsTzP9+9Idd4mMMtsdtzp/uR5/7JpDl+e2k+Ol802TT0qMVp25b67P6ZjxRohvU3XRmfe6YjpwTxHJH0GGAWIlbUlKLpYgn5Zwtk0vQQgzFF8uBQjuCWMkQTDUmn9HYmU8MkvdH1jrZYpa0q7thtHrKEOaWuGcm98mFEYBqVRl3B/AZ/vLz1g/E0CGJMCBhPIYhLk1TFkAPOSLSb+vpap8Gcd/HQYFLa8xH9ZSji5skKVIWGYw5+4nHF3XpENUwaFJj62S2aLMOZqO0HAzyhflpnohosKIEZHSMtPiU9k9RAfXQbSsh76TNzIGYVCnKSodzOEEy7ubgKLXLpBxuSQw+kh2ULq0ClIzoJu+PhcHDqj5IiqFdxiMsJR+Hxh9li9U635LcqvzDM40IJQFv8GUD0Vl2fiajL/19k19IvWbhl/09s16IvmrmG33d0gPrd33m4jRDRnZ43d6mRqWZSG6P3KEA0MflZYl+uq1UQw5VfDk6vpaOp401oqEA2HFuIKbVA64YQfT3xNXwP9Kf8KAb1OM4hhFpP0vACuQ263TUPVNFNu1bTkxEcAu+KO+ewu4IqLonzP/wY0LkOsjpZzzUAKIkJBw+Wfhoy752N7vN+GB7fic0Frz4e4w4gCcYeNHEXi6XLelicU6WvNX+5naDEfPca63d80jb+iH19UsupYB7OZVFNW8Y1mk7BVvMYD6EaHJL1XrT6ea7IevZM6nfsB7vVW22xSjvKTNngGrTZzjpF3ikHJP6Q/pH//AxYTDVnEBwAA
        # billingAddress.street: 12 Pilmore Mews
        # billingAddress.houseNumberOrName: 
        # billingAddress.city: Hurworth
        # billingAddress.postalCode: DL2 2BQ
        # billingAddress.stateOrProvince: 
        # billingAddress.country: GB
        # billingAddressType: 
        # deliveryAddress.street: 12 Pilmore Mews
        # deliveryAddress.houseNumberOrName: 
        # deliveryAddress.city: Hurworth
        # deliveryAddress.postalCode: DL2 2BQ
        # deliveryAddress.stateOrProvince: 
        # deliveryAddress.country: GB
        # shopper.firstName: Charlie
        # shopper.lastName: Bottomley
        # shopper.gender: UNKNOWN
        # shopper.telephoneNumber: 07796233905
        # riskdata.deliveryMethod: Panagora.ShippingProvider.Webshipr
        # merchantIntegration.sig: 2OqTzig4Z3cTkPiRQKFh4DG/6+g=
        # merchantIntegration.type: HPP
        # riskdata.sig: KPMf5wYhHeSgumn82BGlQ304gxo=
        # referrerURL: https://www.nakedcph.com/en/cart/view
        # dfValue: ryEGX8eZpJ0030000000000000BTWDfYZVR30089146776cVB94iKzBGQkPFutk01m5S16Goh5Mk0045zgp4q8JSa00000qZkTE00000PRbZ1HbvOQG2etdcqzfW:40
        # usingFrame: false
        # usingPopUp: false
        # 
        # 

        


