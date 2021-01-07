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

SITE = 'FOOTASYLUM'

from utils.logger import logger
from utils.webhook import discord
from utils.log import log
from utils.captcha import captcha
from utils.akamai import AKAMAI
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification,storeCookies, updateConsoleTitle, encodeURIComponent, scraper)

class FOOTASYLUM:
    def __init__(self,task,taskName):
        self.task = task
        # self.session = requests.session()
        self.taskID = taskName
        self.session = scraper()

        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)


        self.collect()

    def collect(self):
        # cookies = AKAMAI.footasylum(self.session, self.taskID)
        # while cookies["_abck"] == "error":
            # cookies = AKAMAI.footasylum(self.session, self.taskID)
# 
# 
        # cookie_obj = requests.cookies.create_cookie(domain=f'.footasylum.com',name='_abck',value='9A0F5ABED3E05EF1B97621C1ABAC3F5E~0~YAAQHux7XD3GlrN2AQAADLMrxAU8KDJmNhLbKclnSr0RN/MEGcoNjpeW/dfPghn9xJ2w2wFOcvXCwdobJri75aA5WPVmWIvM0jri8yOTorxoKqbWQpO17+QUdzcVvJ9QX+Qjcm3A9+2yggb8ByWzNXQZw3+3CbH02Yw6NzeEbNZuyQgr1xT9DKEHhSijkxtDZUDe+LwEvwC1oiifHBMLBcrS3/IiWEvHvI4uigRWcpx1S7TgvGDGrPeLTpyItINZBLzJLO9y9DfK8oHI50VpwKRWW7/S5FODIdRVhqqD/SRrCdfQfW8Poo7a44B0nURyRP8ErilLkJsfaJm6Md/TVbIsD15G7h8oXwI=~-1~-1~-1')
        # self.session.cookies.set_cookie(cookie_obj)

        logger.prepare(SITE,self.taskID,'Getting product page...')
        try:
            retrieve = self.session.get(self.task["PRODUCT"],headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.collect()

        if retrieve.status_code == 200:
            self.start = time.time()
            logger.warning(SITE,self.taskID,'Got product page')
            logger.prepare(SITE,self.taskID,'Getting product data...')
            try:
                soup = BeautifulSoup(retrieve.text,"html.parser")
                pf_id = soup.find("input",{"name":"pf_id"})["value"]
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.collect()

            regex = r"variants = {(.+)}"
            matches = re.search(regex, retrieve.text, re.MULTILINE)
            if matches:
                productData = json.loads(matches.group().split('variants = ')[1].replace("'",'"'))
                pids = []
                sizes = []
                allSizes = []
                for s in productData:
                    pids.append(s)

                for s in pids:
                    p = productData[s]
                    if p["stock_status"] == "in stock":
                        if p["pf_id"] == pf_id:
                            size = p["option2"]
                            sku = p["sku"]
                            colour = p["option1"]
                            price = p["price"]
                            img = 'https://www.footasylum.com/images/products/medium/' + p["mob_swatch"]
                            name = p["name"]
    
                            sizes.append(size)
                            allSizes.append('{}#{}#{}#{}#{}#{}'.format(size,sku,colour,price,img,name))
                    else:
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
                            if size.split('#')[0] == self.task["SIZE"]:
                                self.size = size.split('#')[0]
                                self.sizeSku = size.split('#')[1]
                                self.sizeColour = size.split("#")[2]
                                self.productPrice = size.split("#")[3]
                                self.productImage = size.split("#")[4]
                                self.productTitle = size.split("#")[5]
                                logger.warning(SITE,self.taskID,f'Found Size => {self.size}')
                                self.login()
        
                    
                elif self.task["SIZE"].lower() == "random":
                    selected = random.choice(allSizes)
                    self.size = selected.split('#')[0]
                    self.sizeSku = selected.split('#')[1]
                    self.sizeColour = selected.split("#")[2]
                    self.productPrice = selected.split("#")[3]
                    self.productImage = selected.split("#")[4]
                    self.productTitle = selected.split("#")[5]
                    logger.warning(SITE,self.taskID,f'Found Size => {self.size}')
                    self.login()
            else:
                logger.error(SITE,self.taskID,'Sizes Not Found')
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
            
    def login(self):
        logger.prepare(SITE,self.taskID,'Logging In...')
        try:
            GETlogin = self.session.get('https://www.footasylum.com/page/login/',headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'x-xss-protection':'0'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.login()
        
        if GETlogin.status_code == 200:
            try:
                soup = BeautifulSoup(GETlogin.text,"html.parser")
                self.preLog = soup.find('input',{'name':'prelog'})["value"]
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to parse login page. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.login()
        else:
            logger.error(SITE,self.taskID,'Failed to get login page. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.login()


        payload = {
            'target': '',
            'targetar': '',
            'pf_id': '',
            'sku': '',
            'rdPassword': 'LOGIN',
            'prelog':self.preLog,
            'lookup_Validate': 1,
            'email2': self.task["ACCOUNT EMAIL"],
            'password': self.task["ACCOUNT PASSWORD"]
        }
        payload = "target=&targetar=&pf_id=&sku=&rdPassword=LOGIN&prelog={}&lookup_Validate=1&email2={}&password={}".format(
            self.preLog,
            self.task["ACCOUNT EMAIL"],
            self.task["ACCOUNT PASSWORD"]
        )

        try:
            login = self.session.post('https://www.footasylum.com/page/login/',data=payload,headers={
                'origin': 'https://www.footasylum.com',
                'referer': 'https://www.footasylum.com/page/login/',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded',
                'x-xss-protection':'0'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.login()

        if login.status_code == 200 and '?sessionid=' in login.url: 
            logger.warning(SITE,self.taskID,'Successfully logged in')
            self.sessionId = login.url.split('?sessionid=')[1]
            self.addToCart()
        
        else:
            logger.error(SITE,self.taskID,'Failed to login. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.login()




    def addToCart(self):
        logger.prepare(SITE,self.taskID,'Carting Products...')

        params = {
            "target":"ajx_basket.asp",
            "sku":self.sizeSku,
            "sessionid":self.sessionId,
            "_":time.time()
        }
        try:
            initCart = self.session.get('https://www.footasylum.com/page/xt_orderform_additem/',timeout=20,params=params,headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'accept': '*/*',
                'referer':'{}?sessionid={}'.format(self.task["PRODUCT"],self.sessionId),
                'authority': 'www.footasylum.com',
                'x-requested-with': 'XMLHttpRequest'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, TimeoutError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()

        if initCart.status_code in [200,302]:
            updateConsoleTitle(True,False,SITE)
            logger.warning(SITE,self.taskID,'Successfully carted')
            self.initiateCheckout()
        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

    
    def initiateCheckout(self):
        logger.prepare(SITE,self.taskID,'Initializing checkout...')
        try:
            initCheckout = self.session.post('https://www.footasylum.com/page/nw-api/initiatecheckout/?sessionid={}'.format(self.sessionId),headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'accept': 'text/plain, */*; q=0.01',
                'origin':'https://www.footasylum.com',
                'x-requested-with': 'XMLHttpRequest',
                'referer': 'https://www.footasylum.com/page/basket/' + self.sessionId
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.initiateCheckout()

        if initCheckout.text == '{"error":"1"}':
            logger.error(SITE,self.taskID,'Failed to initialize checkout. Retrying...')
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.collect()

        elif initCheckout.status_code == 200 and initCheckout.text != '{"error":"1"}':
            logger.warning(SITE,self.taskID,'Successfully Initialized checkout')
            self.checkoutSessionId = initCheckout.json()["checkoutSessionId"]
            self.basketId = initCheckout.json()["basket"]["id"]
            self.basketCustomerId = initCheckout.json()["basket"]["customerId"]

            logger.prepare(SITE,self.taskID,'Getting session info...')
            try:
                p = {
                    "orderNum":self.checkoutSessionId,
                    "refresh":True,
                    "medium":"web",
                    "apiKey":"lGJjE ccd0SiBdu3I6yByRp3/yY8uVIRFa9afLx 2YSrSwkWDfxq0YKUsh96/tP84CZO4phvoR 0y9wtm9Dh5w==",
                    "checkout_client":"secure"
                }
                paymentGateway = self.session.get('https://paymentgateway.checkout.footasylum.net/basket',params=p,headers={
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                    'accept': 'application/json',
                    'authority': 'paymentgateway.checkout.footasylum.net',
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.initiateCheckout()

            if paymentGateway.status_code == 200:
                self.customerId = paymentGateway.json()["basket"]["paraspar_customer_id"]
                self.currency = paymentGateway.json()["basket"]["currency_code"]
                self.pasparBasketId = paymentGateway.json()["basket"]["paraspar_id"]
                self.channelId = paymentGateway.json()["basket"]["channel_id"]
                self.fascia_id = paymentGateway.json()["basket"]["fascia_id"]
                self.parasparSessionId = paymentGateway.json()["basket"]["paraspar_session_id"]
                logger.warning(SITE,self.taskID,'Successfully retrieved session info')
                self.basketDetails()

            elif paymentGateway.status_code != 200:
                logger.error(SITE,self.taskID,'Failed to retrieved session info. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.initiateCheckout()
                

    def basketDetails(self):
        logger.prepare(SITE,self.taskID,'Getting customer info...')
        try:
            payload = {"fascia_id":self.fascia_id,"channel_id":self.channelId,"currency_code":self.currency,"customer":{"customer_id":self.customerId,"sessionID":self.parasparSessionId,"request_address":1,"request_basket":1}}
            details = self.session.post('https://r9udv3ar7g.execute-api.eu-west-2.amazonaws.com/prod/customer/details?checkout_client=secure',json=payload,headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'accept': 'application/json',
                'authority': 'r9udv3ar7g.execute-api.eu-west-2.amazonaws.com',
                'origin':'https://secure.footasylum.com',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'path': '/prod/customer/details?checkout_client=secure',
                'referer': 'https://secure.footasylum.com/?checkoutSessionId={}'.format(self.checkoutSessionId)
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.initiateCheckout()

        if details.status_code == 200:
            print(details.json())
            self.shippingDetails = details.json()["basket"]["shipping_details"]
            self.billingDetails = details.json()["basket"]["billing_details"]
            self.shippingMethodCode = details.json()["basket"]["shipping_method_code"]
            self.shippingMethodName = details.json()["basket"]["shipping_method_name"]
            self.shippingTotal = details.json()["basket"]["shipping_total"]
            self.authState = details.json()["customer"]["session_state"]
            logger.warning(SITE,self.taskID,'Successfully retrieved customer info')
            self.basketAddress()
        
        else:
            logger.error(SITE,self.taskID,'Failed to retrieve customer info')
            time.sleep(int(self.task["DELAY"]))
            self.initiateCheckout()

    def basketAddress(self):
        logger.prepare(SITE,self.taskID,'Submitting address...')
        payload = {
            "fascia_id":self.fascia_id,
            "channel_id":self.channelId,
            "currency_code":self.currency,
            "customer":{
                "customer_id":self.customerId,
                "sessionID":self.parasparSessionId
            },
            "basket":{
                "basket_id":self.pasparBasketId
            },
            "shipping_details":{
                "title":self.shippingDetails["title"],
                "firstname":self.shippingDetails["firstname"],
                "surname":self.shippingDetails["surname"],
                "address1":self.shippingDetails["address1"],
                "address2":self.shippingDetails["address2"],
                "town":self.shippingDetails["city"],
                "county":self.shippingDetails["county"],
                "postcode":self.shippingDetails["postcode"],
                "country_id":self.shippingDetails["country_id"],
                "country_name":self.shippingDetails["country_name"],
                "phone":self.shippingDetails["phone"],
                "mobile":self.shippingDetails["phone"]
            },
            "billing_details":{
                "title":self.billingDetails["title"],
                "firstname":self.billingDetails["firstname"],
                "surname":self.billingDetails["surname"],
                "address1":self.billingDetails["address1"],
                "address2":self.billingDetails["address2"],
                "town":self.billingDetails["city"],
                "county":self.billingDetails["county"],
                "postcode":self.billingDetails["postcode"],
                "country_id":self.billingDetails["country_id"],
                "country_name":self.billingDetails["country_name"],
                "phone":self.billingDetails["phone"],
                "mobile":self.billingDetails["phone"]
            }
        }
        try:
            address = self.session.post('https://r9udv3ar7g.execute-api.eu-west-2.amazonaws.com/prod/basket/basketaddaddress?checkout_client=secure',json=payload,headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'accept': 'application/json',
                'authority': 'r9udv3ar7g.execute-api.eu-west-2.amazonaws.com',
                'origin':'https://secure.footasylum.com',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'path':'/prod/basket/basketaddaddress?checkout_client=secure',
                'referer': 'https://secure.footasylum.com/?checkoutSessionId={}'.format(self.checkoutSessionId)
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.initiateCheckout()

        if address.status_code == 200:
            logger.warning(SITE,self.taskID,'Submitted address')
            self.productPrice = '{} {}'.format(address.json()["basket"]["total"],address.json()["basket"]["currency_code"])
            params = {"medium": "web","apiKey": "lGJjE ccd0SiBdu3I6yByRp3/yY8uVIRFa9afLx 2YSrSwkWDfxq0YKUsh96/tP84CZO4phvoR 0y9wtm9Dh5w==","checkout_client": "secure"}
            payload = {"basketId":self.pasparBasketId,"type":"shipping","shippingTotal":self.shippingTotal,"shippingCode":self.shippingMethodCode,"shippingCarrier":self.shippingMethodName}
            logger.prepare(SITE,self.taskID,'Submitting shipping method...')
            try:
                method = self.session.put('https://paymentgateway.checkout.footasylum.net/basket/shipping',params=params,json=payload,headers={
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                    'accept': 'application/json',
                    'authority': 'paymentgateway.checkout.footasylum.net',
                    'origin':'https://secure.footasylum.com',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'cross-site',
                    'referer': 'https://secure.footasylum.com/?checkoutSessionId={}'.format(self.checkoutSessionId)
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.basketAddress()

            if method.status_code == 200 and method.json()["status"] == "Success":
                logger.warning(SITE,self.taskID,'Successfully set shipping')

                payload = {
                    "cartId":self.pasparBasketId,
                    "customer":{
                        "firstname":address.json()["customer"]["firstname"],
                        "lastname":address.json()["customer"]["surname"],
                        "email":address.json()["customer"]["email"],
                        "mobile":address.json()["basket"]["shipping_details"]["phone"],
                        "title":address.json()["customer"]["title"],
                        "newsletter":1,
                        "sessionId":self.parasparSessionId,
                        "parasparId":self.customerId
                    },
                    "shippingAddress":{
                        "company":"",
                        "address1":address.json()["basket"]["shipping_details"]["address1"],
                        "address2":address.json()["basket"]["shipping_details"]["address2"],
                        "city":address.json()["basket"]["shipping_details"]["city"],
                        "country":address.json()["basket"]["shipping_details"]["country_name"],
                        "postcode":address.json()["basket"]["shipping_details"]["postcode"],
                        "shortCountry":address.json()["basket"]["shipping_details"]["country_id"],
                        "delivery_instructions":""
                    },
                    "billingAddress":{
                        "company":"",
                        "address1":address.json()["basket"]["billing_details"]["address1"],
                        "address2":address.json()["basket"]["billing_details"]["address2"],
                        "city":address.json()["basket"]["billing_details"]["city"],
                        "country":address.json()["basket"]["billing_details"]["country_name"],
                        "postcode":address.json()["basket"]["billing_details"]["postcode"],
                        "shortCountry":address.json()["basket"]["billing_details"]["country_id"],
                        "delivery_instructions":""
                    },
                    "authState":self.authState
                }

                params = {"medium": "web","apiKey": "lGJjE ccd0SiBdu3I6yByRp3/yY8uVIRFa9afLx 2YSrSwkWDfxq0YKUsh96/tP84CZO4phvoR 0y9wtm9Dh5w==","checkout_client": "secure"}
                logger.prepare(SITE,self.taskID,'Updating customer data...')

                try:
                    customer = self.session.put('https://paymentgateway.checkout.footasylum.net/customer',params=params,json=payload,headers={
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                        'accept': 'application/json',
                        'authority': 'paymentgateway.checkout.footasylum.net',
                        'origin':'https://secure.footasylum.com',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'cross-site',
                        'referer': 'https://secure.footasylum.com/?checkoutSessionId={}'.format(self.checkoutSessionId)
                    })
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    log.info(e)
                    logger.error(SITE,self.taskID,'Error: {}'.format(e))
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    self.basketAddress()

                if customer.status_code == 200 and customer.json()["status"] == "success":
                    logger.warning(SITE,self.taskID,'Customer updated')
                    if self.task["PAYMENT"].lower() == "paypal":
                        self.paymentToken()
                    else:
                        self.paymentToken()
                else:
                    logger.error(SITE,self.taskID,'Failed to update customer. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.basketAddress()

            else:
                logger.error(SITE,self.taskID,'Failed to set shipping. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.basketAddress()
        
        else:
            logger.error(SITE,self.taskID,'Failed to set shipping. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.basketAddress()

    def basketCheck(self):
        captchaResponse = captcha.v3('6LfENJwUAAAAANpLoBFfQG7BbAR4iQd-FvXSUzO8','https://secure.footasylum.com',self.session.proxies,SITE,self.taskID)
        if captchaResponse == "empty":
            captchaResponse = captcha.v2('6Ldpi-gUAAAAANpo2mKVvIR6u8nUGrInKKik8MME',self.task["PRODUCT"],self.proxies,SITE,self.taskID)
        payload = {
            "checkoutSessionId":self.checkoutSessionId,
            "websaleId":self.basketId,
            "recaptchaToken":captchaResponse,
            "cartId":self.pasparBasketId,
            "customer":{
                "parasparId":self.customerId
            },
            "source":"new-checkout"
        }
        params = {
            'medium': 'web',
            'apiKey': 'lGJjE ccd0SiBdu3I6yByRp3/yY8uVIRFa9afLx 2YSrSwkWDfxq0YKUsh96/tP84CZO4phvoR 0y9wtm9Dh5w==',
            'checkout_client': 'secure'
        }
        logger.prepare(SITE,self.taskID,'Creating checkout...')

        try:
            basketCheck = self.session.post('https://paymentgateway.checkout.footasylum.net/basket/check',params=params,json=payload,headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'accept': 'application/json',
                'authority': 'paymentgateway.checkout.footasylum.net',
                'origin':'https://secure.footasylum.com',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'referer': 'https://secure.footasylum.com/?checkoutSessionId={}'.format(self.checkoutSessionId)
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.basketCheck()

        try:
            basketCheck.json()
        except:
            logger.error(SITE,self.taskID,'Failed to check basket. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.basketCheck()

        if basketCheck.status_code == 200 and basketCheck.json()["status"] == "success":
            logger.warning(SITE,self.taskID,'Successfully created new checkout')
            if self.task["PAYMENT"].lower() == "paypal":
                self.paymentToken()
            else:
                self.paymentToken()
        else:
            logger.error(SITE,self.taskID,'Failed to check basket. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.basketCheck()

    
    def paymentToken(self):
        logger.prepare(SITE,self.taskID,'Getting payment token...')
        try:
            pt = self.session.post('https://paymentgateway.checkout.footasylum.net/paypal/payment-token',data={"basketId":self.pasparBasketId},headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'accept': 'application/json',
                'authority': 'paymentgateway.checkout.footasylum.net',
                'origin':'https://secure.footasylum.com',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'path': '/paypal/payment-token',
                'referer': 'https://secure.footasylum.com/?checkoutSessionId={}'.format(self.checkoutSessionId)
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)

        if pt.status_code == 200 and pt.json()["status"] == "success":
            logger.warning(SITE,self.taskID,'Successfully retrieved payment token')
            self.paymentId = pt.json()["data"]["payment_id"]
            self.payPal()
        else:
            logger.error(SITE,self.taskID,'Failed to retrieve payment token. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.paymentToken()

    
    def payPal(self):
        logger.info(SITE,self.taskID,'Starting [PAYPAL] checkout...')
        payPalHeaders = {
            'authority': 'www.paypal.com',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'x-csrf-jwt': '__blank__',
            'x-requested-by': 'smart-payment-buttons',
            'x-requested-with': 'XMLHttpRequest',
            'content-type': 'application/json',
            'accept': 'application/json',
            'origin': 'https://www.paypal.com'

        }
        logger.prepare(SITE,self.taskID,'Getting paypal checkout token...')
        try:
            ec = self.session.post('https://www.paypal.com/smart/api/payment/{}/ectoken'.format(self.paymentId),headers=payPalHeaders,json={"meta":{}})
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.payPal()

        if ec.status_code == 200 and ec.json()["ack"] == "success":
            self.end = time.time() - self.start
            logger.warning(SITE,self.taskID,'Successfully retrieved PayPal checkout token')
            self.ecToken = ec.json()["data"]["token"]
            paypalURL = 'https://www.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token={}&useraction=commit'.format(self.ecToken)

            logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')
            updateConsoleTitle(False,True,SITE)
 

            url = storeCookies(paypalURL,self.session, self.productTitle, self.productImage, self.productPrice)

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
            logger.error(SITE,self.taskID,'Failed to get PayPal checkout token. Retrying...')
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
            self.payPal()

    def stripe(self):
        self.publicKey = 'pk_live_y7GywYfDSuh3fr8oraR8g66U' 
        pass
        #payload = {
        #    'type': 'card',
        #    'currency': self.currency,
        #    'amount': 8499,
        #    'owner[name]': '{} {}'.format(),
        #    'owner[email]': self.shippingDetails["email"],
        #    'owner[address][line1]': self.shippingDetails["address1"],
        #    'owner[address][city]': self.shippingDetails["city"],
        #    'owner[address][postal_code]': self.shippingDetails["postcode"],
        #    'owner[address][country]': self.shippingDetails["country_id"],
        #    'metadata[description]': 'New Checkout payment for FA products',
        #    'redirect[return_url]':'https://secure.footasylum.com/redirect-result?checkoutSessionId={}&disable_root_load=true'.format(self.checkoutSessionId)   ,      
        #    'card[number]': 4596548040807232
        #    'card[cvc]': 734
        #    'card[exp_month]': 09
        #    'card[exp_year]': 24
        #    'guid': f0934449-96c0-41bd-90bd-8db38299e017
        #    'muid': e5526e0d-7c48-4cd7-b1c2-0bace1547c62
        #    'sid': df95877c-8c4e-44b4-a43f-db1b1b85073d
        #    'pasted_fields': 'number'
        #    'payment_user_agent': 'stripe.js/47146d16; stripe-js-v3/47146d16'
        #    'time_on_page': 114975
        #    'referrer': 'https://secure.footasylum.com/?checkoutSessionId={}'.format(self.checkoutSessionId)
        #    'key': 'pk_live_y7GywYfDSuh3fr8oraR8g66U'
        #}
        


            





                    


                        

                

    

            

   