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
import urllib.parse
import string
from urllib3.exceptions import HTTPError
import csv


from utils.logger import logger
from utils.webhook import discord
from utils.log import log
from utils.captcha import captcha
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies, updateConsoleTitle, scraper)
SITE = 'NAKED'



class NAKED:
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
        self.sess = requests.session()
        self.taskID = taskName
        self.rowNumber = rowNumber

        try:
            self.session = scraper()
        except Exception as e:
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.__init__(task,taskName)
        
        self.captchaRequired = False
        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
        threading.Thread(target=self.task_checker,daemon=True).start()
        if self.task["ACCOUNT EMAIL"] == "":
            self.collect()
        else:
            self.login()
        

    def login(self):
        logger.prepare(SITE,self.taskID,'Logging In...')

        try:
            loginPage = self.session.get('https://www.nakedcph.com/en/auth/submit',headers={
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9,it;q=0.8',
                'Referer': 'https://www.nakedcph.com/en/auth/view',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.login()

        soup = BeautifulSoup(loginPage.text, "html.parser")
        self.antiCsrf = self.session.cookies["AntiCsrfToken"]

        captchaResponse = loadToken(SITE)
        if captchaResponse == "empty":
            captchaResponse = captcha.v2('6LeNqBUUAAAAAFbhC-CS22rwzkZjr_g4vMmqD_qo',self.task["PRODUCT"],self.session.proxies,SITE,self.taskID)

        
        payload = {
            '_AntiCsrfToken': self.antiCsrf,
            'email': self.task["ACCOUNT EMAIL"],
            'password': self.task["ACCOUNT PASSWORD"],
            'g-recaptcha-response':captchaResponse,
            'action':'login'
        }


        try:
            login = self.session.post('https://www.nakedcph.com/en/auth/submit', data=payload,headers={
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9,it;q=0.8',
                'Referer': 'https://www.nakedcph.com/en/auth/view',
                'X-Requested-With': 'XMLHttpRequest'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.login()

        # self.session.debugRequest(login)


        if login.status_code == 200 and login.json()["Response"]["Success"] == True:
            logger.warning(SITE,self.taskID,'Successfully logged in')
            self.collect()
        else:
            logger.error(SITE,self.taskID,'Failed to login. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.login()

    def collect(self):
        logger.prepare(SITE,self.taskID,'Getting product page...')
        try:
            retrieve = self.session.get(self.task["PRODUCT"])
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
                self.antiCsrf = self.session.cookies["AntiCsrfToken"]
                self.productTitle = soup.find('title').text
                self.productPrice = soup.find('meta',{'property':'og:price'})["content"]
                self.productImage = 'https://www.nakedcph.com/' + soup.find_all('img',{'class':'lazyload'})[0]['data-href']
    
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
                                    logger.warning(SITE,self.taskID,f'Found Size => {self.size}')
        
                    
                    elif self.task["SIZE"].lower() == "random":
                        chosen = random.choice(allSizes)
                        self.size = chosen.split(':')[0]
                        self.sizeId = chosen.split(':')[1]
                        logger.warning(SITE,self.taskID,f'Found Size => {self.size}')
                
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


        elif retrieve.status_code != 200:
            try:
                status = retrieve.status_code
            except:
                status = 'Unknown'
            logger.error(SITE,self.taskID,f'Failed to get product page => {status}. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.collect()



    def addToCart(self):

        payload = {
            '_AntiCsrfToken': self.antiCsrf,
            'id': self.sizeId,
            'partial': 'ajax-cart',
        }

        if self.captchaRequired == True:
            captchaResponse = loadToken(SITE)
            if captchaResponse == "empty":
                captchaResponse = captcha.v2('6LeNqBUUAAAAAFbhC-CS22rwzkZjr_g4vMmqD_qo',self.task["PRODUCT"],self.session.proxies,SITE,self.taskID)
            
            payload['g-recaptcha-response'] = captchaResponse
        
        logger.prepare(SITE,self.taskID,'Carting Product...')


        try:
            postCart = self.session.post('https://www.nakedcph.com/en/cart/add', data=payload, headers={
                'accept': '*/*',
                'referer': self.task["PRODUCT"],
                'x-requested-with': 'XMLHttpRequest',
                'x-anticsrftoken':self.antiCsrf,
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()
    


        if postCart.status_code == 200:
            updateConsoleTitle(True,False,SITE)
            logger.warning(SITE,self.taskID,'Successfully carted')
            self.shipping()
        else:
            if 'ReCaptchaFailed' in postCart.text:
                logger.error(SITE,self.taskID,'Failed to cart (Captcha Required). Retrying...')
                self.captchaRequired = True
            else:
                logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
                self.captchaRequired = False
            time.sleep(int(self.task["DELAY"]))
            if self.task["SIZE"].lower() == "random":
                self.collect()
            else:
                self.addToCart()


    def shipping(self):
        
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        countryCode = profile["countryCode"]

        logger.prepare(SITE,self.taskID,'Submitting shipping...')
        params = {
            'partial': 'shipping-quotes',
            'zip': profile["zip"],
            'countryCode': countryCode,
            'skip_layout': '1'
        }
        try:
            shippingQuote = self.session.post('https://www.nakedcph.com/en/webshipr/render', params=params, headers={
                'accept': '*/*',
                'referer': 'https://www.nakedcph.com/en/cart/view',
                'x-requested-with': 'XMLHttpRequest',
                'x-anticsrftoken':self.antiCsrf,
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
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
            try:
                shippingQuote = self.session.post('https://www.nakedcph.com/en/webshipr/setshippingquote', params=params, headers={
                    'accept': '*/*',
                    'referer': 'https://www.nakedcph.com/en/cart/view',
                    'x-requested-with': 'XMLHttpRequest',
                    'x-anticsrftoken':self.antiCsrf,
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.shipping()

            if shippingQuote.status_code == 200:
                logger.warning(SITE,self.taskID,'Successfully saved shipping details')
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
        logger.prepare(SITE,self.taskID,'Setting payment details...')

        try:
            paymentMethod = self.session.post('https://www.nakedcph.com/en/cart/setpaymentmethod', data={'id': '5', 'partial': 'ajax-cart'}, headers={
                'accept': '*/*',
                'referer': 'https://www.nakedcph.com/en/cart/view',
                'x-requested-with': 'XMLHttpRequest',
                'x-anticsrftoken':self.antiCsrf,
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.payment()

        if paymentMethod.status_code == 200:
            logger.warning(SITE,self.taskID,'Successfully saved payment details')
            self.process()
        else:
            logger.error(SITE,self.taskID,'Failed to save payment details.Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.shipping()

    def process(self):
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        logger.prepare(SITE,self.taskID,'Getting checkout data...')
        payload = {
            '_AntiCsrfToken': self.antiCsrf,
            'country': profile["countryCode"],
            'emailAddress':profile["email"],
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
            'termsAccepted': 'true'
        }
        try:
            processP = self.session.post('https://www.nakedcph.com/en/cart/process', data=payload, headers={
                'referer': 'https://www.nakedcph.com/en/cart/view',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'content-type': 'application/x-www-form-urlencoded',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.process()


        if 'paypal' in processP.url:
            logger.warning(SITE,self.taskID,'Got paypal link')
            self.ppUrl = processP.url
            self.end = time.time() - self.start
            self.sendPaypal()
        elif 'adyen' in processP.url:
            try:
                adyen = self.session.get(processP.url,headers={
                    'Referer': 'https://www.nakedcph.com/en/cart/view',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.process()
            
            if adyen.status_code == 200:
                soup = BeautifulSoup(adyen.text,"html.parser")
                self.originalSession = soup.find('input',{'name':'originalSession'})['value']
                self.merchantIntegrationSig = soup.find('input',{'name':'merchantIntegration.sig'})['value']
                self.merchantIntegrationType = soup.find('input',{'name':'merchantIntegration.type'})['value']
                self.sig = soup.find('input',{'name':'sig'})['value']

                
                def decodeURIComponent(str):
                    decoded = urllib.parse.unquote(str)
                    return decoded

                url = processP.url
                self.referer = url
                self.paymentAmount = decodeURIComponent(url.split('?paymentAmount=')[1].split('&')[0])
                self.currencyCode = decodeURIComponent(url.split('currencyCode=')[1].split('&')[0])
                self.skinCode = decodeURIComponent(url.split('skinCode=')[1].split('&')[0])
                self.merchantRef = decodeURIComponent(url.split('merchantReference=')[1].split('&')[0])
                self.shopperIP = decodeURIComponent(url.split('shopperIP=')[1].split('&')[0])
                self.shopperReference = decodeURIComponent(url.split('shopperReference=')[1].split('&')[0])
                self.shopperEmail = decodeURIComponent(url.split('shopperEmail=')[1].split('&')[0])
                self.merchantAccount = decodeURIComponent(url.split('merchantAccount=')[1].split('&')[0])
                self.sessionValidity = decodeURIComponent(url.split('sessionValidity=')[1].split('&')[0])
                self.shipBeforeDate = decodeURIComponent(url.split('shipBeforeDate=')[1].split('&')[0])
                self.allowedMethods = decodeURIComponent(url.split('allowedMethods=')[1].split('&')[0])
                self.resURL = decodeURIComponent(url.split('resURL=')[1].split('&')[0])
                self.countryCode = decodeURIComponent(url.split('countryCode=')[1].split('&')[0])
                self.merchantOrderReference = decodeURIComponent(url.split('merchantOrderReference=')[1].split('&')[0])
                self.shopperFname = decodeURIComponent(url.split('shopper.firstName=')[1].split('&')[0])
                self.shopperLname = decodeURIComponent(url.split('shopper.lastName=')[1].split('&')[0])
                self.shopperGender = decodeURIComponent(url.split('shopper.gender=')[1].split('&')[0])
                self.shopperPhone = decodeURIComponent(url.split('shopper.telephoneNumber=')[1].split('&')[0])
                self.riskDataMethod = decodeURIComponent(url.split('riskdata.deliveryMethod=')[1].split('&')[0])
                self.billingAddressType = decodeURIComponent(url.split('billingAddressType=')[1].split('&')[0])
                self.shopperLocale = decodeURIComponent(url.split('shopperLocale=')[1].split('&')[0])
                self.orderData = decodeURIComponent(url.split('orderData=')[1].split('&')[0])
                self.billingStreet = decodeURIComponent(url.split('billingAddress.street=')[1].split('&')[0])
                self.billingHouse = decodeURIComponent(url.split('billingAddress.houseNumberOrName=')[1].split('&')[0])
                self.billingCity = decodeURIComponent(url.split('billingAddress.city=')[1].split('&')[0])
                self.billingZIP = decodeURIComponent(url.split('billingAddress.postalCode=')[1].split('&')[0])
                self.billingState = decodeURIComponent(url.split('billingAddress.stateOrProvince=')[1].split('&')[0])
                self.billingCountry = decodeURIComponent(url.split('billingAddress.country=')[1].split('&')[0])
                self.billingAddressSig = decodeURIComponent(url.split('billingAddressSig=')[1].split('&')[0])
                self.deliveryStreet = decodeURIComponent(url.split('deliveryAddress.street=')[1].split('&')[0])
                self.deliveryHouse = decodeURIComponent(url.split('deliveryAddress.houseNumberOrName=')[1].split('&')[0])
                self.deliveryCity = decodeURIComponent(url.split('deliveryAddress.city=')[1].split('&')[0])
                self.deliveryZIP = decodeURIComponent(url.split('deliveryAddress.postalCode=')[1].split('&')[0])
                self.deliveryState = decodeURIComponent(url.split('deliveryAddress.stateOrProvince=')[1].split('&')[0])
                self.deliveryCountry = decodeURIComponent(url.split('deliveryAddress.country=')[1].split('&')[0])
                self.deliveryAddressSig = decodeURIComponent(url.split('deliveryAddressSig=')[1].split('&')[0])
                self.merchantSig = decodeURIComponent(url.split('merchantSig=')[1].split('&')[0])
                self.shopperSig = decodeURIComponent(url.split('shopperSig=')[1].split('&')[0])
                self.riskDataSig = decodeURIComponent(url.split('riskdata.sig=')[1].split('&')[0])
                logger.warning(SITE,self.taskID,'Successfully got checkout data')
                self.paypal()
        
        else:
            logger.error(SITE,self.taskID,'Failed to get checkout data. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.process()
                
            

    def paypal(self):
        logger.prepare(SITE,self.taskID,'Getting paypal link...')
        adyenForm = {
            'displayGroup': 'paypal',
            'pay': 'pay',
            'sig': self.sig,
            'merchantReference': self.merchantRef,
            'brandCode': 'paypal',
            'paymentAmount': self.paymentAmount,
            'currencyCode': self.currencyCode,
            'shipBeforeDate': self.shipBeforeDate,
            'skinCode': self.skinCode,
            'merchantAccount': self.merchantAccount,
            'shopperLocale': self.shopperLocale,
            'stage': 'pay',
            'sessionId': self.merchantSig,
            'orderData': self.orderData,
            'sessionValidity': self.sessionValidity,
            'countryCode': self.countryCode,
            'shopperEmail': self.shopperEmail,
            'shopperReference': self.shopperReference,
            'merchantOrderReference': self.merchantOrderReference,
            'resURL': self.resURL,
            'allowedMethods': self.allowedMethods,
            'originalSession': self.originalSession,
            'billingAddress.street': self.billingStreet,
            'billingAddress.houseNumberOrName': self.billingHouse,
            'billingAddress.city': self.billingCity,
            'billingAddress.postalCode': self.billingZIP,
            'billingAddress.stateOrProvince': self.billingState,
            'billingAddress.country': self.billingCountry,
            'billingAddressType': self.billingAddressType,
            'deliveryAddress.street': self.deliveryStreet,
            'deliveryAddress.houseNumberOrName': self.deliveryHouse,
            'deliveryAddress.city': self.deliveryCity,
            'deliveryAddress.postalCode': self.deliveryZIP,
            'deliveryAddress.stateOrProvince': self.deliveryState,
            'deliveryAddress.country': self.deliveryCountry,
            'shopper.firstName': self.shopperFname,
            'shopper.lastName': self.shopperLname,
            'shopper.gender': self.shopperGender,
            'shopper.telephoneNumber': self.shopperPhone,
            'riskdata.deliveryMethod': self.riskDataMethod,
            'merchantIntegration.sig': self.merchantIntegrationSig,
            'merchantIntegration.type': self.merchantIntegrationType,
            'riskdata.sig': self.riskDataSig,
            'referrerURL': 'https://www.nakedcph.com/en/cart/view',
            'dfValue': 'ryEGX8eZpJ0030000000000000BTWDfYZVR30089146776cVB94iKzBGzk6emGsPvH5S16Goh5Mk0045zgp4q8JSa00000qZkTE00000PRbZ1HbvOQG2etdcqzfW:40',
            'usingFrame': False,
            'usingPopUp': False,
            'shopperBehaviorLog': ''
        }
        
        try:
            getPaypal = self.session.post('https://live.adyen.com/hpp/redirectPayPal.shtml', data=adyenForm, headers={
                'Referer': self.referer,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'content-type': 'application/x-www-form-urlencoded',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.paypal()


        if getPaypal.status_code in [200,302] and 'paypal' in getPaypal.url:
            logger.warning(SITE,self.taskID,'Got paypal link')
            self.end = time.time() - self.start
            self.ppUrl = getPaypal.url
            self.sendPaypal()

        else:
            logger.error(SITE,self.taskID,'Failed to get PayPal checkout. Retrying...')
            try:
                discord.failed(
                    webhook=loadSettings()["webhook"],
                    site=SITE,
                    url=self.task["PRODUCT"],
                    image=self.productImage,
                    title=self.productTitle,
                    size=self.size,
                    price=self.productPrice,
                    paymentMethod='PayPal',
                    profile=self.task["PROFILE"],
                    account=self.task["ACCOUNT EMAIL"],
                    proxy=self.session.proxies
                )
            except:
                pass
            time.sleep(int(self.task["DELAY"]))
            self.paypal()

    def sendPaypal(self):
        updateConsoleTitle(False,True,SITE)
        logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')
        url = storeCookies(self.ppUrl,self.session, self.productTitle, self.productImage, self.productPrice)
        
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
                account=self.task["ACCOUNT EMAIL"],
                speed=self.end
            )
            sendNotification(SITE,self.productTitle)
            while True:
                pass
        except Exception as e:
            log.info(e)
            logger.alert(SITE,self.taskID,'Failed to send webhook. Checkout here ==> {}'.format(url))



        


