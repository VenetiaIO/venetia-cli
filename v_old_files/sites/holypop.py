import requests
from bs4 import BeautifulSoup
import datetime
import threading
import random
import sys
import time
import re
import json
import base64
import string
from urllib3.exceptions import HTTPError
import csv
SITE = 'HOLYPOP'

from utils.logger import logger
from utils.captcha import captcha
from utils.webhook import discord
from utils.log import log
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification,storeCookies, updateConsoleTitle)

class HOLYPOP:
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

    def __init__(self,task,taskName,rowNumber):
        self.task = task
        self.session = requests.session()
        self.taskID = taskName
        self.rowNumber = rowNumber

        self.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
        self.session.proxies = self.proxies
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'referer':'https://www.holypopstore.com/en'
        }
        threading.Thread(target=self.task_checker,daemon=True).start()
        
        if 'holypop' in self.task["PRODUCT"]:
            self.collect()
        else:
            self.itemId = self.task["PRODUCT"]
            self.login()

    def collect(self):
        while True:
            logger.prepare(SITE,self.taskID,'Getting product page...')
            try:
                retrieve = self.session.get(self.task["PRODUCT"])
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if retrieve:
                if retrieve.status_code == 200:
                    logger.warning(SITE,self.taskID,'Got product page')
                    logger.prepare(SITE,self.taskID,'Getting product data...')
                    self.start = time.time()
                    regex = r"preloadedStock =(.+)"
                    matches = re.search(regex, retrieve.text, re.MULTILINE)
                    if matches:
                        matches = matches.group().split('preloadedStock = ')[1]
                        productData = json.loads(matches[:-1])
        
                        allSizes = []
                        sizes = []
            
                        for s in productData:
                            size = s["variant"].split(' US')[0]
                            id = s["id"]
                            allSizes.append('{}:{}'.format(size,id))
                            sizes.append(size)
            
                        if len(sizes) == 0:
                            logger.error(SITE,self.taskID,'Size Not Found')
                            time.sleep(int(self.task["DELAY"]))
                            continue
            
                        if self.task["SIZE"].lower() != "random":
                            if self.task["SIZE"] not in sizes:
                                logger.error(SITE,self.taskID,'Size Not Found')
                                time.sleep(int(self.task["DELAY"]))
                                continue
                            else:
                                for size in allSizes:
                                    if size.split(':')[0] == self.task["SIZE"]:
                                        self.size = size.split(':')[0]
                                        self.itemId = size.split(':')[1]
                                        logger.warning(SITE,self.taskID,f'Found Size => {self.size}')
                                        self.login()
            
                        
                        elif self.task["SIZE"].lower() == "random":
                            selected = random.choice(allSizes)
                            self.size = selected.split(":")[0]
                            self.itemId = selected.split(":")[1]
                            logger.warning(SITE,self.taskID,f'Found Size => {self.size}')
                            self.login()
                    else:
                        logger.error(SITE,self.taskID,'Failed to scrape page. Retrying....')
                        time.sleep(int(self.task["DELAY"]))
                        continue
            else:
                logger.error(SITE,self.taskID,f'Failed to get product page => {str(retrieve.status_code)}. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                continue


    def login(self):
        logger.prepare(SITE,self.taskID,'Logging in...')
        try:
            getLogin = self.session.get('https://www.holypopstore.com/')
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.login()

        if getLogin.status_code == 200:
            try:
                self.version = getLogin.text.split("b.version = '")[1].split("';")[0]
                self.cookieVersion = getLogin.text.split("b.cookieVersion = '")[1].split("';")[0]
                self.region = getLogin.text.split("b.locale = '")[1].split("';")[0].upper()
            except:
                logger.error(SITE,self.taskID,'Failed to login. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.login()
                
            self.session.headers['accept'] = 'application/json, text/javascript, */*; q=0.01'
            self.session.headers['x-requested-with'] = 'XMLHttpRequest'

            payload2 = {
                'controller': 'auth',
                'action': 'authenticate',
                'type': 'standard',
                'extension': 'holypop',
                'credential': self.task["ACCOUNT EMAIL"],
                'password': self.task["ACCOUNT PASSWORD"],
                'language': self.region,
                'version': self.version,
                'cookieVersion': self.cookieVersion
            }
            self.session.headers['referer'] = 'https://www.holypopstore.com/en/login/signin'
            try:
                signIn = self.session.post('https://www.holypopstore.com/index.php',data=payload2)
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.login()
            if signIn.status_code != 200:
                logger.error(SITE,self.taskID,'Failed to login. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.login()
            else:
                logger.warning(SITE,self.taskID,'Successfully logged in')
                self.addToCart()
        
        else:
            logger.error(SITE,self.taskID,'Failed to get login page. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.login()


    
    def addToCart(self):
        self.session.headers['referer'] = self.task["PRODUCT"]
        logger.prepare(SITE,self.taskID,'Carting product...')

        payload = {
            'controller': 'orders',
            'action': 'addStockItemToBasket',
            'stockItemId': self.itemId, 
            'quantity': 1,
            'extension': 'holypop',
            'language': self.region,
            'version': self.version,
            'cookieVersion': self.cookieVersion
        }
        try:
            cart = self.session.post('https://www.holypopstore.com/index.php',data=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()

        try:
            jsonData = cart.json()
        except Exception as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

        if cart.status_code == 200 and jsonData["success"] == True:
            updateConsoleTitle(True,False,SITE)
            logger.warning(SITE,self.taskID,'Successfully carted')
            self.productTitle = cart.json()["payload"][0]["title"]
            self.size = cart.json()["payload"][0]["attributes"][0]["value"]["title"]
            self.productImage = cart.json()["payload"][0]["imageObject"]["imageUrl"]
            self.productPrice = '{} {}'.format(cart.json()["payload"][0]["price"],cart.json()["payload"][0]["currencyCode"])
            self.productLink = cart.json()["payload"][0]["permalink"]
            if self.task["PAYMENT"].lower() == "cart hold":
                updateConsoleTitle(False,True,SITE)
                self.end = time.time() - self.start
                try:
                    discord.success(
                        webhook=loadSettings()["webhook"],
                        site=SITE,
                        url=self.productLink,
                        image=self.productImage,
                        title=self.productTitle,
                        size=self.size,
                        price=self.productPrice,
                        paymentMethod='Cart Hold',
                        profile=self.task["PROFILE"],
                        account=self.task["ACCOUNT EMAIL"],
                        product=self.task["PRODUCT"],
                        proxy=self.session.proxies,
                        speed=self.end
                    )
                except:
                    logger.secondary(SITE,self.taskID,'Failed to send webhook. Cart Hold ==> {}'.format(self.task["ACCOUNT EMAIL"]))
                    
            elif self.task["PAYMENT"].lower() == "paypal":
                self.checkout()
        else:
            try:
                message = jsonData["error"]["reference"]
            except:
                message = 'Out of stock'
            logger.error(SITE,self.taskID,'Failed to cart [{}]. Retrying...'.format(message))

    
    def checkout(self):
        logger.prepare(SITE,self.taskID,'Getting checkout page...')
        self.session.headers['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        self.session.headers['referer'] = 'https://www.holypopstore.com/{}'.format(self.region.lower())
        self.session.headers['x-requested-with'] = ''
        try:
            checkout = self.session.get('https://www.holypopstore.com/en/orders/review')
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.checkout()

        if checkout.status_code == 200:
            logger.warning(SITE,self.taskID,'Successfully got checkout page')
            soup = BeautifulSoup(checkout.text,"html.parser")
            addressId = soup.find('option',{'selected':'selected'})["value"]
            regex = r"preloadedShippers =(.+)"
            matches = re.search(regex, checkout.text, re.MULTILINE)
            if matches:
                try:
                    matches = matches.group().split('preloadedShippers = ')[1]
                    productData = json.loads(matches[:-1])
                    shipperId = productData[0]["id"]
                    shipperAccountId = productData[0]["accounts"][0]["id"]
                except Exception as e:
                    log.info(e)
                    logger.error(SITE,self.taskID,'Failed to get shipping info. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.checkout()
                

            captchaResponse = loadToken(SITE)
            if captchaResponse == "empty":
                captchaResponse = captcha.v2('6Lc8GBUUAAAAAKMfe1S46jE08TvVKNSnMYnuj6HN',self.task["PRODUCT"],self.proxies,SITE,self.taskID)

            payload = {
                'secretly': False,
                'hardErrorize': False,
                'billingAddressId': addressId,
                'shippingAddressId': addressId,
                'shipmentFlow': 'DELIVERY',
                'newAddresses': 0,
                'requestInvoice': 0,
                'notes': '',
                'paymentMethodId': 1,
                'paymentMethodAccountId': 1,
                'shipments[0][shipmentFlow]': 'DELIVERY',
                'shipments[0][addressId]': addressId,
                'shipments[0][shipperId]': shipperId,
                'shipments[0][shipperAccountId]': shipperAccountId,
                'recaptcha':captchaResponse,
                'toDisplay': 0,
                'extension': 'holypop',
                'controller': 'orders',
                'action': 'save',
                'language': self.region,
                'version': self.version,
                'cookieVersion': self.cookieVersion
            }
            logger.prepare(SITE,self.taskID,'Submitting shipping...')
            self.session.headers['referer'] = 'https://www.holypopstore.com/{}/orders/review'.format(self.region.lower())
            self.session.headers['x-requested-with'] = 'XMLHttpRequest'
            self.session.headers['accept'] = 'application/json, text/javascript, */*; q=0.01'
            try:
                postCheckout = self.session.post('https://www.holypopstore.com/index.php',data=payload)
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.checkout()

            try:
                jsonData = postCheckout.json()
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to submit shipping. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.checkout()

            if postCheckout.status_code == 200:
                self.orderId = jsonData["payload"]["orderId"]
                logger.warning(SITE,self.taskID,'Successfully submitted shipping')
                self.startPP()
            else:
                logger.error(SITE,self.taskID,'Failed to submit shipping. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.checkout()

        else:
            logger.error(SITE,self.taskID,'Failed to get checkout. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.checkout()

    def startPP(self):
        logger.info(SITE,self.taskID,'Starting [PAYPAL] checkout...')
        self.session.headers['referer'] = 'https://www.holypopstore.com/{}/orders/review'.format(self.region.lower())
        self.session.headers['x-requested-with'] = ''
        self.session.headers['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        logger.prepare(SITE,self.taskID,'Getting paypal link...')
        try:
            checkout = self.session.get(f'https://www.holypopstore.com/en/orders/checkout/{self.orderId}',params={'paymentMethodId':1,'paymentMethodAccountId':1})
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.startPP()

        if checkout.status_code == 200 and "paypal" in checkout.url:
            logger.warning(SITE,self.taskID,'Successfully got paypal link')
            self.end = time.time() - self.start
            logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')
            updateConsoleTitle(False,True,SITE)

            url = storeCookies(checkout.url,self.session, self.productTitle, self.productImage, self.productPrice)
            
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
                sendNotification(SITE,self.productTitle)
                while True:
                    pass
            except:
                    logger.alert(SITE,self.taskID,'Failed to send webhook. Checkout here ==> {}'.format(url))
        else:
            logger.error(SITE,self.taskID,'Failed to get PayPal checkout. Retrying...')
            try:
                discord.failed(
                    webhook=loadSettings()["webhook"],
                    site=SITE,
                    url=self.productLink,
                    image=self.productImage,
                    title=self.productTitle,
                    size=self.size,
                    price=self.productPrice,
                    paymentMethod='PayPal',
                    profile=self.task["PROFILE"],
                    proxy=self.session.proxies
                )
            except:
                pass
            time.sleep(int(self.task["DELAY"]))
            self.startPP()

                


    
        

