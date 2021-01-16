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
from utils.adyen import ClientSideEncrypter
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies, updateConsoleTitle, scraper)
SITE = 'PRO-DIRECT'

class PRODIRECT:
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
        self.session = scraper()
        self.taskID = taskName
        self.rowNumber = rowNumber
        
        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
        threading.Thread(target=self.task_checker,daemon=True).start()
        self.collect()

    def collect(self):
        logger.prepare(SITE,self.taskID,'Getting product page...')
        try:
            retrieve = self.session.get(self.task["PRODUCT"],headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
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
                self.productTitle = soup.find('title').text.replace('\n','').replace(' ','').replace('\r','')
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
                                    logger.warning(SITE,self.taskID,f'Found Size => {self.size}')
        
                    
                    elif self.task["SIZE"].lower() == "random":
                        chosen = random.choice(sizes)
                        self.size = chosen
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


            self.login()
        
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
            login = self.session.post('https://www.prodirectbasketball.com/accounts/MyAccount.aspx', data=payload, headers={
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'referer': 'https://www.prodirectbasketball.com/accounts/MyAccount.aspx',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.login()


        if login.status_code in [200,302,301]:
            logger.warning(SITE,self.taskID,'Successfully logged in')
            self.addToCart()
        else:
            logger.error(SITE,self.taskID,'Failed to login. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.login()

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
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()

        if postCart.status_code == 200 and 'successfully' in postCart.text:
            logger.warning(SITE,self.taskID,'Successfully carted')
            updateConsoleTitle(True,False,SITE)
            self.address()
        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            if self.task["SIZE"].lower() == "random":
                self.collect()
            else:
                self.addToCart()

    

    def address(self):
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        logger.prepare(SITE,self.taskID,'Submitting Address...')
        try:
            addy = self.session.get('https://www.prodirectbasketball.com/accounts/Checkout.aspx?ACC=ADDR',headers={
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'referer': 'https://www.prodirectbasketball.com/accounts/MyAccount.aspx?Return=Checkout',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.login()

        if addy.status_code == 200:
            try:
                soup = BeautifulSoup(addy.text,"html.parser")
                txtAddyID = soup.find('input',{'name':'txtAddressID'})['value']
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.address()
        
        
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
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.address()
    
            if postAddy.status_code in [200,302,301] and 'Checkout.aspx?ACC=PAYD' in postAddy.url:
                logger.warning(SITE,self.taskID,'Address submitted')
                self.pay()
            else:
                logger.error(SITE,self.taskID,'Failed to submit address (make sure you have an address linked to your account). Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.address()
        
        else:
            logger.error(SITE,self.taskID,'Failed to submit address. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.address()


    def pay(self):
        logger.prepare(SITE,self.taskID,'Getting payment data...')
        encryptedInfo = ClientSideEncrypter("10001|9D82A3F3F81509D2638BEB784DBD525FB3156EE4E0742E195E0DCB79354AC45FA5422E36B224EB082B63CF09F8355B7C28C3D1BB4C6E091CC07022CF6FB76194BD2B166B44452624AF7D770D6DD98CF9D1943979C342005A6F6016DB3CF192BD06E2A56AE46552647581B29A07D2A3E7AD32CEFE6FF03BFDEFB51419855BFD209343B60F963B8AEC00E68764B6471B8CDF66585BBCA31584BB35A7660C3B4D4862E7518C4369C5E1E176E3A9FEA76A641442DFA01707098A6E94AF847C1534F6E164427CFCEA92295327431D1B2256A222E4EDBAD7B86EC5931F5529A75977A07EDF441B581EF60C09357227AFAA234824B03AD411DFA1723F4441B5BCA29115", "_0_1_18")
        adyenEncrypted = str(encryptedInfo.generate_adyen_nonce("John Doe", 5555444433331111, 737, "06",  "2016").replace("b'", "").replace("'", ""))

        data = {
            'deliveryOptionInfo': 'STANDARD',
            'browserInfo': {"screenWidth":2560,"screenHeight":1440,"colorDepth":24,"userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36","timeZoneOffset":-60,"language":"en-US","javaEnabled":False},
            'paymentOption': 'paypal',
            'rbCard': 'newcard',
            'CardType': 'Adyen',
            'tbxIagree': 'agree',
            '__EVENTTARGET': 'fw100$btnGoToPayNow',
            'adyen-encrypted-data': adyenEncrypted
        }
        try:
            adyen = self.session.post('https://www.prodirectbasketball.com/accounts/Checkout.aspx?ACC=PAYD',data=data,headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'referer':'https://www.prodirectbasketball.com/accounts/Checkout.aspx?ACC=PAYD'
    
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.pay()


        if adyen.status_code in [200,302,301] and 'AlternatePaymentRedirect' in adyen.url:
            try:
                redirect = self.session.get('https://www.prodirectbasketball.com/accounts/AlternatePaymentRedirect.aspx',headers={
                    'authority': 'www.prodirectbasketball.com',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'accept-language': 'en-US,en;q=0.9',
                    'referer': 'https://www.prodirectbasketball.com/accounts/Checkout.aspx?ACC=PAYD',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
        
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.pay()
            if redirect:
                if redirect.status_code == 200:
                    try:
                        soup = BeautifulSoup(redirect.text,'html.parser')
                        self.payload = {
                            'countryCode': '',
                            'merchantAccount': 'ProDirectBasketball',
                            'merchantReference': soup.find('input',{'name':'merchantReference'})['value'],
                            'merchantSig': soup.find('input',{'name':'merchantSig'})['value'],
                            'brandCode': 'paypal',
                            'issuerId': '',
                            'recurringContract': soup.find('input',{'name':'recurringContract'})['value'],
                            'sessionValidity': soup.find('input',{'name':'sessionValidity'})['value'],
                            'shopperLocale': soup.find('input',{'name':'shopperLocale'})['value'],
                            'skinCode': soup.find('input',{'name':'skinCode'})['value'],
                            'paymentAmount': soup.find('input',{'name':'paymentAmount'})['value'],
                            'currencyCode': soup.find('input',{'name':'currencyCode'})['value'],
                            'shopperEmail': soup.find('input',{'name':'shopperEmail'})['value'],
                            'shopperReference': soup.find('input',{'name':'shopperReference'})['value'],
                            'shopper.firstName': soup.find('input',{'name':'shopper.firstName'})['value'],
                            'shopper.lastName': soup.find('input',{'name':'shopper.lastName'})['value'],
                            'billingAddress.houseNumberOrName': soup.find('input',{'name':'billingAddress.houseNumberOrName'})['value'],
                            'billingAddress.street': soup.find('input',{'name':'billingAddress.street'})['value'],
                            'billingAddress.city': soup.find('input',{'name':'billingAddress.city'})['value'],
                            'billingAddress.stateOrProvince': soup.find('input',{'name':'billingAddress.stateOrProvince'})['value'],
                            'billingAddress.country': soup.find('input',{'name':'billingAddress.country'})['value'],
                            'billingAddress.postalCode': soup.find('input',{'name':'billingAddress.postalCode'})['value'],
                            'deliveryAddress.houseNumberOrName': soup.find('input',{'name':'deliveryAddress.houseNumberOrName'})['value'],
                            'deliveryAddress.street': soup.find('input',{'name':'deliveryAddress.street'})['value'],
                            'deliveryAddress.city': soup.find('input',{'name':'deliveryAddress.city'})['value'],
                            'deliveryAddress.stateOrProvince': soup.find('input',{'name':'deliveryAddress.stateOrProvince'})['value'],
                            'deliveryAddress.country': soup.find('input',{'name':'deliveryAddress.country'})['value'],
                            'deliveryAddress.postalCode': soup.find('input',{'name':'deliveryAddress.postalCode'})['value']
                        }
                    except Exception as e:
                        log.info(e)
                        logger.error(SITE,self.taskID,'Failed to scrape payment details. Retrying...')
                        self.pay()

                    logger.warning(SITE,self.taskID,'Got payment data')
                    self.finish()
                else:
                    logger.error(SITE,self.taskID,'Failed to submit payment. Retrying...')
                    if self.task["SIZE"].lower() == "random":
                        self.collect()
                    else:
                        self.addToCart()

            else:
                logger.error(SITE,self.taskID,'Failed to submit payment. Retrying...')
                if self.task["SIZE"].lower() == "random":
                    self.collect()
                else:
                    self.addToCart()
        else:
            logger.error(SITE,self.taskID,'Failed to submit payment. Retrying...')
            if self.task["SIZE"].lower() == "random":
                self.collect()
            else:
                self.addToCart()

    def finish(self):
        logger.prepare(SITE,self.taskID,'Getting paypal link...')
        try:
            pp = self.session.post('https://live.adyen.com/hpp/skipDetails.shtml',data=self.payload,headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Referer':'https://www.prodirectbasketball.com/'
    
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.finish()

        if pp.status_code in [200,302] and 'paypal' in pp.url:
            logger.warning(SITE,self.taskID,'Got paypal link')
            self.end = time.time() - self.start
            logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')
            updateConsoleTitle(False,True,SITE)

            url = storeCookies(pp.url,self.session, self.productTitle, self.productImage, self.productPrice)
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
            except:
                logger.alert(SITE,self.taskID,'Failed to send webhook. Checkout here ==> {}'.format(url))

        else:
            logger.error(SITE,self.taskID,'Could not complete PayPal Checkout. Retrying...')
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
            time.sleep(int(self.task["DELAY"]))
            self.finish()

        
        




