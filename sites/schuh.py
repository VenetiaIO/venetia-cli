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


from utils.logger import logger
from utils.webhook import discord
from utils.log import log
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification,storeCookies)
SITE = 'SCHUH'


class SCHUH:
    def __init__(self, task,taskName):
        self.task = task
        self.session = requests.session()
        self.taskID = taskName
        
        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer':self.task["PRODUCT"]
        }

        self.collect()

    def collect(self):
        try:
            retrieve = self.session.get(self.task["PRODUCT"])
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.collect()

        if retrieve.status_code == 200:
            logger.success(SITE,self.taskID,'Got product page')
            try:
                soup = BeautifulSoup(retrieve.text,"html.parser")
                self.productImage = soup.find('img',{'class':'noScriptImage'})['src']
                sizeSelect = soup.find('select',{'id':'sizes'})
                self.locale = soup.find('span',{'id':'cultureCI-val'}).text
                self.hidPrice = soup.find('input',{'id':'hidPrice'})['value']
                
                all_sizes = []
                sizes = []
    
                for s in sizeSelect:
                    try:
                        size = s["data-dispsize"].split(' ')[1]
                        sizeValue = s["value"]
                        iCode = s["data-icode"]
                        junior = s["data-isjunior"]
                        all_sizes.append(f'{size}:{sizeValue}:{iCode}:{junior}')
                        sizes.append(size)
                    except:
                        pass
                
                if len(sizes) == 0:
                    logger.error(SITE,self.taskID,'Size Not Found')
                    time.sleep(int(self.task["DELAY"]))
                    self.collect()
    
                if self.task["SIZE"].lower() == "random":
                    chosen = random.choice(all_sizes)
                    self.sizeValue = chosen.split(':')[1]
                    self.size = chosen.split(':')[0]
                    self.icode = chosen.split(':')[2]
                    self.isJunior = chosen.split(':')[3]
                    logger.success(SITE,self.taskID,f'Found Size => {self.size}')
                    self.addToCart()
                    
                else:
                    if self.task["SIZE"] not in sizes:
                        logger.error(SITE,self.taskID,'Size Not Found')
                        time.sleep(int(self.task["DELAY"]))
                        self.collect()
                    for size in all_sizes:
                        if self.task["SIZE"] == size.split(':')[0]:
                            self.size = size.split(':')[0]
                            logger.success(SITE,self.taskID,f'Found Size => {self.size}')
                            self.sizeValue = size.split(':')[1]
                            self.icode = size.split(':')[2]
                            self.isJunior = size.split(':')[3]
                            self.addToCart()
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to scrape page (Most likely out of stock). Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.collect()

            
        else:
            try:
                status = retrieve.status_code
            except:
                status = 'Unknown'
            logger.error(SITE,self.taskID,f'Failed to get product page => {status}. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.collect()

    def addToCart(self):
        logger.warning(SITE,self.taskID,'Carting products...')
        region = self.task["PRODUCT"].split('schuh.')[1].split('/')[0]
        self.baseURL = 'https://secure.schuh.{}'.format(region)

        payload = {
            "iCode":self.icode,
            "szRef":self.sizeValue,
            "quantity":"1",
            "price":self.hidPrice,
            "parentcode":"",
            "preorder":0,
            "sku":"0",
            "branchRef":0,
            "position":1,
            "junior":self.isJunior,
            "locale":self.locale,
            "merchUrl":"",
            "merchType":""
        }
        self.session.headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        try:
            cart = self.session.post(f'{self.baseURL}/BasketService/AddToBasket',json=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()
        try:
            json = cart.json()
        except:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            if self.task["SIZE"] == "random":
                self.collect()
            else:
                self.addToCart()

        if cart.status_code == 200 and json["d"]["Success"] == True:
            logger.success(SITE,self.taskID,'Successfully carted')
            self.basket()
        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            if self.task["SIZE"] == "random":
                self.collect()
            else:
                self.addToCart()

    def basket(self):
        logger.warning(SITE,self.taskID,'Updating basket details...')
        payload = {"action":"delivery","deliveryOptionCode":"0","branchRef":"0"}
        try:
            update = self.session.post(f'{self.baseURL}/BasketService/updateBasket',json=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.basket()

        if update.status_code == 200:
            logger.success(SITE,self.taskID,'Basket details updated')

            self.session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
            self.session.headers['Referer'] = f'{self.baseURL}/basket.aspx'
            try:
                login = self.session.post(f'{self.baseURL}/login.aspx',json=payload)
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.basket()

            if login.status_code == 200 and 'klarnaCheckout' in login.url:
                logger.success(SITE,self.taskID,'Successfully got checkout page')
                self.orderURL = login.text.split('ORDER_URL:')[1].split(',')[0].replace("'",'')
                self.klarnaID = self.orderURL.split('/orders/')[1]
                self.klarnaAuth = login.text.split('AUTH_HEADER:')[1].split(',')[0].replace("'",'')
                self.klarnaCheckout()
            else:
                logger.error(SITE,self.taskID,'Failed to get checkout page. Retrying...')
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                self.collect()

        else:
            logger.error(SITE,self.taskID,'Failed to update basket details. Retrying...')

    
    def klarnaCheckout(self):
        try:
            initKlarna = self.session.get(f'https://js.klarna.com/eu/kco/checkout/orders/{self.klarnaID}?type=initial',headers={
                'accept':'application/vnd.klarna.checkout.server-order-v1+json',
                'authorization':self.klarnaAuth,
                'referer':'https://js.klarna.com/kcoc/200729-bdbb575/checkout-template.html',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'klarna-client-version': '200713-dd02c1f',
                'klarna-sdid': '6e390e93-c3b6-4ef8-8700-97689e3f155f',
                'klarna-sdid-status': 'new'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.klarnaCheckout()
        
        if initKlarna.status_code == 200:
            self.klarnaSession = initKlarna.json()
            self.productTitle = self.klarnaSession["cart"]["items"][0]["name"]
            self.subTotal = int(self.klarnaSession["cart"]["subtotal"]) / 100
            self.currency = self.klarnaSession["shared"]["currency"]
            self.productPrice = f'{self.subTotal} {self.currency}'
            logger.success(SITE,self.taskID,'Successfully initialized Klarna checkout')
        else:
            logger.error(SITE,self.taskID,'Failed to initialize klarna chekout. Retrying...')

        self.session.headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        self.session.headers['X-Requested-With'] = 'XMLHttpRequest'
        self.session.headers['Referer'] = f'{self.baseURL}/klarnaCheckout.aspx'

        profile = loadProfile(self.task["PROFILE"])
        try:
            payload = {"email":profile["email"]}
            klarnaEmail = self.session.post(f'{self.baseURL}/CheckoutService/RegisterKlarnaEmail',json=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.klarnaCheckout()
        
        if klarnaEmail.status_code == 200:
            logger.success(SITE,self.taskID,'Klarna email registered')
            #self.address()
            self.paypal()
        else:
            logger.success(SITE,self.taskID,'Failed to register klarna email. Retrying...')
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.collect()
    
    def paypal(self):
        profile = loadProfile(self.task["PROFILE"])

        self.session.headers['Accept'] = '*/*'
        self.session.headers['X-Requested-With'] = 'XMLHttpRequest'
        self.session.headers['Referer'] = f'{self.baseURL}/klarnaCheckout.aspx'

        try:
            payID = self.session.post('https://secure.schuh.co.uk/PayWithPayPalInContext.aspx?viewPort=3&repay=0&country=GB&referrer=klarna',data={
                'viewPort': 3,
                'repay': 0,
                'country': profile["countryCode"],
                'referrer': 'klarna'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.paypal()

        if payID.status_code == 200:
            logger.success(SITE,self.taskID,'Successfully Retrieved PayPal PayID')
            self.payID = payID.text.replace('"','')

            self.session.headers['accept'] = 'application/json'
            self.session.headers['x-cookies'] = '{}'
            self.session.headers['x-csrf-jwt'] = '__blank__'
            self.session.headers['x-requested-by'] = 'smart-payment-buttons'
            self.session.headers['x-Requested-With'] = 'XMLHttpRequest'
            try:
                EC = self.session.post(f'https://www.paypal.com/smart/api/payment/{self.payID}/ectoken',json={"meta":{}})
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.paypal()
            try:
                EC.json()
            except:
                logger.error(SITE,self.taskID,'Failed to retrieve paypal checkout info. Retrying...')
                time.sleep(int(self.task['DELAY']))
                self.paypal()
            if EC.status_code == 200:
                self.ppToken = EC.json()["data"]["token"]

                self.ppURL = 'https://www.paypal.com/checkoutnow?locale.x=en_GB&fundingSource=paypal&env=production&fundingOffered=paypal&logLevel=warn&version=4&token={}&xcomponent=1'.format(self.ppToken)

                logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')

                url = storeCookies(self.ppURL,self.session)
    
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
                    product=self.task["PRODUCT"]
                )
                sendNotification(SITE,self.productTitle)
                while True:
                    pass
            else:
                logger.error(SITE,self.taskID,'Could not complete PayPal Checkout. Retrying...')
                discord.failed(
                    webhook=loadSettings()["webhook"],
                    site=SITE,
                    url=self.task["PRODUCT"],
                    image=self.productImage,
                    title=self.productTitle,
                    size=self.size,
                    price=self.productPrice,
                    paymentMethod='PayPal',
                    profile=self.task["PROFILE"]
                )
                logger.error(SITE,self.taskID,'Failed to retrieve paypal checkout info. Retrying...')
                time.sleep(int(self.task['DELAY']))
                self.paypal()

        else:
            logger.error(SITE,self.taskID,'Failed to retrieve paypal payID. Retrying...')
            time.sleep(int(self.task['DELAY']))
            self.paypal()

    
    #def address(self):
    #    profile = loadProfile(self.task["PROFILE"])
    #    payload = {"browser_prefilled":["postal_code"],"customer_details":{"email":profile["email"],"postal_code":profile["zip"]},"skipped_fields":[],"user_submitted":False,"action":"postalCodeChange"}
    #    try:
    #        addressKlarna = self.session.get(f'https://js.klarna.com/eu/customer/client/v1/session/{self.klarnaID}')
    #    except:
    #        logger.error(SITE,self.taskID,'Connection Error. Retrying...')
    #        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
    #        time.sleep(int(self.task["DELAY"]))
    #        self.collect()
#
    #    url = 'https://js.klarna.com/eu/address/v2/country/{}/postal/{}/street/{}{}?acquiring_source=kco&source_reference={}'.format(profile["countryCode"],profile["zip"],profile["house"],profile["addressOne"],self.klarnaID)#.replace(' ','%20')
    #    print(url)
#
    #    self.session.headers['accept'] = 'application/json, text/plain, */*'
    #    self.session.headers['referer'] = 'https://js.klarna.com/kcoc/200729-bdbb575/checkout-template.html'
    #    try:
    #        addressKlarna = self.session.get(url)
    #    except:
    #        logger.error(SITE,self.taskID,'Connection Error. Retrying...')
    #        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
    #        time.sleep(int(self.task["DELAY"]))
    #        self.collect()
    #    
    #    print(addressKlarna)
    #    print(addressKlarna.json())


