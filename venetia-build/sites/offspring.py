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
import csv

from utils.logger import logger
from utils.webhook import discord
from utils.log import log
from utils.captcha import captcha
from utils.akamai import AKAMAI
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies, updateConsoleTitle, scraper, offspring_session)
SITE = 'OFFSPRING'


class OFFSPRING:
    def task_checker(self):
        originalTask = self.task
        while True:
            with open('./{}/tasks.csv'.format(SITE.lower()),'r') as csvFile:
                csv_reader = csv.DictReader(csvFile)
                row = [row for idx, row in enumerate(csv_reader) if idx in (self.rowNumber,self.rowNumber)]
                self.task = row[0]
                self.task['PRODUCT'] = 'https://www.offspring.co.uk/view/product/offspring_catalog/1,21/' + self.task['PRODUCT'] 
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
        
        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)

        threading.Thread(target=self.task_checker,daemon=True).start()
        self.collect()

    def collect(self):
        # cookies = AKAMAI.offspring(self.session, self.taskID)
        # while cookies["_abck"] == "error":
            # cookies = AKAMAI.offspring(self.session, self.taskID)


        # print(cookies)
        # cookies['_abck']
        while True:
            cookie = '4F04B3A4B98DEDEDA61982F45AD8E5FA~0~YAAQhkISArUy6bt3AQAARC41wAXuaEFsb0EcY8WZSUKjWoI9QX4btVmsBn2qBmZIVCb3lKWP74rOXYgcrexc8ZzQvHkKaKCbpI757FYJE+DmWzcbIDFFJxGcZMa/NH6P6D+zKr9Xt36w/qcc9dPJY7cL/87+wcFO9I+hWzsNEkv/vd7VgKL+uqcPAwp1fxnPcLVKpNAIzsLH7x0qKxB4pZJhBVbhx3OQftm+WVqic/rcfFyxwutEc8CG2qCPFzqTR2tli/JZZhLsHbFWuRgVHj5+/LRZbBBnvi64S0kmTcFQa9RufbtkibD4PbsS1H78WToKpvB9qPZLSl5CC6aycXKXWH2aD2HNHMXIe/xBUtNzECEiUoQRStkAkAiTJzoiL7vJSCrKecZX13wcq79pc+P7jBMEUdn33XlqVDxJ8f6I+res5TDOJsJUqgKzbKt675lNAg==~-1~-1~-1'
            cookie_obj = requests.cookies.create_cookie(domain=f'.offspring.co.uk',name='_abck',value=cookie)
            self.session.cookies.set_cookie(cookie_obj)
            if 'offspring' not in self.task['PRODUCT']:
                self.task['PRODUCT'] = 'https://www.offspring.co.uk/view/product/offspring_catalog/1,21/' + self.task['PRODUCT'] 


    # 
            logger.prepare(SITE,self.taskID,'Getting product page...')
            try:
                retrieve = self.session.get(self.task["PRODUCT"],headers={
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-languag': 'en-US,en;q=0.9'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue

            if retrieve.status_code == 503:
                logger.info(SITE,self.taskID,'Queue....')
                try:
                    akavpwr_VP_offspring_val = str(retrieve.headers['set-cookie']).split('akavpwr_VP_offspring=')[1].split(';')[0]
                    cookie_obj = requests.cookies.create_cookie(domain='www.offspring.co.uk',name='akavpau_VP_offspring',value=akavpwr_VP_offspring_val)
                    self.session.cookies.set_cookie(cookie_obj)
                    clearables = []
                    for cookie in self.session.cookies:
                        if cookie.name == 'akavpwr_VP_offspring':
                            continue
                        clearables.append((cookie.domain, cookie.path, cookie.name))
                        
                    for domain, path, name in clearables:
                        self.session.cookies.clear(domain, path, name)
                

                except Exception as e:
                    log.info(e)
                    pass
                continue
            

            currentVal = self.task['PRODUCT'].split('/offspring_catalog/')[1].split(',')[0]
            self.task['PRODUCT'] = self.task['PRODUCT'].replace(currentVal + ',', str(random.randint(1,99)) + ',')
            

            if retrieve.status_code == 200:
                if 'Something went wrong, please try again later.' in retrieve.text:
                    logger.error(SITE,self.taskID,'IP BAN. Rotating Proxy...')
                    self.session.proxies = loadProxy(self.task['PROXIES'],self.taskID,SITE)
                    time.sleep(2)
                    continue
                self.start = time.time()
                logger.warning(SITE,self.taskID,'Got product page')
                try:
                    logger.prepare(SITE,self.taskID,'Getting product data...')
                    soup = BeautifulSoup(retrieve.text, "html.parser")
                    self.pid = soup.find('input',{'id':'productCodeId'})['value']
                    self.csrf = soup.find('input',{'name':'CSRFToken'})['value']

        
                    foundSizes = soup.find('ul',{'data-locale':'UK'})
                    if foundSizes:
                        sizes = []
                        allSizes = []
                        for s in foundSizes:
                            try:
                                size = s['data-name']
                                sizes.append(size)
                                allSizes.append('{}:{}'.format(size, self.pid+s['data-value']))
                            except:
                                pass
        
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
                        continue
            
                except Exception as e:
                    log.info(e)
                    logger.error(SITE,self.taskID,'Failed to scrape page (Most likely out of stock). Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    continue


                self.addToCart()


            elif retrieve.status_code != 200:
                logger.error(SITE,self.taskID,f'Failed to get product page => {str(retrieve.status_code)}. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

    def addToCart(self):
        logger.prepare(SITE,self.taskID,'Checking Captcha...')

        cartPayload = {
            "productCode":self.sizeId,
            "wishlist":False
        }
    
        cookie_obj = requests.cookies.create_cookie(domain=f'.offspring.co.uk',name='CSRFToken',value=self.csrf)
        self.session.cookies.set_cookie(cookie_obj)

        try:
            capCheck = self.session.post('https://www.offspring.co.uk/view/captcha/isCaptchaEnabledForProduct', data={"productCode":self.pid},headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'accept': '*/*',
                'x-requested-with': 'XMLHttpRequest',
                'referer':self.task['PRODUCT'],
                'csrftoken':self.csrf,
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',

            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()


        if 'false' in capCheck.text:
            logger.warning(SITE,self.taskID,'No Captcha Required')
        elif 'true' in capCheck.text:
            logger.warning(SITE,self.taskID,'Captcha Required')
            captchaResponse = loadToken(SITE)
            if captchaResponse == "empty":
                captchaResponse = captcha.v2('6Ld-VBsUAAAAABeqZuOqiQmZ-1WAMVeTKjdq2-bJ',self.task["PRODUCT"],self.session.proxies,SITE,self.taskID)
            cartPayload['grecaptcharesponse'] = captchaResponse

        logger.prepare(SITE,self.taskID,'Carting Product...')
        try:
            atcResponse = self.session.post('https://www.offspring.co.uk/view/basket/add',data=cartPayload,headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'accept': '*/*',
                'x-requested-with': 'XMLHttpRequest',
                'referer':self.task['PRODUCT'],
                'csrftoken':self.csrf,
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'origin': 'https://www.offspring.co.uk',
                'authority': 'www.offspring.co.uk',
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'cookie':f'CSRFToken={self.csrf};',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()
        
        try:
            data = atcResponse.json()
            statusCode = data['statusCode']
        except Exception as e:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task['DELAY']))
            self.addToCart()

        if statusCode == "success":
            updateConsoleTitle(True,False,SITE)
            logger.warning(SITE,self.taskID,'Successfully carted')
            self.productTitle = data['entry']['product']['name']
            self.productPrice = data['entry']['totalPrice']['formattedValue']
            self.productImage = data['entry']['product']['images'][0]['url']
            self.cartCode = data['cartCode']
            self.delivery()
        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

    def delivery(self):
        logger.prepare(SITE,self.taskID,'Setting shipping country...')

        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()

        payload = {
            "countryIsoCode": profile['countryCode'].upper(),
            "CSRFToken": self.csrf
        }


        try:
            shippingCountry = self.session.post('https://www.offspring.co.uk/view/component/singlepagecheckout/setDeliveryCountry',data=payload,headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'accept': '*/*',
                'referer':'https://www.offspring.co.uk/checkout/singlePageCheckout',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'x-requested-with': 'XMLHttpRequest',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.delivery()

        try:
            data = shippingCountry.json()
            status = data['updateStatus']
        except Exception as e:
            logger.error(SITE,self.taskID,'Failed to set shipping country. Retrying...')
            time.sleep(int(self.task['DELAY']))
            self.delivery()

        if shippingCountry.status_code == 200 and status == 'SUCCESS':
            methods = data['orderSummary']['deliveryModes']
            if len(methods) == 1:
                self.option = methods[0]["code"]
            else:
                for k in methods:
                    if 'standard' in k['name'].lower():
                        self.option = k['code']
            logger.warning(SITE,self.taskID,'Set shipping country')

        else:
            logger.error(SITE,self.taskID,'Failed to set shipping country. Retrying...')
            time.sleep(int(self.task['DELAY']))
            self.delivery()

        # print(self.session.cookies)
        logger.prepare(SITE,self.taskID,'Setting delivery...')
        deliveryPayload = {
            "deliveryModeCode": self.option,
            "CSRFToken": self.csrf
        }

        try:
            deliveryResponse = self.session.post('https://www.offspring.co.uk/view/component/singlepagecheckout/setDeliveryMode', data=deliveryPayload,headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'accept': '*/*',
                'x-requested-with': 'XMLHttpRequest',
                'referer':'https://www.offspring.co.uk/checkout/singlePageCheckout',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.delivery()

        try:
            data = deliveryResponse.json()
            statusCode = data['updateStatus']
        except Exception as e:
            logger.error(SITE,self.taskID,'Failed to set delivery. Retrying...')
            time.sleep(int(self.task['DELAY']))
            self.delivery()

        if statusCode == "SUCCESS":
            logger.warning(SITE,self.taskID,'Delivery Set')
            self.address()
        else:
            logger.error(SITE,self.taskID,'Failed to set delivery. Retrying...')
            time.sleep(int(self.task['DELAY']))
            self.delivery()

    def address(self):
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()

        logger.prepare(SITE,self.taskID,'Submitting address...')
        addyPayload = {
            "email": profile['email'],
            "title": 'Mr',
            "titleCode": 'mr',
            "phone": profile['phone'],
            "firstName": profile['firstName'],
            "lastName": profile['lastName'],
            "companyName": '',
            "line1": profile['house'] + ' ' + profile['addressOne'],
            "line2": profile['addressTwo'],
            "town": profile['city'],
            "postalCode": profile['zip'],
            "country": profile['countryCode'],
            "defaultAddress": True,
            "CSRFToken": self.csrf
        }

        try:
            addyResponse = self.session.post('https://www.offspring.co.uk/view/component/singlepagecheckout/addEditDeliveryAddress', data=addyPayload,headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'accept': '*/*',
                'referer':'https://www.offspring.co.uk/checkout/singlePageCheckout',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'x-requested-with': 'XMLHttpRequest',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.address()

        if addyResponse.status_code == 200:
            logger.warning(SITE,self.taskID,'Submitted Address')
            if self.task["PAYMENT"].lower() == "paypal":
                self.paypal()

        else:
            logger.error(SITE,self.taskID,'Failed to submit address. Retrying...')
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.address()


    def paypal(self):
        logger.info(SITE,self.taskID,'Starting [PAYPAL] checkout...')
        logger.prepare(SITE,self.taskID,'Getting paypal link...')
        payPayload = {
            'paymentMode': 'worldpay_paypal',
            'emailOptIn': 'true',
            'newsAlerts': 'true',
            'CSRFToken': self.csrf
        }
        try:
            paymentPost = self.session.post('https://www.offspring.co.uk/view/component/singlepagecheckout/continueToPaymentDetails', data=payPayload,headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'referer':'https://www.offspring.co.uk/checkout/singlePageCheckout',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'x-requested-with': 'XMLHttpRequest',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.paypal()

        if paymentPost.status_code in [200,302] and "paypal" in paymentPost.url:
            self.end = time.time() - self.start
            logger.warning(SITE,self.taskID,'Successfully got paypal link')
            updateConsoleTitle(False,True,SITE)
            logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')
            url = storeCookies(paymentPost.url,self.session, self.productTitle, self.productImage, self.productPrice)

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
            except Exception as e:
                log.info(e)
                logger.alert(SITE,self.taskID,'Failed to send webhook. Checkout here ==> {}'.format(url))
        
        else:
            logger.error(SITE,self.taskID,'Failed to get paypal link. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.paypal()

        
        