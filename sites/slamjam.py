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

from utils.logger import logger
from utils.webhook import discord
from utils.log import log
from utils.datadome import datadome
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies, updateConsoleTitle, scraper)
SITE = 'SLAMJAM'



class SLAMJAM:
    def __init__(self, task,taskName):
        self.task = task
        self.sess = requests.session()
        self.taskID = taskName

        twoCap = loadSettings()["2Captcha"]
        self.session = scraper()
        self.session.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "dnt": "1",
            "pragma": "no-cache",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        }
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        self.region = profile["countryCode"].upper()

        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)


        self.collect()

    def collect(self):
        logger.prepare(SITE,self.taskID,'Getting product page...')
        if 'https' in self.task["PRODUCT"]:
            self.url = self.task["PRODUCT"]
        else:
            self.url = 'https://www.slamjam.com/en_{}/{}.html'.format(self.region,self.task["PRODUCT"])
        
        try:
            retrieve = self.session.get(self.url,timeout=10)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.collect()

        self.start = time.time()
        regex = r"[A-Z](\d+).html"
        matches = re.search(regex, retrieve.url)
        if matches:
            self.pid = matches.group().split('.html')[0]
        else:
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.collect()
        
    
        self.cookie = loadCookie('SLAMJAM')["cookie"]
        if self.cookie == 'empty':
            del self.session.cookies["datadome"]
            self.cookie = datadome.slamjam(self.session.proxies, self.taskID, 'return')
            self.session.cookies["datadome"]  = self.cookie
        else:
            del self.session.cookies["datadome"]
            self.session.cookies["datadome"]  = self.cookie
            self.session.proxies = self.cookie["proxy"]


        if retrieve.status_code == 200:
            
            self.redirectUrl = retrieve.url
            logger.success(SITE,self.taskID,'Got product page')
            try:
                soup = BeautifulSoup(retrieve.text, "html.parser")
                #self.pid = retrieve.text.split("criteoProductsArray.push('")[1].split("');")[0]
                self.csrf = soup.find('input',{'name':'csrf_token'})['value']
                categorys = soup.find_all("li",{"class":"breadcrumb-item"})[3]
                aCategorys = categorys.find('a')
                self.productCategory = aCategorys.find('span').text
                self.queryString = f'https://www.slamjam.com/on/demandware.store/Sites-slamjam-Site/en_{self.region}/Product-Variation?pid={self.pid}'
                        
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to scrape page (Most likely out of stock). Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.collect()

            self.retrieve()

        else:
            try:
                status = retrieve.status_code
            except:
                status = 'Unknown'
            logger.error(SITE,self.taskID,f'Failed to get product page => {status}. Retrying...')
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.collect()


    def retrieve(self):
        logger.warning(SITE,self.taskID,'Gathering product info...')
        try:
            data = self.session.get(self.queryString)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.collect()
        
        print(data)
        if data:
            if 'DDUser' in data.url:
                logger.info(SITE,self.taskID,'Challenge Found, Solving...')
                self.cookie = loadCookie('SLAMJAM')["cookie"]
                if self.cookie == 'empty':
                    del self.session.cookies["datadome"]
                    self.cookie = datadome.slamjam(self.session.proxies, self.taskID, 'return')
                    self.session.cookies["datadome"]  = self.cookie
                else:
                    del self.session.cookies["datadome"]
                    self.session.cookies["datadome"]  = self.cookie
                    self.session.proxies = self.cookie["proxy"]

                self.retrieve()
            else:
                if data.status_code == 200:
                    try:
                        data = data.json()
                    except:
                        logger.error(SITE,self.taskID,'Failed to retrieve product info. Retrying...')
                        time.sleep(int(self.task["DELAY"]))
                        self.collect()

                    print(data)
    
                    self.uuid = data["product"]["uuid"]
                    self.productTitle = data["product"]["productName"]
                    self.productPrice = data["product"]["price"]["sales"]["formatted"]
                    self.productImage = data["product"]["images"]["hi-res"][0]["absURL"]
    
                    sizeData = data["product"]["variationAttributes"][1]["values"]
    
                    allSizes = []
                    sizes = []
                    for s in sizeData:
                        # SIZE : SIZE ID : SIZE PRODUCT ID : IN STOCK (TRUE / FALSE )
                        if s["selectable"] == True:
                            allSizes.append('{}:{}:{}:{}'.format(s["displayValue"],s["id"],s["productID"],s["selectable"]))
                            sizes.append(s["displayValue"])
    
    
                    if len(sizes) == 0:
                        logger.error(SITE,self.taskID,'Size Not Found')
                        time.sleep(int(self.task["DELAY"]))
                        self.retrieve()
    
                        
                    if self.task["SIZE"].lower() != "random":
                        if self.task["SIZE"] not in sizes:
                            logger.error(SITE,self.taskID,'Size Not Found')
                            time.sleep(int(self.task["DELAY"]))
                            self.retrieve()
                        else:
                            for size in allSizes:
                                if size.split(':')[0] == self.task["SIZE"]:
                                    self.size = size.split(':')[0]
                                    self.sizeID = size.split(':')[1]
                                    self.sizeProductID = size.split(":")[2]
                                    logger.success(SITE,self.taskID,f'Found Size => {self.size}')
                                    self.addToCart()
        
                    
                    elif self.task["SIZE"].lower() == "random":
                        selected = random.choice(allSizes)
                        self.size = selected.split(':')[0]
                        self.sizeProductID = selected.split(":")[2]
                        self.sizeID = selected.split(':')[1]
                        logger.success(SITE,self.taskID,f'Found Size => {self.size}')
                        self.addToCart()

        else:
            logger.error(SITE,self.taskID,'Failed to get product info.')
            time.sleep(int(self.task["DELAY"]))
            self.retrieve()



    def addToCart(self):
        del self.session.cookies["datadome"]
        self.session.cookies["datadome"]  = self.cookie
        logger.prepare(SITE,self.taskID,'Carting Product...')
        self.session.headers = {}
        self.session.headers = {
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.slamjam.com',
            'referer': self.redirectUrl,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        cartPayload = {
            'pid': self.sizeProductID,
            'quantity': 1,
            'category': self.productCategory,
            'viewFrom': 'si',
            'options': []
        }
        try:
            cart = self.session.post(f'https://www.slamjam.com/on/demandware.store/Sites-slamjam-Site/en_{self.region}/Cart-AddProduct',data=cartPayload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

        if cart:
            if 'DDUser' in cart.url:
                logger.info(SITE,self.taskID,'Challenge Found, Solving...')
                self.cookie = loadCookie('SLAMJAM')["cookie"]
                if self.cookie == 'empty':
                    del self.session.cookies["datadome"]
                    self.cookie = datadome.slamjam(self.session.proxies, self.taskID, 'return')
                    self.session.cookies["datadome"]  = self.cookie
                else:
                    del self.session.cookies["datadome"]
                    self.session.cookies["datadome"]  = self.cookie
                    self.session.proxies = self.cookie["proxy"]
                self.addToCart()
            else:    
                try:
                    cart.json()
                except:
                    logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.collect()
        
                if cart.status_code == 200 and int(cart.json()["quantityTotal"]) > 0:
                    updateConsoleTitle(True,False,SITE)
                    logger.success(SITE,self.taskID,'Successfully Carted Product!')
                    self.shipping()
                else:
                    logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.addToCart()

    def shipping(self):
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        logger.prepare(SITE,self.taskID,'Getting checkout page...')
        self.session.headers = {}
        self.session.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9',
            'referer': f'https://www.slamjam.com/en_{self.region}/checkout',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
        }

        try:
            shipping = self.session.get(f'https://www.slamjam.com/en_{self.region}/checkout-begin?stage=shipping#shipping')
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.shipping()

        if shipping:
            if 'DDUser' in shipping.url:
                logger.info(SITE,self.taskID,'Challenge Found, Solving...')
                self.cookie = loadCookie('SLAMJAM')["cookie"]
                if self.cookie == 'empty':
                    del self.session.cookies["datadome"]
                    self.cookie = datadome.slamjam(self.session.proxies, self.taskID, 'return')
                    self.session.cookies["datadome"]  = self.cookie
                else:
                    del self.session.cookies["datadome"]
                    self.session.cookies["datadome"]  = self.cookie
                    self.session.proxies = self.cookie["proxy"]

                self.shipping()
            else:
                if shipping.status_code == 200:
                    soup = BeautifulSoup(shipping.text,"html.parser")
                    # try:
                    self.shipmentUUID = soup.find("input",{"name":"shipmentUUID"})["value"]
                    self.csrfToken = soup.find("input",{"name":"csrf_token"})["value"]
                    
                    states = soup.find("select",{"name":"dwfrm_shipping_shippingAddress_addressFields_states_stateCode"})
                    for s in states:
                        try:
                            if s.text.lower() == profile["region"].lower():
                                self.stateID = s["id"]
                        except:
                            pass
                    # except Exception as e:
                        # log.info(e)
                        # logger.error(SITE,self.taskID,'Failed to get shipping page. Retrying...')
                        # time.sleep(int(self.task["DELAY"]))
                        # self.shipping()
                else:
                    logger.error(SITE,self.taskID,'Failed to get shipping page. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.shipping()
    
        else:
            logger.error(SITE,self.taskID,'Failed to get shipping page. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.shipping()

        self.session.headers = {}
        self.session.headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.slamjam.com',
            'referer': 'https://www.slamjam.com/en_GB/checkout-begin?stage=shipping',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        
        payload = {
            'firstName': profile["firstName"],
            'lastName': profile["lastName"],
            'address1': profile["house"] + " " + profile["addressOne"],
            'address2': profile["addressTwo"],
            'city': profile["city"],
            'postalCode': profile["zip"],
            'stateCode': self.stateID,
            'countryCode': profile["countryCode"],
            'phone': '',
            'shipmentUUID': self.shipmentUUID,
            'idAddress': 'new'
        }
        logger.prepare(SITE,self.taskID,'Retrieving shipping rates')
        try:
            shippingMethods = self.session.post(f'https://www.slamjam.com/on/demandware.store/Sites-slamjam-Site/en_{self.region}/CheckoutShippingServices-UpdateShippingMethodsList',data=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.shipping()
        
        if shippingMethods:
            if 'DDUser' in shippingMethods.url:
                logger.info(SITE,self.taskID,'Challenge Found, Solving...')
                self.cookie = loadCookie('SLAMJAM')["cookie"]
                if self.cookie == 'empty':
                    del self.session.cookies["datadome"]
                    self.cookie = datadome.slamjam(self.session.proxies, self.taskID, 'return')
                    self.session.cookies["datadome"]  = self.cookie
                else:
                    del self.session.cookies["datadome"]
                    self.session.cookies["datadome"]  = self.cookie
                    self.session.proxies = self.cookie["proxy"]

                self.shipping()
            else:

                if shippingMethods.status_code == 200:
                    try:
                        self.shippingMethodId = shippingMethods.json()["order"]["shipping"][0]["applicableShippingMethods"][0]["ID"]
                    except Exception as e:
                        log.info(e)
                        logger.error(SITE,self.taskID,'Failed to get shipping methods. Retrying...')
                        time.sleep(int(self.task["DELAY"]))
                        self.shipping()
                else:
                    logger.error(SITE,self.taskID,'Failed to get shipping methods. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.shipping()

        else:
            logger.error(SITE,self.taskID,'Failed to get shipping methods. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.shipping()

        payload = {
            'originalShipmentUUID': self.csrfToken,
            'shipmentUUID': self.shipmentUUID,
            'shipmentSelector': 'new',
            'dwfrm_shipping_shippingAddress_addressFields_firstName': profile["firstName"],
            'dwfrm_shipping_shippingAddress_addressFields_lastName': profile["lastName"],
            'dwfrm_shipping_shippingAddress_addressFields_states_country': profile["countryCode"],
            'dwfrm_shipping_shippingAddress_addressFields_states_stateCode': self.stateID,
            'dwfrm_shipping_shippingAddress_addressFields_city': profile["city"],
            'dwfrm_shipping_shippingAddress_addressFields_states_postalCode': profile["zip"],
            'dwfrm_shipping_shippingAddress_addressFields_address1': profile["house"] + " " + profile["addressOne"],
            'dwfrm_shipping_shippingAddress_addressFields_address2': profile["addressTwo"],
            'dwfrm_shipping_shippingAddress_addressFields_prefix': profile["phonePrefix"],
            'dwfrm_shipping_shippingAddress_addressFields_phone': profile["phone"],
            'dwfrm_shipping_shippingAddress_shippingMethodID': self.shippingMethodId,
            'csrf_token': self.csrfToken,
        }
        logger.prepare(SITE,self.taskID,'Posting shipping details...')
        try:
            shipping = self.session.post(f'https://www.slamjam.com/on/demandware.store/Sites-slamjam-Site/en_{self.region}/CheckoutShippingServices-SubmitShipping',data=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()
        
        try:
            data = shipping.json()
        except:
            logger.error(SITE,self.taskID,'Failed to post shipping details. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.shipping()
        
        if shipping:
            if 'DDUser' in shipping.url:
                logger.info(SITE,self.taskID,'Challenge Found, Solving...')
                self.cookie = loadCookie('SLAMJAM')["cookie"]
                if self.cookie == 'empty':
                    del self.session.cookies["datadome"]
                    self.cookie = datadome.slamjam(self.session.proxies, self.taskID, 'return')
                    self.session.cookies["datadome"]  = self.cookie
                else:
                    del self.session.cookies["datadome"]
                    self.session.cookies["datadome"]  = self.cookie
                    self.session.proxies = self.cookie["proxy"]

                self.shipping()
            else:
                if shipping.status_code == 200 and data:
                    logger.success(SITE,self.taskID,'Successfully posted shipping details')
                    self.PayPalpayment()
                else:
                    logger.error(SITE,self.taskID,'Failed to post shipping details. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.shipping()


    def PayPalpayment(self):
        logger.warning(SITE,self.taskID,'Submitting payment...')
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        payload = {
            'addressSelector': self.shipmentUUID,
            'dwfrm_billing_addressFields_firstName': profile["firstName"],
            'dwfrm_billing_addressFields_lastName': profile["lastName"],
            'dwfrm_billing_addressFields_states_country': profile["countryCode"],
            'dwfrm_billing_addressFields_states_stateCode': self.stateID,
            'dwfrm_billing_addressFields_city': profile["city"],
            'dwfrm_billing_addressFields_states_postalCode': profile["zip"],
            'dwfrm_billing_addressFields_address1': profile["house"] + " " + profile["addressOne"],
            'dwfrm_billing_addressFields_address2': profile["addressTwo"],
            'dwfrm_billing_paymentMethod': 'PayPal',
            'dwfrm_billing_creditCardFields_email': profile["email"],
            'dwfrm_billing_privacy': 'true',
            'isPaypal': 'true',
            'dwfrm_billing_paymentMethod': 'PayPal',
            'dwfrm_billing_paymentMethod': 'CREDIT_CARD',
            'dwfrm_billing_creditCardFields_cardType': '',
            'dwfrm_billing_creditCardFields_adyenEncryptedData': '',
            'dwfrm_billing_creditCardFields_selectedCardID': '',
            'dwfrm_billing_creditCardFields_cardNumber': '',
            'dwfrm_billing_creditCardFields_expirationMonth': '',
            'dwfrm_billing_creditCardFields_expirationYear': '',
            'csrf_token': self.csrfToken
        }

        try:
            payment = self.session.post(f'https://www.slamjam.com/on/demandware.store/Sites-slamjam-Site/en_{self.region}/CheckoutServices-SubmitPayment',data=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.PayPalpayment()
        if payment:
            if 'DDUser' in payment.url:
                logger.info(SITE,self.taskID,'Challenge Found, Solving...')
                self.cookie = loadCookie('SLAMJAM')["cookie"]
                if self.cookie == 'empty':
                    del self.session.cookies["datadome"]
                    self.cookie = datadome.slamjam(self.session.proxies, self.taskID, 'return')
                    self.session.cookies["datadome"]  = self.cookie
                else:
                    del self.session.cookies["datadome"]
                    self.session.cookies["datadome"]  = self.cookie
                    self.session.proxies = self.cookie["proxy"]
                    
                self.PayPalpayment()
            else:
                try:
                    data = payment.json()
                except:
                    logger.error(SITE,self.taskID,'Failed to submit payment. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.PayPalpayment()
        
                if payment.status_code == 200 and data:
                    self.end = time.time() - self.start
                    logger.success(SITE,self.taskID,'Successfully submitted payment')
                    
                    try:
                        self.paypalToken = data["paypalProcessorResult"]["paypalToken"]
                    except:
                        logger.error(SITE,self.taskID,'Failed to submit payments. Retrying...')
                        time.sleep(int(self.task["DELAY"]))
                        self.PayPalpayment()
        
                    paypalURL = 'https://www.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token={}&useraction=commit'.format(self.paypalToken)
                    logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')
                    updateConsoleTitle(False,True,SITE)
                    
                    url = storeCookies(paypalURL,self.session)
            
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
                        logger.secondary(SITE,self.taskID,'Failed to send webhook. Checkout here ==> {}'.format(url))
                    
                else:
                    logger.error(SITE,self.taskID,'Failed to submit payment. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.PayPalpayment()

    def ccPayment(self):
        logger.warning(SITE,self.taskID,'Submitting payment...')
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        firstNumber = profile["card"]["cardNumber"]
        if firstNumber == "3":
            CARD_TYPE = 'American Express'
        if firstNumber == "4":
            CARD_TYPE = 'Visa'
        if firstNumber == "5":
            CARD_TYPE = 'Master Card'
        if firstNumber == "6":
            CARD_TYPE = 'Discover Card'

        LAST_4_CARD = profile["card"]["cardNumber"][-4:]
        payload = {
            'addressSelector': self.shipmentUUID,
            'dwfrm_billing_addressFields_firstName': profile["firstName"],
            'dwfrm_billing_addressFields_lastName': profile["lastName"],
            'dwfrm_billing_addressFields_states_country': profile["countryCode"],
            'dwfrm_billing_addressFields_states_stateCode': self.stateID,
            'dwfrm_billing_addressFields_city': profile["city"],
            'dwfrm_billing_addressFields_states_postalCode': profile["zip"],
            'dwfrm_billing_addressFields_address1': profile["house"] + " " + profile["addressOne"],
            'dwfrm_billing_addressFields_address2': profile["addressTwo"],
            'dwfrm_billing_paymentMethod': 'CREDIT_CARD',
            'dwfrm_billing_creditCardFields_email': profile["email"],
            'dwfrm_billing_privacy': 'true',
            'dwfrm_billing_paymentMethod': 'CREDIT_CARD',
            'dwfrm_billing_creditCardFields_cardType': CARD_TYPE,
            'dwfrm_billing_creditCardFields_adyenEncryptedData': '',
            'dwfrm_billing_creditCardFields_selectedCardID': '',
            'dwfrm_billing_creditCardFields_cardNumber': f'************{LAST_4_CARD}',
            'dwfrm_billing_creditCardFields_expirationMonth': profile["card"]["cardMonth"],
            'dwfrm_billing_creditCardFields_expirationYear': profile["card"]["cardYear"],
            'csrf_token': self.csrfToken
        }
        try:
            payment = self.session.post(f'https://www.slamjam.com/on/demandware.store/Sites-slamjam-Site/en_{self.region}/CheckoutServices-SubmitPayment',data=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.ccPayment()


        

  