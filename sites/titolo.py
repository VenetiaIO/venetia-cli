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
import cloudscraper
SITE = 'TITOLO'

from utils.logger import logger
from utils.captcha import captcha
from utils.webhook import discord
from utils.log import log
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies)


class TITOLO:
    def __init__(self,task,taskName):
        self.task = task
        self.sess = requests.session()
        self.taskID = taskName

        twoCap = loadSettings()["2Captcha"]
        self.session = cloudscraper.create_scraper(
            requestPostHook=injection,
            sess=self.sess,
            interpreter='nodejs',
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
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }

        self.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
        self.session.proxies = self.proxies


        self.collect()

    def collect(self):
        try:
            retrieve = self.session.get(self.task["PRODUCT"],headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.collect()

        if retrieve.status_code == 200:
            logger.success(SITE,self.taskID,'Got product page')
            try:
                split = self.task["PRODUCT"].split("titoloshop.")[1]
                self.region = split.split('/')[0]
                self.baseSite = 'https://en.titoloshop.com'
            except:
                split = self.task["PRODUCT"].split("titolo.")[1]
                self.region = split.split('/')[0]
                self.baseSite = 'https://en.titolo.ch'
            try:

                soup = BeautifulSoup(retrieve.text,"html.parser")
                self.productTitle = soup.find("img",{"id":"image"})["title"]
                self.productImage = soup.find("img",{"id":"image"})["src"]
                self.productPrice = soup.find("span",{"class":"price"}).text
                self.atcUrl = soup.find("form", {"id": "product_addtocart_form"})["action"].replace(',',',,')
                self.formKey = soup.find("input", {"name": "form_key"})["value"]
                self.productId = soup.find("input", {"name": "product"})["value"]
                self.attributeIdColor = soup.find_all("select", {"class": "required-entry super-attribute-select"})[0]["id"].split("attribute")[1]
                self.attributeId = soup.find_all("select", {"class": "required-entry super-attribute-select"})[1]["id"].split("attribute")[1]
                sizeSelect = soup.find("select",{"id":"attributesize-size_eu"})
    
                regex = r"{\"attributes\":(.*?)}}\)"
                matches = re.search(regex, retrieve.text, re.MULTILINE)
                if matches:
                    productData = json.loads(
                        matches.group()[:-1])["attributes"][self.attributeIdColor]
                    self.color = productData["options"][0]["id"]
    
                allSizes = []
                sizes = []
                for s in sizeSelect:
                    try:
                        allSizes.append('{}:{}:{}'.format(s.text,s["value"],s["source"]))
                        sizes.append(s.text)
                    except:
                        pass
    
                if len(sizes) == 0:
                    logger.error(SITE,self.taskID,'Size Not Found')
                    time.sleep(int(self.task["DELAY"]))
                    self.collect()
    
                if self.task["SIZE"].lower() == "random":
                    chosen = random.choice(allSizes)
                    self.sizeValue = chosen.split(':')[1]
                    self.size = chosen.split(':')[0]
                    self.sizeAttributeId = chosen.split(':')[2]
                    logger.success(SITE,self.taskID,f'Found Size => {self.size}')
                
        
    
                else:
                    if self.task["SIZE"] not in sizes:
                        logger.error(SITE,self.taskID,'Size Not Found')
                        time.sleep(int(self.task["DELAY"]))
                        self.collect()
                    for size in allSizes:
                        if self.task["SIZE"] == size.split(':')[0]:
                            self.sizeValue = chosen.split(':')[1]
                            self.size = chosen.split(':')[0]
                            self.sizeAttributeId = chosen.split(':')[2]
                            logger.success(SITE,self.taskID,f'Found Size => {self.size}')



            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to scrape page (Most likely out of stock). Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.collect()

            self.addToCart()
        else:
            try:
                status = retrieve.status_code
            except:
                status = 'Unknown'
            logger.error(SITE,self.taskID,f'Failed to get product page => {status}. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.collect()

    def addToCart(self):
        captchaResponse = loadToken(SITE)
        if captchaResponse == "empty":
            captchaResponse = captcha.v2('6Ldpi-gUAAAAANpo2mKVvIR6u8nUGrInKKik8MME',self.task["PRODUCT"],self.proxies,SITE,self.taskID)
    
        payload = {
            'product': self.productId,
            'related_product': '',
            'standard_attribute[size]': 'size_us',
            f'super_attribute[{self.attributeIdColor}]': self.color,
            f'super_attribute[{self.attributeId}]': self.sizeAttributeId,
            'size_attribute[size]': self.sizeValue,
            'return_url': '',
            'g-recaptcha-response': captchaResponse,
            'amasty_invisible_token': captchaResponse
        }
        try:
            postCart = self.session.post(self.atcUrl,data=payload,headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()

        if postCart.status_code == 200 and "/checkout/cart/" in postCart.url:
            logger.success(SITE,self.taskID,'Successfully carted')
            self.method()
        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

    def method(self):
        try:
            setMethod = self.session.post(f'{self.baseSite}/checkout/onepage/saveMethod/',data={"method": "guest"},headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'accept': 'text/javascript, text/html, application/xml, text/xml, */*',
            })
            setMethod = self.session.post(f'{self.baseSite}/checkout/onepage/saveMethod/',data={"method": "guest"},headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'accept': 'text/javascript, text/html, application/xml, text/xml, */*',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.method()

        if setMethod.status_code == 200 and setMethod.json() == []:
            logger.success(SITE,self.taskID,'Saved Method')
            self.billing()
        else:
            logger.error(SITE,self.taskID,'Failed to save method. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.method()



    def billing(self):
        profile = loadProfile(self.task["PROFILE"])
        countryCode = profile["countryCode"]

        payload = {
            'billing[address_id]': '',
            'billing[firstname]': profile["firstName"],
            'billing[lastname]': profile["lastName"],
            'billing[company]': '',
            'billing[email]': profile["email"],
            'billing[street][]': profile["house"] + " " + profile["addressOne"],
            'billing[city]': profile["city"],
            'billing[region_id]': '',
            'billing[region]': profile["region"],
            'billing[postcode]': profile["zip"],
            'billing[country_id]': countryCode,
            'billing[telephone]': profile["phone"],
            'billing[fax]': '',
            'billing[customer_password]': '',
            'billing[confirm_password]': '',
            'billing[save_in_address_book]': '1',
            'billing[use_for_shipping]': '1',
            'form_key': self.formKey
        }

        try:
            postBilling = self.session.post(f'{self.baseSite}/checkout/onepage/saveBilling/',data=payload,headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'accept': 'text/javascript, text/html, application/xml, text/xml, */*'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.billing()

        if postBilling.status_code == 200:
            if postBilling.text:
                shippingOptions = json.loads(postBilling.text)
                shippingHtml = shippingOptions["update_section"]["html"]
                soup = BeautifulSoup(shippingHtml,"html.parser")
                self.shippingMethods = soup.find_all('input',{'name':'shipping_method'})
                logger.success(SITE,self.taskID,'Successfully set shipping')
                self.shippingMethod()
            else:
                logger.error(SITE,self.taskID,'Failed to set shipping. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.collect()
        elif postBilling.status_code != 200:
            logger.error(SITE,self.taskID,'Failed to set shipping. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.billing()

    def shippingMethod(self):
        try:
            setShippingMethod = self.session.post(f'{self.baseSite}/SaferpayCw/onepage/saveShippingMethod/',data={"shipping_method": self.shippingMethods[0]["value"],"form_key":self.formKey},headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'accept': 'text/javascript, text/html, application/xml, text/xml, */*'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.shippingMethod()

        if setShippingMethod.status_code == 200:
            logger.success(SITE,self.taskID,'Successfully set shipping method')
            if self.task["PAYMENT"].lower() == "paypal":
                self.paypal()
            if self.task["PAYMENT"].lower() == "mastercard":
                self.paymentMethod = 'saferpaycw_mastercard'
                self.card()
            if self.task["PAYMENT"].lower() == "visa":
                self.paymentMethod = 'saferpaycw_visa'
                self.card()
            elif self.task["PAYMENT"].lower() not in ["paypal","mastercard","visa"]:
                self.paypal()
 
        else:
            logger.error(SITE,self.taskID,'Failed to set shipping method')
            time.sleep(int(self.task["DELAY"]))
            self.shippingMethod()


    def paypal(self):
        logger.info(SITE,self.taskID,'Starting [PAYPAL] checkout...')
        try:
            setPayment = self.session.post(f'{self.baseSite}/checkout/onepage/savePayment/',data={"payment[method]": "paypal_express","form_key":self.formKey},headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'accept': 'text/javascript, text/html, application/xml, text/xml, */*'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.paypal()

        if setPayment.status_code == 200:
            logger.success(SITE,self.taskID,'Successfully set payment')
            try:
                getPaypal = self.session.get(f'{self.baseSite}/paypal/express/start/',headers={
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.paypal()

    
            if "paypal" in getPaypal.url:
                logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')
                url = storeCookies(getPaypal.url,self.session)
                
                sendNotification(SITE,self.productTitle)
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
                while True:
                    pass
            elif "paypal" not in getPaypal.url:
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
                )
                logger.error(SITE,self.taskID,'Failed to get PayPal checkout link. Retrying...')
                self.paypal()
            
        else:
            logger.error(SITE,self.taskID,'Failed to set payment. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.shippingMethod()


    def card(self):
        logger.info(SITE,self.taskID,'Starting [CARD] checkout...')
        try:
            savePayment = self.session.post(f'{self.baseSite}/checkout/onepage/savePayment/',data={"payment[method]": self.paymentMethod,"form_key":self.formKey},headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
            'accept': 'text/javascript, text/html, application/xml, text/xml, */*'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.card()

        if savePayment.status_code == 200:
            logger.success(SITE,self.taskID,'Successfully set payment')
            self.placeOrder()  
        elif savePayment.status_code != 200:
            logger.error(SITE,self.taskID,'Failed to set payment. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.card()

    def placeOrder(self):
        captchaResponse = loadToken(SITE)
        if captchaResponse == "empty":
            captchaResponse = captcha.v2('6Ldpi-gUAAAAANpo2mKVvIR6u8nUGrInKKik8MME',self.task["PRODUCT"],self.proxies,SITE,self.taskID)
            
        payload = {
            'payment[method]': self.paymentMethod,
            'form_key': self.formKey,
            'agreement[1]': 1,
            'agreement[3]': 1,
            'g-recaptcha-response': captchaResponse,
            'amasty_invisible_token': captchaResponse
        }

        try:
            saveOrder = self.session.post(f'{self.baseSite}/checkout/onepage/saveOrder/form_key/{self.formKey}',data=payload,headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'accept': 'text/javascript, text/html, application/xml, text/xml, */*',
                'content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'referer':f'{self.baseSite}/checkout/onepage/'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.placeOrder()


        try:
            json = saveOrder.json()
        except:
            logger.error(SITE,self.taskID,'Failed to retrieve SaferPay redirect. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.placeOrder()

        if saveOrder.json()["success"] == True:
            logger.success(SITE,self.taskID,'Successfully retrieved SaferPay redirect')
            self.ccRedirect = saveOrder.json()["redirect"]
#            
            profile = loadProfile(self.task["PROFILE"])
            getSaferPay = self.session.get(self.ccRedirect,headers={
                'authority': 'en.titoloshop.com',
                'method': 'GET',
                'scheme': 'https',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'referer':f'{self.baseSite}/checkout/onepage/',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            })
    
            cardPayload = {
                'CardNumber': profile["card"]["cardNumber"],
                'ExpMonth': profile["card"]["cardMonth"],
                'ExpYear':  profile["card"]["cardYear"],
                'HolderName': '{} {}'.format(profile["firstName"],profile["lastName"]),
                'VerificationCode':  profile["card"]["cardCVV"],
                'SubmitToNext': '',
            }
    
            submitCard = self.session.post(getSaferPay.url,data=cardPayload,headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            })

            
            if submitCard.status_code == 200:
                logger.alert(SITE,self.taskID,'Sending Card checkout to Discord!')
                url = storeCookies(submitCard.url,self.session)
    

                discord.success(
                    webhook=loadSettings()["webhook"],
                    site=SITE,
                    url=url,
                    image=self.productImage,
                    title=self.productTitle,
                    size=self.size,
                    price=self.productPrice,
                    paymentMethod=self.paymentMethod,
                    profile=self.task["PROFILE"],
                    product=self.task["PRODUCT"]
                )
                while True:
                    pass
            elif submitCard.status_code != 200:
                logger.error(SITE,self.taskID,'Error submitting card. Retrying...')
                discord.failed(
                    webhook=loadSettings()["webhook"],
                    site=SITE,
                    url=self.task["PRODUCT"],
                    image=self.productImage,
                    title=self.productTitle,
                    size=self.size,
                    price=self.productPrice,
                    paymentMethod=self.paymentMethod,
                    profile=self.task["PROFILE"],
                )
                time.sleep(int(self.task["DELAY"]))
                self.placeOrder()

        if saveOrder.json()["success"] == False:
            logger.error(SITE,self.taskID,'Failed to retrieve SaferPay redirect. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.placeOrder()
        
        else:
            logger.error(SITE,self.taskID,'Failed to retrieve SaferPay redirect. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.placeOrder()




    
        

