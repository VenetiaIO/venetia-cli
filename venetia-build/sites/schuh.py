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


from utils.logger import logger
from utils.webhook import discord
from utils.log import log
from utils.adyen import ClientSideEncrypter
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification,storeCookies, updateConsoleTitle)
SITE = 'SCHUH'


class SCHUH:
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
        
        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer':self.task["PRODUCT"]
        }

        threading.Thread(target=self.task_checker,daemon=True).start()
        self.collect()

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

            if retrieve.status_code == 200:
                self.start = time.time()
                logger.warning(SITE,self.taskID,'Got product page')
                try:
                    logger.prepare(SITE,self.taskID,'Getting product data...')
                    soup = BeautifulSoup(retrieve.text,"html.parser")
                    self.productImage = soup.find('img',{'class':'noScriptImage'})['src']
                    sizeSelect = soup.find('select',{'id':'sizes'})
                    self.locale = soup.find('span',{'id':'cultureCI-val'}).text
                    self.hidPrice = soup.find('input',{'id':'hidPrice'})['value']
                    self.productTitle = soup.find('title').text.split('|')[0]
                    self.productPrice = soup.find('span',{'id':'price'}).text

                    all_sizes = []
                    sizes = []
        
                    for s in sizeSelect:
                        try:
                            size = s["data-dispsize"]
                            try:
                                size = size.split(' ')[1]
                            except:
                                pass
                            
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
                        continue
        
                    if self.task["SIZE"].lower() == "random":
                        chosen = random.choice(all_sizes)
                        self.sizeValue = chosen.split(':')[1]
                        self.size = chosen.split(':')[0]
                        self.icode = chosen.split(':')[2]
                        self.isJunior = chosen.split(':')[3]
                        logger.warning(SITE,self.taskID,f'Found Size => {self.size}')
                        self.addToCart()
                        
                    else:
                        if self.task["SIZE"] not in sizes:
                            logger.error(SITE,self.taskID,'Size Not Found')
                            time.sleep(int(self.task["DELAY"]))
                            continue
                        for size in all_sizes:
                            if self.task["SIZE"] == size.split(':')[0]:
                                self.size = size.split(':')[0]
                                logger.warning(SITE,self.taskID,f'Found Size => {self.size}')
                                self.sizeValue = size.split(':')[1]
                                self.icode = size.split(':')[2]
                                self.isJunior = size.split(':')[3]
                                self.addToCart()
                except Exception as e:
                    log.info(e)
                    logger.error(SITE,self.taskID,'Failed to scrape page (Most likely out of stock). Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    continue

                
            else:
                logger.error(SITE,self.taskID,f'Failed to get product page => {str(retrieve.status_code)}. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

    def addToCart(self):
        logger.prepare(SITE,self.taskID,'Carting products...')
        region = self.task["PRODUCT"].split('schuh.')[1].split('/')[0]
        if region == 'eu': region = region + '/en-eu'
        
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
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
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
            updateConsoleTitle(True,False,SITE)
            logger.warning(SITE,self.taskID,'Successfully carted')
            self.basket()
        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            if self.task["SIZE"] == "random":
                self.collect()
            else:
                self.addToCart()

    def basket(self):
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()

        if profile['countryCode'].upper() == 'FR':
            payload = {"action":"delivery","deliveryOptionCode":"478","countryLocale":"FR"}
        if profile['countryCode'].upper() == 'PT':
            payload = {"action":"delivery","deliveryOptionCode":"578","countryLocale":"PT"}
        if profile['countryCode'].upper() == 'RO':
            payload = {"action":"delivery","deliveryOptionCode":"582","countryLocale":"RO"}
        if profile['countryCode'].upper() == 'ES':
            payload = {"action":"delivery","deliveryOptionCode":"605","countryLocale":"ES"}
        if profile['countryCode'].upper() == 'GB':
            payload = {"action":"checkout","deliveryOptionCode":"0","viewPort":"1","branchRef":"0","chosenDate":""}
            self.country = 'UK'
            self.region2 = 'england'



        logger.prepare(SITE,self.taskID,'Updating basket details...')
        try:
            update = self.session.post(f'{self.baseURL}/BasketService/updateBasket',json=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.basket()

        if update.status_code == 200:
            logger.warning(SITE,self.taskID,'Basket details updated')

            self.checkoutLogin()

        else:
            logger.error(SITE,self.taskID,'Failed to update basket details. Retrying...')
            self.basket()

    def checkoutLogin(self):

        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()

        logger.prepare(SITE,self.taskID,'Initiating checkout...')
        

        payload = {"loginType":"new","email":profile['email'],"password":"-1","mailOrderEmail":"-1","page":"login.aspx"}

        try:
            checkoutLog = self.session.post(f'{self.baseURL}/CheckoutService/checkoutLogin',json=payload,headers={
                'Accept':'application/json, text/javascript, */*; q=0.01n',
                'referer':f'{self.baseURL}/login.aspx',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.checkoutLogin()

        try:
            data = checkoutLog.json()
            stat = data['d']['Success']
        except Exception as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Failed to initiate checkout.Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.checkoutLogin()

        if checkoutLog.status_code == 200 and stat == True:
            logger.warning(SITE,self.taskID,'Successfully Initiated checkout')
            self.addressSubmit()
        else:
            logger.error(SITE,self.taskID,'Failed to initiate checkout.Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.checkoutLogin()


    def addressSubmit(self):
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()

        logger.prepare(SITE,self.taskID,'Submitting address...')


    

        js = {
            "addressID": 0,
            "title": "Mr",
            "firstName": profile['firstName'],
            "surname": profile['lastName'],
            "phone": profile['phone'],
            "line1": profile['house'] + ' ' + profile['addressOne'],
            "line2": profile['addressTwo'],
            "cityTown": profile['city'],
            "county": profile['region'],
            "postcode": profile['zip'],
            "country": self.country,
            "countryDelOptionCode": 0,
            "addressBookCount": 0,
            "addressType": "d",
            "billingSameAsDelivery": True,
            "region": self.region2
        }
        payload = {"addressString":str(json.dumps(js)),"addressType":"d"}

        try:
            addressSub = self.session.post(f'{self.baseURL}/CheckoutService/AddressBookSubmit',json=payload,headers={
                'Accept':'application/json, text/javascript, */*; q=0.01n',
                'referer':f'{self.baseURL}/delivery.aspx',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addressSubmit()

        try:
            data = addressSub.json()
            stat = data['d']['Success']
        except Exception as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Failed to submit address.Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addressSubmit()

        
        if addressSub.status_code == 200 and stat == True:
            logger.warning(SITE,self.taskID,'Successfully submitted address')

            if self.task['PAYMENT'].lower() == 'paypal':
                self.paypalPayment()
            else:
                self.cardPayment()

        else:
            logger.error(SITE,self.taskID,'Failed to submit address.Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addressSubmit()

        sys.exit()


    def paypalPayment(self):
        logger.prepare(SITE,self.taskID,'Submitting payment...')
        try:
            paymentProcess = self.session.post(f'{self.baseURL}/CheckoutService/PaymentProcess',json={"type":"paypal","repayment":False,"viewPort":"3","repaymentid":"0"},headers={
                'Accept':'application/json, text/javascript, */*; q=0.01n',
                'referer':f'{self.baseURL}/billing.aspx',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.paypalPayment()



        if paymentProcess.status_code == 200:
            try:
                finalUrl = '{}/{}'.format(self.baseURL, paymentProcess.json()['d'].split('success:')[1]).replace('viewPort=3','viewPort=1')
            except:
                logger.error(SITE,self.taskID,'Failed to submit payment.Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.paypalPayment()
        
            try:
                getPayal = self.session.get(finalUrl, headers={
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9n',
                    'referer':f'{self.baseURL}/billing.aspx',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.paypalPayment()
            if 'paypal' in getPayal.url:
                logger.warning(SITE,self.taskID,'Payment submitted')
                updateConsoleTitle(False,True,SITE)
                self.end = time.time() - self.start
                logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')
                url = storeCookies(getPayal.url,self.session, self.productTitle, self.productImage, self.productPrice)


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
                except Exception as e:
                    print(e)
                    logger.alert(SITE,self.taskID,'Failed to send webhook. Checkout here ==> {}'.format(url))
            else:
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
                        proxy=self.session.proxies
                    )
                except:
                    pass

                logger.error(SITE,self.taskID,'Failed to submit payment.Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.paypalPayment()
        
        else:
            logger.error(SITE,self.taskID,'Failed to submit payment.Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.paypalPayment()

    def cardPayment(self):
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()

        logger.prepare(SITE,self.taskID,'Setting payment method...')
        try:
            paymentProcess = self.session.post(f'{self.baseURL}/CheckoutService/PaymentProcess',json={"type":"adyen","repayment":False,"viewPort":"1","repaymentid":"0"},headers={
                'Accept':'application/json, text/javascript, */*; q=0.01n',
                'referer':f'{self.baseURL}/billing.aspx',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.cardPayment()

        if paymentProcess.status_code == 200 and 'adyen' in paymentProcess.text:
            try:
                self.orderNumber = paymentProcess.text.split('success:adyen:')[1].split('|')[0]
                self.orderTotal = paymentProcess.text.split('|')[1].split('"}')[0]
            except Exception as e:
                logger.error(SITE,self.taskID,'Failed to set payment method. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.cardPayment()

            logger.warning(SITE,self.taskID,'Successfully set payment method')

            logger.prepare(SITE,self.taskID,'Starting Adyen checkout...')

            number = profile["card"]["cardNumber"]
            if str(number[0]) == "3":
                cType = 'amex'
            if str(number[0]) == "4":
                cType = 'visa'
            if str(number[0]) == "5":
                cType = 'mastercard'
    
    
            encryptedInfo = ClientSideEncrypter("10001|A56EE633C9798A4A8908E08338C183038DCD607260FC3E6ECA8466C567053D30932A7DA147906B29CC9C0070F4FD42FB5A4F0C9AAE36123C5662B13A55AB2ED9519E0ED470D71F48669999FD6107C90B9075E4A4DAC76BE804A4BE1252A69D138DC0BB1BAC3B4CF4760D39267E4879F94D0AF1EE373133BF2F1DAC39B8BC9F64DF4A0D05BFCFB64CF511B7064465AB08D7EE145F9163BD46A2159BD17F6305E2F57515027C63D4193C56A33F4779CCA723C0B48D4996AC6B2EF1DC6A203D0EFF1765B298D42C5E98A7F8E01BFF67CFD10685EC406B52FE6BD2FD7E635DB1D0F7D06ECEB052BE5CF0CD6318E7A4B23B6BCED51C86090ECFE55EAF14398C04622B", "_0_1_25")
            encryptedCardNum = str(encryptedInfo.generate_adyen_nonce(profile["firstName"] + " " + profile["lastName"], profile["card"]["cardNumber"], '', '', '').replace("b'", "").replace("'", ""))
            encryptedExpMonth = str(encryptedInfo.generate_adyen_nonce(profile["firstName"] + " " + profile["lastName"], '', '', profile["card"]["cardMonth"], '').replace("b'", "").replace("'", ""))
            encryptedExpYear = str(encryptedInfo.generate_adyen_nonce(profile["firstName"] + " " + profile["lastName"], '', '', '', profile["card"]["cardYear"]).replace("b'", "").replace("'", ""))
            encryptedCVV = str(encryptedInfo.generate_adyen_nonce(profile["firstName"] + " " + profile["lastName"], '', profile["card"]["cardCVV"], '', '').replace("b'", "").replace("'", ""))

            data = {
                "orderNumber": self.orderNumber,
                "orderTotal": self.orderTotal,
                "paymentMethodObj": {
                    "type": "scheme",
                    "holderName": profile['firstName'] + ' ' + profile['lastName'],
                    "encryptedCardNumber": encryptedCardNum,
                    "encryptedExpiryMonth": encryptedExpMonth,
                    "encryptedExpiryYear": encryptedExpYear,
                    "encryptedSecurityCode": encryptedCVV,
                    "bi": {
                        "acceptHeader": "",
                        "colorDepth": 24,
                        "javaScriptEnabled": True,
                        "javaEnabled": False,
                        "language": "en-US",
                        "screenHeight": 960,
                        "screenWidth": 1536,
                        "timeZoneOffset": -60,
                        "userAgent": ""
                    }
                },
                "strPaymentPage": "billing"
            }

            try:
                paymentDropIn = self.session.post(f'{self.baseURL}/CheckoutService/AdyenCreatePaymentDropIn',json=data,headers={
                    'Accept':'application/json, text/javascript, */*; q=0.01n',
                    'referer':f'{self.baseURL}/billing.aspx',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.cardPayment()

            response = json.loads(paymentDropIn.json()['d'].split('|')[1].replace(' ','').replace('\n',''))


        
        else:
            logger.error(SITE,self.taskID,'Failed to set payment method. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.cardPayment()



        
    