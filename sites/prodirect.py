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

from utils.logger import logger
from utils.webhook import discord
from utils.log import log
from utils.captcha import captcha
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies)
SITE = 'PRO-DIRECT'

class PRODIRECT:
    def __init__(self, task,taskName):
        self.task = task
        self.session = requests.session()
        self.taskID = taskName

        twoCap = loadSettings()["2Captcha"]
        #self.session = cloudscraper.create_scraper(
        #    requestPostHook=injection,
        #    sess=self.sess,
        #    interpreter='nodejs',
        #    delay=5,
        #    browser={
        #        'browser': 'chrome',
        #        'mobile': False,
        #        'platform': 'windows'
        #        #'platform': 'darwin'
        #    },
        #    captcha={
        #        'provider': '2captcha',
        #        'api_key': twoCap
        #    }
        #)
        
        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)

        self.collect()

    def collect(self):
        #logger.warning(SITE,self.taskID,'Solving Cloudflare...')
        try:
            retrieve = self.session.get(self.task["PRODUCT"],headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
            })
            #logger.success(SITE,self.taskID,'Solved Cloudflare')
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
                self.productTitle = soup.find('title').text.replace('\n','')
                self.productPrice = soup.find('p',{'class':'price'}).text
                imgs = soup.find_all('img',{'class':'product mainImage'})
                self.productImage = 'https://www.prodirectbasketball.com/' + imgs[0]["src"]
    
                foundSizes = soup.find_all('option')
                if foundSizes:
                    sizes = []
                    for s in foundSizes:
                        try:
                            if s["value"] == "tab-1":
                                pass
                            if s["value"] == "tab-3":
                                pass
                            else:
                                if "½" in s["data-uksize"]:
                                    size = s["data-uksize"].split('½')[0]
                                    size = size + '.5'
                                else:
                                    size = s["data-uksize"]
                                sizes.append(size)
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
                            for size in sizes:
                                if size == self.task["SIZE"]:
                                    self.size = size
                                    logger.success(SITE,self.taskID,f'Found Size => {self.size}')
        
                    
                    elif self.task["SIZE"].lower() == "random":
                        chosen = random.choice(sizes)
                        self.size = chosen
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

        elif retrieve.status_code not in [200,403]:
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
            'sizeregion': 'UK',
            'size': self.size,
            'quantity': '1',
            'buynow': '1',
        }

        try:
            postCart = self.session.post(self.task["PRODUCT"], data=payload, headers={
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'referer': self.task["PRODUCT"],
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()

        if postCart.status_code == 200 and 'successfully' in postCart.text:
            logger.success(SITE,self.taskID,'Successfully carted')
            self.login()
        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            if self.task["SIZE"].lower() == "random":
                self.collect()
            else:
                self.addToCart()

    
    def login(self):
        logger.prepare(SITE,self.taskID,'Preparing login...')
        captchaResponse = loadToken(SITE)
        if captchaResponse == "empty":
            captchaResponse = captcha.v2('6LdXsbwUAAAAAMe1vJVElW1JpeizmksakCUkLL8g',self.task["PRODUCT"],self.session.proxies,SITE,self.taskID)
        
        payload = {
            'loginemail': self.task["ACCOUNT EMAIL"],
            'loginpassword': self.task["ACCOUNT PASSWORD"],
            'g-recaptcha-response':captchaResponse,
            '__EVENTTARGET':'LogIn'
        }

        try:
            login = self.session.post('https://www.prodirectbasketball.com/accounts/MyAccount.aspx?Return=Checkout', data=payload, headers={
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'referer': 'https://www.prodirectbasketball.com/accounts/MyAccount.aspx?Return=Checkout',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.login()

        if login.status_code in [200,302,301] and 'Checkout.aspx' in login.url:
            logger.success(SITE,self.taskID,'Successfully logged in')
            self.address()
        else:
            logger.error(SITE,self.taskID,'Failed to login. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.login()

    def address(self):
        profile = loadProfile(self.task["PROFILE"])
        logger.prepare(SITE,self.taskID,'Posting Address...')
        try:
            addy = self.session.get('https://www.prodirectbasketball.com/accounts/Checkout.aspx?ACC=ADDR',headers={
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'referer': 'https://www.prodirectbasketball.com/accounts/MyAccount.aspx?Return=Checkout',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.login()

        if addy.status_code == 200:
            soup = BeautifulSoup(addy.text,"html.parser")
            txtAddyID = soup.find('input',{'name':'txtAddressID'})['value']
        
        
        
        payload = {
            'myName': profile["firstName"] + " " + profile["lastName"],
            'txtAddressID': txtAddyID,
            'txtAddressID':txtAddyID,
            '__EVENTTARGET':'fw100$btnProceedPayment'
        }

        try:
            postAddy = self.session.post('https://www.prodirectbasketball.com/accounts/Checkout.aspx?ACC=ADDR', data=payload, headers={
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'referer': 'https://www.prodirectbasketball.com/accounts/Checkout.aspx?ACC=ADDR',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.address()

        if postAddy.status_code in [200,302,301] and 'Checkout.aspx?ACC=PAYD' in postAddy.url:
            logger.success(SITE,self.taskID,'Successfully logged in')
            self.pay()
        else:
            logger.error(SITE,self.taskID,'Failed to login. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.address()

    def pay(self):
        payload = {
            'countryCode': '',
            'merchantAccount': 'ProDirectBasketball',
            'merchantReference': 'WEB42780110',
            'merchantSig': 's6dCOHhgqQdWOPG/wtEqaTBHkgVq1Jl6+577CwwXNbo=',
            'brandCode': 'paypal',
            'issuerId': '',
            'recurringContract': 'RECURRING',
            'sessionValidity': datetime.datetime.now().isoformat(),
            'shopperLocale': 'en_GB',
            'skinCode': 'zrehvq6o',
            'paymentAmount': '16450',
            'currencyCode': 'GBP',
            'shopperEmail': 'charliebottomley15@gmail.com',
            'shopperReference': '220994720',
            'shopper.firstName': 'Charlie',
            'shopper.lastName': 'Bottomley',
            'billingAddress.houseNumberOrName': '',
            'billingAddress.street': '12 Pilmore Mews',
            'billingAddress.city': 'Hurworth',
            'billingAddress.stateOrProvince': 'Durham',
            'billingAddress.country': 'GB',
            'billingAddress.postalCode': 'DL2 2BQ',
            'deliveryAddress.houseNumberOrName':'',
            'deliveryAddress.street': '12 Pilmore Mews',
            'deliveryAddress.city': 'Hurworth',
            'deliveryAddress.stateOrProvince': 'Durham',
            'deliveryAddress.country': 'GB',
            'deliveryAddress.postalCode': 'DL2 2BQ'
        }
        adyen = self.session.post('https://live.adyen.com/hpp/skipDetails.shtml',data=payload,headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'

        })
        print(adyen)
        print(adyen.url)
        print(adyen.text)
        #payload = {
        #    'deliveryOptionInfo': 'STANDARD',
        #    'browserInfo': {"screenWidth":2560,"screenHeight":1440,"colorDepth":24,"userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36","timeZoneOffset":-60,"language":"en-US","javaEnabled":False},
        #    'paymentOption': 'paypal',
        #    'rbCard': 'newcard',
        #    'CardType': 'Adyen',
        #    'tbxIagree': 'agree',
        #    '__EVENTTARGET': 'fw100$btnGoToPayNow',
        #    'adyen-encrypted-data': ''
        #}


