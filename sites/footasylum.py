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
import tls as client
import http.cookiejar
from datetime import timezone, datetime
import uuid

from utils.captcha import captcha
from utils.logger import logger
from utils.webhook import Webhook
from utils.log import log
from utils.threeDS import threeDSecure
from utils.functions import (
    loadSettings,
    loadProfile,
    loadProxy2,
    createId,
    loadCookie,
    loadToken,
    sendNotification,
    injection,
    storeCookies,
    updateConsoleTitle,
    scraper,
    footlocker_snare,
    birthday,
    encodeURIComponent,
    urlEncode,
    b64Encode
)
import utils.config as CONFIG

def getCookies(jar):
    cookieString = ""
    for c in jar:
        cookieString += '{}={};'.format(c.name,c.value)
    
    return cookieString

_SITE_ = 'FOOTASYLUM'
SITE = 'Footasylum'
class FOOTASYLUM:
    def success(self,message):
        logger.success(SITE,self.taskID,message)
    def error(self,message):
        logger.error(SITE,self.taskID,message)
    def prepare(self,message):
        logger.prepare(SITE,self.taskID,message)
    def warning(self,message):
        logger.warning(SITE,self.taskID,message)
    def info(self,message):
        logger.info(SITE,self.taskID,message)
    def secondary(self,message):
        logger.secondary(SITE,self.taskID,message)
    def alert(self,message):
        logger.alert(SITE,self.taskID,message)


    def task_checker(self):
        originalTask = self.task
        while True:
            with open('./{}/tasks.csv'.format(_SITE_.lower()),'r') as csvFile:
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
    
    def setCookies(self,response):
        for c in response.cookies:
            self.cookieJar.set_cookie(http.cookiejar.Cookie(
                version=0,
                name=c,
                value=response.cookies[c],
                port=None,
                port_specified=False,
                domain="www.footasylum.com",
                domain_specified=False,
                domain_initial_dot=False,
                path="/",
                path_specified=True,
                secure=False,
                expires=None,
                discard=True,
                comment=None,
                comment_url=None,
                rest={"HttpOnly": None},
                rfc2109=False,
            ))

    def rotateProxy(self, noProxy = True):
        self.proxy = loadProxy2(self.task["PROXIES"],self.taskID,SITE)
        
        if noProxy == False:
            self.proxy = None

        self.session = client.Session(
            browser=client.Fingerprint.CHROME_83,
            proxy=self.proxy
        )
        return

    def __init__(self, task, taskName, rowNumber):
        self.task = task
        self.taskID = taskName
        self.rowNumber = rowNumber

        if self.rowNumber != 'qt': 
            threading.Thread(target=self.task_checker,daemon=True).start()

        self.proxy = loadProxy2(self.task["PROXIES"],self.taskID,SITE)
        try:
            self.session = client.Session(
                browser=client.Fingerprint.CHROME_83,
                proxy=self.proxy
            )
            # self.session = scraper()
        except Exception as e:
            self.error(f'error => {e}')
            self.__init__(task,taskName,rowNumber)

        self.cookieJar = http.cookiejar.CookieJar()


        self.webhookData = {
            "site":SITE,
            "product":"n/a",
            "size":"n/a",
            "image":"https://i.imgur.com/VqWvzDN.png",
            "price":"0",
            "profile":self.task['PROFILE'],
            "speed":0,
            "url":"https://venetiacli.io",
            "paymentMethod":"n/a",
            "proxy":"n/a",
            "product_url":self.task['PRODUCT']
        }

        self.apiKey = "lGJjE+ccd0SiBdu3I6yByRp3/yY8uVIRFa9afLx+2YSrSwkWDfxq0YKUsh96/tP84CZO4phvoR+0y9wtm9Dh5w=="

        self.ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'

        self.profile = loadProfile(self.task["PROFILE"])
        if self.profile == None:
            self.error("Profile Not found. Exiting...")
            time.sleep(10)
            sys.exit()

        self.tasks()
    
    def tasks(self):
        self.orderNum = None

        self.monitor()
        # self.login()
        self.addToCart()
        self.startSession()
        self.getInfo()
        self.email()
        self.basketDetails()
        # self.shipping()
        self.shippingMethod()
        self.updateCustomerData()
        self.basketCheck()
        

        if self.task['PAYMENT'].strip().lower() == "paypal":
            self.paymentToken()
            self.paypal()
        else:
            self.card()
            self.cardStage2()

        self.sendToDiscord()

    def monitor(self):
        while True:
            self.prepare("Getting Product...")

            try:
                response = self.session.get(self.task["PRODUCT"],headers={
                    'user-agent': self.ua,
                    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'cookie':getCookies(self.cookieJar)
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                self.rotateProxy()
                time.sleep(int(self.task["DELAY"]))
                continue
            
            self.setCookies(response)
            # https://footasylum.queue-it.net/javascriptqueue/footasylum/prodqueue/1615849742928?t=https%3A%2F%2Fwww.footasylum.com%2Fmen%2Fmens-footwear%2Ftrainers%2Fjordan-air-jordan-1-low-se-trainer-black-turf-orange-white-4051607%2F&ver=js2.0.17
            if response.status == 200:
                self.start = time.time()

                self.warning("Retrieved Product")

                try:
                    soup = BeautifulSoup(response.text, "html.parser")

                    pf_id = soup.find("input",{"name":"pf_id"})["value"]


                    regex = r"variants = {(.+)}"
                    matches = re.search(regex, response.text, re.MULTILINE)
                    if matches:
                        productData = json.loads(matches.group().split('variants = ')[1].replace("'",'"'))

                        pids = []
                        allSizes = []
                        sizes = []

                        for s in productData:
                            pids.append(s)

                        for s in pids:
                            p = productData[s]
                            try:
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
                            except:
                                pass

                        if len(sizes) == 0:
                            self.error("No sizes available")
                            time.sleep(int(self.task["DELAY"]))
                            continue
                        
       
                        if self.task["SIZE"].strip().lower() != "random":
                            if self.task["SIZE"] not in sizes:
                                self.error("Size not available")
                                time.sleep(int(self.task["DELAY"]))
                                continue
                            else:
                                for size in allSizes:
                                    if size.split('#')[0].strip().lower() == self.task["SIZE"].strip().lower():
                                        self.size = size.split('#')[0]
                                        self.sizeSku = size.split('#')[1]
                                        self.sizeColour = size.split("#")[2]
                                        
                                        self.webhookData['product'] = size.split("#")[5]
                                        self.webhookData['image'] = size.split("#")[4]
                                        self.webhookData['price'] = size.split("#")[3]

                                        self.warning(f"Found Size => {self.size}")
            
                        else:
                            selected = random.choice(allSizes)
                            self.size = selected.split('#')[0]
                            self.sizeSku = selected.split('#')[1]
                            self.sizeColour = selected.split("#")[2]
                            
                            self.webhookData['product'] = selected.split("#")[5]
                            self.webhookData['image'] = selected.split("#")[4]
                            self.webhookData['price'] = selected.split("#")[3]


                            self.warning(f"Found Size => {self.size}")


                    else:
                        raise Exception

                except Exception as e:
                    log.info(e)
                    self.error("Failed to parse product data (maybe OOS)")
                    time.sleep(int(self.task['DELAY']))
                    continue
                
                self.webhookData['size'] = self.size
                return
                    
            else:
                self.error(f"Failed to get product [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def login(self):
        while True:
            self.prepare("Logging In...")
            try:
                response = self.session.get('https://www.footasylum.com/page/login/',headers={
                    'user-agent': self.ua,
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'cookie':getCookies(self.cookieJar)
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                self.rotateProxy()
                time.sleep(int(self.task["DELAY"]))
                continue
        
            self.setCookies(response)
            if response.status == 200:
                try:
                    soup = BeautifulSoup(response.text,"html.parser")
                    self.preLog = soup.find('input',{'name':'prelog'})["value"]
                except Exception as e:
                    log.info(e)
                    self.error("Failed to parse login page")
                    time.sleep(int(self.task["DELAY"]))
                    continue
            else:
                self.error('Failed to get login page. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue


            
            try:
                # payload = {
                #     'target': '',
                #     'targetar': '',
                #     'pf_id': '',
                #     'sku': '',
                #     'rdPassword': 'LOGIN',
                #     'prelog':self.preLog,
                #     'lookup_Validate': '1',
                #     'email2': self.task["ACCOUNT EMAIL"],
                #     'password': self.task["ACCOUNT PASSWORD"]
                # }
                payload = "target=&targetar=&pf_id=&sku=&rdPassword=LOGIN&prelog={}&lookup_Validate=1&email2={}&password={}".format(
                    self.preLog,
                    encodeURIComponent(self.task["ACCOUNT EMAIL"]),
                    urlEncode(self.task["ACCOUNT PASSWORD"])
                )
            except Exception as e:
                log.info(e)
                self.error("Failed to login [error construcing payload]")
                time.sleep(int(self.task["DELAY"]))
                continue
            
           
            try:
                response2 = self.session.post('https://www.footasylum.com/page/login/',data=payload,headers={
                    'origin':'https://www.footasylum.com',
                    'referer': 'https://www.footasylum.com/page/login/',
                    'user-agent': self.ua,
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded',
                    'cookie':getCookies(self.cookieJar),
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-user': '?1',
                    'sec-gpc': '1'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue

            
            self.setCookies(response2)
            if response2.status == 200 and '?sessionid=' in response2.url: 
                self.warning("Successfully logged in")
                self.sessionId = response2.url.split('?sessionid=')[1]
                return
            
            else:
                self.error("Failed to login. Retrying...")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue
    
    def addToCart(self):
        
        while True:
            self.prepare("Adding to cart...")

            try:
                params = {
                    "target":"ajx_basket.asp",
                    "sku":self.sizeSku,
                    # "sessionid":self.sessionId,
                    "_":str(int(datetime.now(tz=timezone.utc).timestamp() * 1000))
                }
            except:
                self.error(f"Failed to cart [error constructing params]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
            
            try:
                # &sessionid={}
                response = self.session.get('https://www.footasylum.com/page/xt_orderform_additem/?target={}&sku={}&_={}'.format(
                    "ajx_basket.asp",
                    self.sizeSku,
                    # self.sessionId,
                    str(int(datetime.now(tz=timezone.utc).timestamp() * 1000))
                ),headers={
                    'user-agent':self.ua,
                    'accept':'*/*',
                    'x-requested-with':'XMLHttpRequest',
                    'cookie':getCookies(self.cookieJar),
                    'authority': 'www.footasylum.com',
                    'referer':self.task["PRODUCT"]
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue



            self.setCookies(response)
            if response.status in [200,302]:
                self.success("Added to cart!")
                updateConsoleTitle(True,False,SITE)
                return
            
            else:
                self.error(f"Failed to cart [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def startSession(self):
        while True:
            self.prepare("Getting session...")


            try:
                response = self.session.post(f'https://www.footasylum.com/page/nw-api/initiatecheckout/',headers={
                    'user-agent':self.ua,
                    'accept':'text/plain, */*; q=0.01',
                    'origin':'https://www.footasylum.com',
                    'x-requested-with':'XMLHttpRequest',
                    'cookie':getCookies(self.cookieJar),
                    'referer': 'https://www.footasylum.com/page/basket/',
                    'content-type':'application/x-www-form-urlencoded'
                    # 'referer':'https://www.footasylum.com/page/basket/'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue

            self.setCookies(response)
            if response.status in [200,302]:
                try:
                    responseJson = json.loads(response.text)
                    self.checkoutSessionId = responseJson["checkoutSessionId"]
                    self.basketId = responseJson["basket"]["id"]
                    self.basketCustomerId = responseJson["basket"]["customerId"]
                except Exception as e:
                    self.error(f"Failed to get session [failed to parse response]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue

                self.warning("Got session")
                return
            
            else:
                self.error(f"Failed to get session [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def getInfo(self):
        while True:
            self.prepare("Getting session info...")

            params = {
                "orderNum":self.checkoutSessionId,
                "refresh":True,
                "medium":"web",
                "apiKey":self.apiKey,
                "checkout_client":"secure"
            }

            try:
                response = self.session.get('https://api.gateway.footasylum.net/basket?orderNum={}&refresh={}&medium={}&apiKey={}&checkout_client={}'.format(
                    self.checkoutSessionId,
                    "true",
                    "web",
                    self.apiKey,
                    "secure"
                ),headers={
                    'user-agent':self.ua,
                    'accept':'application/json',
                    'cookie':getCookies(self.cookieJar),
                    'referer':'https://secure.footasylum.com/',
                    'authority': 'paymentgateway.checkout.footasylum.net',
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue

            self.setCookies(response)
            if response.status == 200:
                try:
                    responseJson = json.loads(response.text)
                    self.customerId = responseJson["basket"]["paraspar_customer_id"]
                    self.currency = responseJson["basket"]["currency_code"]
                    self.pasparBasketId = responseJson["basket"]["paraspar_id"]
                    self.channelId = responseJson["basket"]["channel_id"]
                    self.fascia_id = responseJson["basket"]["fascia_id"]
                    self.parasparSessionId = responseJson["basket"]["paraspar_session_id"]
                except Exception as e:
                    self.error(f"Failed to get session info [failed to parse response]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue

                self.warning("Got session info")
                return
            
            else:
                self.error(f"Failed to get session info [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def email(self):
        while True:
            self.prepare("Setting email...")

            try:
                response = self.session.post('https://api.gateway.footasylum.net/wrapper/customer/check?checkout_client=secure',headers={
                    'user-agent':self.ua,
                    'accept':'application/json',
                    'cookie':getCookies(self.cookieJar),
                    'referer':'https://secure.footasylum.com/',
                },json={"fascia_id":self.fascia_id,"channel_id":self.channelId,"currency_code":self.currency,"customer":{"email":self.profile['email']}})
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue

            self.setCookies(response)
            if response.status == 200:
                self.warning("Email set")
                return
            
            else:
                self.error(f"Failed to set email [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def basketDetails(self):
        while True:
            self.prepare("Getting customer info...")

            payload = {
                "fascia_id":self.fascia_id,
                "channel_id":self.channelId,
                "currency_code":self.currency,
                "customer":{
                    "customer_id":self.customerId,
                    "sessionID":self.parasparSessionId,
                    "request_address":1,
                    "request_basket":1
                }
            }

            payload = {
                "fascia_id":self.fascia_id,
                "channel_id":self.channelId,
                "currency_code":self.currency,
                "customer": {
                    "customer_id": self.customerId,
                    "sessionID": "",
                    "hash": "xcx"
                },
                "basket_id": self.pasparBasketId,
                "shipping_country": self.profile['countryCode'].upper()
            }

            try:
                # https://r9udv3ar7g.execute-api.eu-west-2.amazonaws.com/prod/customer/details?checkout_client=secure
                response = self.session.post('https://api.gateway.footasylum.net/wrapper/basket?checkout_client=secure',json=payload,headers={
                    'user-agent':self.ua,
                    'accept':'application/json',
                    'cookie':getCookies(self.cookieJar),
                    'referer':'https://secure.footasylum.com/'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue

            self.setCookies(response)
            if response.status == 200:
                try:
                    responseJson = json.loads(response.text)
                    self.customer = responseJson["customer"]
                    self.itemId = responseJson["basket"]["items"][0]["sku"]
                    self.stripePrice = str(responseJson["basket"]["total"]).replace('.','')
                    self.webhookData['price'] = '{} {}'.format(responseJson["basket"]["total"],responseJson["basket"]["currency_code"])

                    # self.title = responseJson["customer"]["title"]
                    # self.shippingDetails = responseJson["basket"]["shipping_details"]
                    # self.billingDetails = responseJson["basket"]["billing_details"]
                    self.shippingMethodCode = responseJson["basket"]["shipping_method_code"]
                    self.shippingMethodName = responseJson["basket"]["shipping_method_name"]
                    self.shippingTotal = responseJson["basket"]["shipping_total"]
                    self.authState = responseJson["customer"]["session_state"]
                except Exception as e:
                    self.error(f"Failed to get customer info [failed to parse response]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue

                self.warning("Got customer info")
                return
            
            else:
                self.error(f"Failed to get customer info [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def delivery(self):
        while True:
            self.prepare("Submitting Delivery...")

            try:
                payload = {
                    "email":self.profile['email'],
                    "order_num":self.checkoutSessionId,
                    "postcode":self.profile['zip'],
                    "country":self.profile['countryCode'],
                    "basket":{
                        "id":self.pasparBasketId,
                        "basketItems":[{"id":self.itemId,"qty":1}]
                    },
                    "paraspar_customer_id":self.customerId,
                    "paraspar_session_id":None,
                    "channelId":self.channelId,
                    "fascia_id":self.fascia_id
                }
            except:
                self.error("Failed to set delivery [failed to construct payload]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

            try:
                response = self.session.post('https://api.gateway.footasylum.net/delivery/options?checkout_client=secure',headers={
                    'user-agent':self.ua,
                    'accept':'application/json',
                    'cookie':getCookies(self.cookieJar),
                    'referer':'https://secure.footasylum.com/',
                },json={"fascia_id":self.fascia_id,"channel_id":self.channelId,"currency_code":self.currency,"customer":{"email":self.profile['email']}})
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue

            self.setCookies(response)
            if response.status == 200:

                self.warning("Delivery set")
                return
            
            else:
                self.error(f"Failed to set delivery [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def shipping(self):
        while True:
            self.prepare("Submitting Basket Address...")

            try:
                payload = {
                    "fascia_id":self.fascia_id,
                    "channel_id":self.channelId,
                    "currency_code":self.currency,
                    "customer":{
                        "customer_id":self.customerId,
                        "sessionID":None
                    },
                    "basket":{
                        "basket_id":self.pasparBasketId
                    },
                    "shipping_details":{
                        "title":"Mr",
                        "firstname":self.profile['firstName'],
                        "surname":self.profile['lastName'],
                        "address1":self.profile['house'] + ' ' + self.profile['addressOne'],
                        "address2":self.profile['addressTwo'],
                        "town":self.profile["city"],
                        "county":self.profile["region"],
                        "postcode":self.profile["zip"],
                        "country_id":self.profile["countryCode"],
                        "country_name":self.profile["country"],
                        "phone":self.profile["phone"],
                        "mobile":self.profile["phone"]
                    },
                    "billing_details":{
                        "title":"Mr",
                        "firstname":self.profile['firstName'],
                        "surname":self.profile['lastName'],
                        "address1":self.profile['house'] + ' ' + self.profile['addressOne'],
                        "address2":self.profile['addressTwo'],
                        "town":self.profile["city"],
                        "county":self.profile["region"],
                        "postcode":self.profile["zip"],
                        "country_id":self.profile["countryCode"],
                        "country_name":self.profile["country"],
                        "phone":self.profile["phone"],
                        "mobile":self.profile["phone"]
                    }
                }
            except Exception as e:
                log.info(e)
                self.error(f"Failed to submit Basket Address [failed to construct payload]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue


            try:
                response = self.session.post('https://api.gateway.footasylum.net/wrapper/basket/basketaddaddress?checkout_client=secure',json=payload,headers={
                    'user-agent':self.ua,
                    'accept':'application/json',
                    'cookie':getCookies(self.cookieJar),
                    'referer':'https://secure.footasylum.com/'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue

            self.setCookies(response)
            if response.status == 200:
                try:
                    responseJson = json.loads(response.text)
                    print(responseJson)
                    # self.basketaddressResponse = responseJson
                    self.stripePrice = str(responseJson["basket"]["total"]).replace('.','')
                    self.webhookData['price'] = '{} {}'.format(responseJson["basket"]["total"],responseJson["basket"]["currency_code"])
                    self.shippingMethodCode = responseJson["basket"]["shipping_method_code"]
                    self.shippingMethodName = responseJson["basket"]["shipping_method_name"]
                    self.shippingTotal = responseJson["basket"]["shipping_total"]
                    self.authState = responseJson["customer"]["session_state"]
                except Exception as e:
                    self.error(f"Failed to submit Basket Address [failed to parse response]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue

                self.warning("Submitted Basket Address")
                return
            
            else:
                self.error(f"Failed to submit Basket Address[{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def shippingMethod(self):
        while True:
            self.prepare("Submitting shipping method...")

            try:
                payload = {
                    "basketId":self.pasparBasketId,
                    "type":"shipping",
                    "shippingTotal":self.shippingTotal,
                    "shippingCode":self.shippingMethodCode,
                    "shippingCarrier":self.shippingMethodName
                }
                params = {
                    "medium": "web",
                    "apiKey":self.apiKey,
                    "checkout_client": "secure"
                }
            except Exception as e:
                log.info(e)
                self.error(f"Failed to submit shipping method [failed to construct payload]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
            
            try:
                response = self.session.put('https://api.gateway.footasylum.net/basket/shipping?medium={}&apiKey={}&checkout_client={}'.format(
                    "web",
                    self.apiKey,
                    "secure"
                ),json=payload,headers={
                    'user-agent':self.ua,
                    'accept':'application/json',
                    'cookie':getCookies(self.cookieJar),
                    'referer':'https://secure.footasylum.com/'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue

            self.setCookies(response)
            if response.status == 200:
                try:
                    responseJson = json.loads(response.text)
                except Exception as e:
                    self.error(f"Failed to submit shipping method [failed to parse response]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue

                self.warning("Submitted shipping method")
                return
            
            else:
                self.error(f"Failed to submit shipping method [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def updateCustomerData(self):
        while True:
            self.prepare("Updating customer...")

            try:
                params = {
                    "medium": "web",
                    "apiKey": self.apiKey,
                    "checkout_client": "secure"
                }

                payload = {
                    "cartId": self.pasparBasketId,
                    "customer": {
                        "firstname": self.profile['firstName'],
                        "lastname": self.profile['lastName'],
                        "email": self.profile['email'],
                        "mobile": self.profile['phone'],
                        "title": "Mr",
                        "newsletter": 1,
                        "sessionId": None,
                        "parasparId": self.customerId
                    },
                    "shippingAddress": {
                        "company": "",
                        "address1":self.profile['house'] + ' ' + self.profile['addressOne'],
                        "address2":self.profile['addressTwo'],
                        "city": self.profile['city'],
                        "country": self.profile['country'],
                        "postcode": self.profile['zip'],
                        "shortCountry": self.profile['countryCode'],
                        "delivery_instructions": ""
                    },
                    "billingAddress": {
                        "company": "",
                        "address1":self.profile['house'] + ' ' + self.profile['addressOne'],
                        "address2":self.profile['addressTwo'],
                        "city": self.profile['city'],
                        "country": self.profile['country'],
                        "postcode": self.profile['zip'],
                        "shortCountry": self.profile['countryCode'],
                        "delivery_instructions": ""
                    },
                    "authState": self.authState
                }

            except Exception as e:
                log.info(e)
                self.error(f"Failed to update customer [failed to construct payload]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

            try:
                response = self.session.put('https://api.gateway.footasylum.net/customer?medium={}&apiKey={}&checkout_client={}'.format(
                    "web",
                    self.apiKey,
                    "secure"
                ),json=payload,headers={
                    'user-agent':self.ua,
                    'accept':'application/json',
                    'cookie':getCookies(self.cookieJar),
                    'referer':'https://secure.footasylum.com/?checkoutSessionId={}'.format(self.checkoutSessionId)
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue

            self.setCookies(response)
            if response.status == 200:
                try:
                    responseJson = json.loads(response.text)
                    fa_stat = responseJson["status"] 
                except Exception as e:
                    self.error(f"Failed to update customer [failed to parse response]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue
                    
                if fa_stat == "success":
                    self.warning("Updated customer")
                    return
                else:
                    self.error(f"Failed to update customer [{str(fa_stat)}]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue
            
            else:
                self.error(f"Failed to update customer [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def basketCheck(self):
        while True:
            # self.prepare("Checking basket...")

            if CONFIG.captcha_configs[_SITE_]['type'].lower() == 'v3':
                capToken = captcha.v3(CONFIG.captcha_configs[_SITE_]['siteKey'],CONFIG.captcha_configs[_SITE_]['url'],self.task['PROXIES'],SITE,self.taskID)
            elif CONFIG.captcha_configs[_SITE_]['type'].lower() == 'v2':
                capToken = captcha.v2(CONFIG.captcha_configs[_SITE_]['siteKey'],CONFIG.captcha_configs[_SITE_]['url'],self.task['PROXIES'],SITE,self.taskID)

            try:
                response = self.session.post('https://api.gateway.footasylum.net/basket/check?medium={}&apiKey={}&checkout_client={}'.format(
                    "web",
                    self.apiKey,
                    "secure"
                ),data=json.dumps({
                    "checkoutSessionId": self.checkoutSessionId,
                    "websaleId": self.checkoutSessionId.split('-')[len(self.checkoutSessionId.split('-')) - 1],
                    "recaptchaToken": capToken,
                    "cartId": self.pasparBasketId,
                    "customer": { "parasparId": self.customerId },
                    "source": "new-checkout"
                })
                ,headers={
                    'user-agent':self.ua,
                    'accept':'application/json',
                    'cookie':getCookies(self.cookieJar),
                    'referer':'https://secure.footasylum.com'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue
            
            return

    def paymentToken(self):
        while True:
            self.prepare("Getting payment token...")

            try:
                payload = { "basketId":self.pasparBasketId }
            except Exception as e:
                log.info(e)
                self.error(f"Failed to get payment token [failed to construct payload]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

            try:
                response = self.session.post('https://api.gateway.footasylum.net/paypal/payment-token',json=payload,headers={
                    'user-agent':self.ua,
                    'accept':'application/json',
                    'cookie':getCookies(self.cookieJar),
                    'referer':'https://secure.footasylum.com/'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy(True)
                continue
            self.setCookies(response)

            if response.status == 200:
                try:
                    responseJson = json.loads(response.text)
                    fa_stat = responseJson["status"] 
                    pay_id = responseJson["data"]["payment_id"]
                except Exception as e:
                    self.error(f"Failed to get payment token [failed to parse response]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue
                    
                if fa_stat == "success":
                    self.warning("Got payment token")
                    self.paymentId = pay_id
                    return
                else:
                    self.error(f"Failed to get payment token [{str(fa_stat)}]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue
            
            else:
                self.error(f"Failed to get payment token [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def paypal(self):
        while True:
            self.prepare("Getting paypal checkout...")


            try:
                response = self.session.post('https://www.paypal.com/smart/api/payment/{}/ectoken'.format(self.paymentId),json={"meta":{}},headers={
                    'user-agent':self.ua,
                    'accept':'application/json',
                    'x-csrf-jwt':'__blank__',
                    'x-requested-by':'smart-payment-buttons',
                    'x-requested-with':'XMLHttpRequest',
                    'cookie':getCookies(self.cookieJar),
                    'content-type':'application/json'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy(True)
                continue

            self.setCookies(response)
            if response.status == 200:
                try:
                    responseJson = json.loads(response.text)
                    pp_stat = responseJson["ack"] 
                    ecToken = responseJson["data"]["token"]
                except Exception as e:
                    self.error(f"Failed to get paypal checkout [failed to parse response]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue
                    
                if pp_stat == "success":
                    self.end = time.time() - self.start
                    self.webhookData['speed'] = self.end

                    self.success("Got paypal checkout")
                    updateConsoleTitle(False,True,SITE)
                    paypalURL = 'https://www.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token={}&useraction=commit'.format(ecToken)
                    self.webhookData['url'] = storeCookies(
                        paypalURL,self.cookieJar,
                        self.webhookData['product'],
                        self.webhookData['image'],
                        self.webhookData['price'],
                        True
                    )

                    return
                else:
                    self.error(f"Failed to get payment token [{str(pp_stat)}]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue
            
            else:
                self.error(f"Failed to get payment token [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def card(self):
        self.pk_live = 'pk_live_y7GywYfDSuh3fr8oraR8g66U'
        while True:
            self.prepare("Completing card checkout...")

            if len(self.profile['card']['cardMonth']) == 1:
                month = '0' + self.profile['card']['cardMonth']
            else:
                month = self.profile['card']['cardMonth']

            self.muid = str(uuid.uuid4())
            self.sid  = str(uuid.uuid4())
            self.guid = str(uuid.uuid4())

            payload1 = {
                'type': 'card',
                'currency': self.currency,
                'amount': self.stripePrice,
                'owner[name]': '{} {}'.format(self.profile['firstName'], self.profile['lastName']),
                'owner[email]': self.profile['email'],
                'owner[address][line1]': self.profile['house'] + ' ' + self.profile['addressOne'],
                'owner[address][city]': self.profile['city'],
                'owner[address][postal_code]': self.profile['zip'],
                'owner[address][country]': self.profile['countryCode'],
                'metadata[description]': 'New Checkout payment for FA products',
                'redirect[return_url]': f'https://secure.footasylum.com/redirect-result?checkoutSessionId={self.checkoutSessionId}&disable_root_load=true',
                'card[number]': self.profile['card']['cardNumber'],
                'card[cvc]': self.profile['card']['cardCVV'],
                'card[exp_month]': month,
                'card[exp_year]': self.profile['card']['cardYear'][-2:],
                'guid': self.guid,
                'muid': self.muid,
                'sid': self.sid,
                'pasted_fields': 'number',
                'payment_user_agent': 'stripe.js/696e73007; stripe-js-v3/696e73007',
                'time_on_page': '479625',
                'referrer': 'https://secure.footasylum.com/',
                'key': self.pk_live
            }


            try:
                response = self.session.post('https://api.stripe.com/v1/sources',data=payload1,headers={
                    "user-agent":self.ua,
                    "accept": "application/json",
                    "accept-language": "en-US,en;q=0.9",
                    'Authorization':'Bearer '+self.pk_live,
                    "accept-encoding": "gzip, deflate, br",
                    "referrer": "https://js.stripe.com/",
                    "content-type": "application/x-www-form-urlencoded",
                    "cookie":getCookies(self.cookieJar),
                    "authority": "api.stripe.com"
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue

            self.setCookies(response)
            if response.status == 200:
                try:
                    responseJson = json.loads(response.text)
                    amount = responseJson['amount']
                    currency = responseJson['currency']
                    _id_ = responseJson['id']
                    self.src = _id_
                except Exception as e:
                    self.error(f"Failed to complete card checkout [failed to parse response]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue

                payload2 = {
                    'type': 'three_d_secure',
                    'amount': amount,
                    'currency': currency,
                    'metadata[cart_id]': self.pasparBasketId,
                    'metadata[customer_id]': self.customerId,
                    'metadata[description]': 'New Checkout payment for FA products',
                    'three_d_secure[card]': _id_,
                    'redirect[return_url]': f'https://secure.footasylum.com/redirect-result?checkoutSessionId={self.checkoutSessionId}&disable_root_load=true',
                    'guid': self.guid,
                    'muid': self.muid,
                    'sid': self.sid,
                    'payment_user_agent': 'stripe.js/696e73007; stripe-js-v3/696e73007',
                    'time_on_page': '480452',
                    'referrer': 'https://secure.footasylum.com/',
                    'key': self.pk_live
                }

                try:
                    response2 = self.session.post('https://api.stripe.com/v1/sources',data=payload2,headers={
                        "user-agent":self.ua,
                        "accept": "application/json",
                        "accept-language": "en-US,en;q=0.9",
                        'Authorization':'Bearer '+self.pk_live,
                        "accept-encoding": "gzip, deflate, br",
                        "referrer": "https://js.stripe.com/",
                        "content-type": "application/x-www-form-urlencoded",
                        "cookie":getCookies(self.cookieJar),
                        "authority": "api.stripe.com"
                    })
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    log.info(e)
                    self.error(f"error: {str(e)}")
                    time.sleep(int(self.task["DELAY"]))
                    self.rotateProxy()
                    continue
                
                self.setCookies(response2)
                if response2.status == 200:
                    try:
                        responseJson = json.loads(response2.text)
                        self.redirectUrl = responseJson['redirect']['url']
                        self.src = responseJson['id']
                    except Exception as e:
                        self.error(f"Failed to complete card checkout [failed to parse response]. Retrying...")
                        time.sleep(int(self.task['DELAY']))
                        continue

                    self.warning("Got 3DS Redirect")
                    return
                
                else:
                    self.error(f"Failed to complete card checkout [{str(response.status)}]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue

            else:
                self.error(f"Failed to complete card checkout [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def cardStage2(self):
        while True:
            self.prepare("Getting 3DS checkout...")

            try:
                response0 = self.session.put(f'https://api.gateway.footasylum.net/basket/trans-code?medium=web&apiKey={self.apiKey}&checkout_client=secure',headers={
                    "user-agent":self.ua,
                    "accept": "application/json",
                    "content-type":"application/json",
                    "referrer": "https://secure.footasylum.com/",
                    "cookie":getCookies(self.cookieJar),
                },json={"basketId":self.pasparBasketId,"stripeToken":self.src,"tracking":{"utm":{"utm_source":None,"utm_medium":None,"utm_campaign":None}}})
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue

            try:
                response = self.session.get(self.redirectUrl,headers={
                    "user-agent":self.ua,
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "referrer": "https://secure.footasylum.com/",
                    "cookie":getCookies(self.cookieJar),
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue
            
            self.setCookies(response)
            if response.status == 200 and 'three_d_secure' in response.url:

                try:
                    response2 = self.session.get(response.url,headers={
                        "user-agent":self.ua,
                        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "referrer": "https://secure.footasylum.com/",
                        "cookie":getCookies(self.cookieJar),
                    })
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    log.info(e)
                    self.error(f"error: {str(e)}")
                    time.sleep(int(self.task["DELAY"]))
                    self.rotateProxy()
                    continue
                
                self.setCookies(response2)
                if response2.status == 200:
                    try:
                        soup = BeautifulSoup(response2.text, "html.parser")
                        PaReq = soup.find('input',{'name':'PaReq'})['value']
                        termUrl = soup.find('input',{'name':'TermUrl'})['value']
                        MD = soup.find('input',{'name':'MD'})['value']
                    except Exception as e:
                        self.error(f"Failed to complete card checkout [failed to parse response]. Retrying...")
                        time.sleep(int(self.task['DELAY']))
                        continue

                    self.Dpayload = {
                        "TermUrl":termUrl,
                        "PaReq":PaReq,
                        "MD":MD 
                    }

                    three_d_data = threeDSecure.solve(
                        self.session,
                        self.profile,
                        self.Dpayload,
                        self.webhookData,
                        self.taskID,
                        'https://secure.footasylum.com/'
                    )
                    if three_d_data == False:
                        self.error("Checkout Failed (3DS Declined or Failed). Retrying...")
                        time.sleep(int(self.task['DELAY']))
                        continue
                    
                    try:
                        response3 = self.session.post(termUrl,data=three_d_data,headers={
                            "user-agent":self.ua,
                            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                            "referrer": "https://verifiedbyvisa.acs.touchtechpayments.com/",
                            "cookie":getCookies(self.cookieJar),
                            "content-type":"application/x-www-form-urlencoded"
                        })
                    except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                        log.info(e)
                        self.error(f"error: {str(e)}")
                        time.sleep(int(self.task["DELAY"]))
                        self.rotateProxy()
                        continue
                    
                    self.setCookies(response3)
                    if response3.status == 200:
                        try:
                            soup = BeautifulSoup(response3.text, "html.parser")

                            form = {
                                "MD":soup.find("input",{"name":"MD"})["value"],
                                "PaRes":soup.find("input",{"name":"PaRes"})["value"],
                                "splat":"[]",
                                "captures":soup.find("input",{"name":"captures"})["value"].replace('&quot;','"'),
                                "merchant":soup.find("input",{"name":"merchant"})["value"],
                                "three_d_secure":soup.find("input",{"name":"three_d_secure"})["value"]
                            }
                            post_url = soup.find("form", attrs={"method": "POST"})['action']
                        except Exception as e:
                            self.error('Checkout failed [failed to construct form]. Retrying...')
                            time.sleep(int(self.task['DELAY']))
                            continue


                        try:
                            response4 = self.session.post(post_url,data=form,headers={
                                "user-agent":self.ua,
                                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                                "cookie":getCookies(self.cookieJar),
                                "content-type":"application/x-www-form-urlencoded",
                                "referer":termUrl
                            })
                        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                            log.info(e)
                            self.error(f"error: {str(e)}")
                            time.sleep(int(self.task["DELAY"]))
                            self.rotateProxy()
                            continue

                        self.setCookies(response4)

                        # try:
                        #     response4_2 = self.session.get(response4.url,headers={
                        #         "user-agent":self.ua,
                        #         "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        #         "cookie":getCookies(self.cookieJar),
                        #     })
                        # except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                        #     log.info(e)
                        #     self.error(f"error: {str(e)}")
                        #     time.sleep(int(self.task["DELAY"]))
                        #     self.rotateProxy()
                        #     continue

                        # self.setCookies(response4_2)


                        status = 'pending'
                        while status == 'pending':
                            try:
                                response5 = self.session.get('https://api.gateway.footasylum.net/basket/trans-code?code={}&medium={}&apiKey={}&checkout_client={}'.format(
                                    self.checkoutSessionId,
                                    "web",
                                    self.apiKey,
                                    "secure"
                                ),headers={
                                    "user-agent":self.ua,
                                    "accept": "application/json",
                                    "cookie":getCookies(self.cookieJar),
                                    "referer":"https://secure.footasylum.com/"
                                })
                            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                                log.info(e)
                                self.error(f"error: {str(e)}")
                                time.sleep(int(self.task["DELAY"]))
                                self.rotateProxy()
                                continue
                            self.setCookies(response5)
                            
                            status = response5.json()['basket']['payment_status']
                            time.sleep(1)
                        
                        if status == 'succeeded':
                            try:
                                jsonData = json.loads(response5.text)
                                self.orderNum = jsonData['basket']['tracking']['AWIN']['orderRef']
                            except:
                                pass
                            self.end = time.time() - self.start
                            self.webhookData['speed'] = self.end

                            self.success("Checkout Successful")
                            updateConsoleTitle(False,True,SITE)
                            return
                    


                    else:
                        self.error(f"Checkout failed [{str(response3.status)}]. Retrying...")
                        time.sleep(int(self.task['DELAY']))
                        continue

                else:
                    self.error(f"Failed to get 3DS checkout [{str(response2.status)}]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue

            else:
                self.error(f"Failed to get 3DS checkout [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    
    def sendToDiscord(self):
        while True:
            
            self.webhookData['proxy'] = self.proxy
            sendNotification(SITE,self.webhookData['product'])
            try:
                Webhook.success(
                    webhook=loadSettings()["webhook"],
                    site=SITE,
                    url=self.webhookData['url'],
                    image=self.webhookData['image'],
                    title=self.webhookData['product'],
                    size=self.webhookData['size'],
                    price=self.webhookData['price'],
                    paymentMethod=self.task['PAYMENT'].strip().title(),
                    product=self.webhookData['product_url'],
                    profile=self.task["PROFILE"],
                    proxy=self.webhookData['proxy'],
                    speed=self.webhookData['speed'],
                    order=self.orderNum
                )
                self.secondary("Sent to discord!")
                while True:
                    pass
            except Exception as e:
                self.alert("Failed to send webhook. Checkout here ==> {}".format(self.webhookData['url']))
                while True:
                    pass