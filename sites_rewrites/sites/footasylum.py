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

from utils.captcha import captcha
from utils.logger import logger
from utils.webhook import Webhook
from utils.log import log
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies, updateConsoleTitle, scraper)
from utils.config import *

SITE = 'FOOTASYLUM'
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

    def __init__(self, task, taskName, rowNumber):
        self.task = task
        self.taskID = taskName
        self.rowNumber = rowNumber

        if self.rowNumber != 'qt': 
            threading.Thread(target=self.task_checker,daemon=True).start()

        try:
            self.session = client.Session(browser=client.Fingerprint.CHROME_83)
            # self.session = scraper()
        except Exception as e:
            self.error(f'error => {e}')
            self.__init__(task,taskName,rowNumber)


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

        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)

        self.apiKey = "lGJjE ccd0SiBdu3I6yByRp3/yY8uVIRFa9afLx 2YSrSwkWDfxq0YKUsh96/tP84CZO4phvoR 0y9wtm9Dh5w=="

        self.profile = loadProfile(self.task["PROFILE"])
        if self.profile == None:
            self.error("Profile Not found. Exiting...")
            time.sleep(10)
            sys.exit()

        self.tasks()
    
    def tasks(self):

        self.monitor()
        self.login()
        self.addToCart()
        self.startSession()
        self.getInfo()
        self.basketDetails()
        self.shipping()
        self.shippingMethod()
        self.updateCustomerData()
        self.paymentToken()


        if self.task['PAYMENT'].strip().lower() == "paypal":
            self.paypal()
        else:
            pass
            # self.card()

        self.sendToDiscord()

    def monitor(self):
        while True:
            self.prepare("Getting Product...")

            try:
                response = self.session.get(self.task["PRODUCT"])
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue
            
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
                                    if size.split(':')[0].strip().lower() == self.task["SIZE"].strip().lower():
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
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'cookie':'startTime={}'.format(str(int(time.time())))
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue
        
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
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue


            
            try:
                payload = {
                    'target': '',
                    'targetar': '',
                    'pf_id': '',
                    'sku': '',
                    'rdPassword': 'LOGIN',
                    'prelog':self.preLog,
                    'lookup_Validate': '1',
                    'email2': self.task["ACCOUNT EMAIL"],
                    'password': self.task["ACCOUNT PASSWORD"]
                }
                # payload = "target=&targetar=&pf_id=&sku=&rdPassword=LOGIN&prelog={}&lookup_Validate=1&email2={}&password={}".format(
                #     self.preLog,
                #     self.task["ACCOUNT EMAIL"],
                #     self.task["ACCOUNT PASSWORD"]
                # )
            except Exception as e:
                log.info(e)
                self.error("Failed to login [error construcing payload]")
                time.sleep(int(self.task["DELAY"]))
                continue
           
            try:
                response2 = self.session.post('https://www.footasylum.com/page/login/',data=payload,headers=[
                    ['origin', 'https://www.footasylum.com'],
                    ['referer', 'https://www.footasylum.com/page/login/'],
                    ['user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'],
                    ['accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'],
                    ['accept-language', 'en-US,en;q=0.9'],
                    ['content-type', 'application/x-www-form-urlencoded']
                ])
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue


            if response2.status == 200 and '?sessionid=' in response2.url: 
                self.warning("Successfully logged in")
                self.sessionId = response2.url.split('?sessionid=')[1]
                return
            
            else:
                self.error("Failed to login. Retrying...")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue
    
    def addToCart(self):
        while True:
            self.prepare("Adding to cart...")
            
            try:
                params = {
                    "target":"ajx_basket.asp",
                    "sku":self.sizeSku,
                    "sessionid":self.sessionId,
                    "_":str(int(time.time()))
                }
            except:
                self.error(f"Failed to cart [error constructing params]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

            try:
                response = self.session.get('https://www.footasylum.com/page/xt_orderform_additem/',params=params, headers=[
                    ['user-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'],
                    ['accept','*/*'],
                    ['origin','https://www.footasylum.com'],
                    ['x-requested-with','XMLHttpRequest'],
                    ['referer','https://www.footasylum.com/page/basket/' + self.sessionId],
                ])
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue


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

            params = {
                "sessionid":self.sessionId
            }

            try:
                response = self.session.post('https://www.footasylum.com/page/nw-api/initiatecheckout/',params=params,headers=[
                    ['user-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'],
                    ['accept','text/plain, */*; q=0.01'],
                    ['origin','https://www.footasylum.com'],
                    ['x-requested-with','XMLHttpRequest'],
                    # 'referer': 'https://www.footasylum.com/page/basket/' + self.sessionId
                    ['referer','https://www.footasylum.com/page/basket/']
                ])
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue


            if response.status in [200,302]:
                try:
                    self.checkoutSessionId = response.json()["checkoutSessionId"]
                    self.basketId = response.json()["basket"]["id"]
                    self.basketCustomerId = response.json()["basket"]["customerId"]
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
                response = self.session.get('https://api.gateway.footasylum.net/basket',params=params,headers=[
                    ['user-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'],
                    ['accept','application/json'],
                    ['referer','https://secure.footasylum.com/']
                ])
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue


            if response.status == 200:
                try:
                    self.customerId = response.json()["basket"]["paraspar_customer_id"]
                    self.currency = response.json()["basket"]["currency_code"]
                    self.pasparBasketId = response.json()["basket"]["paraspar_id"]
                    self.channelId = response.json()["basket"]["channel_id"]
                    self.fascia_id = response.json()["basket"]["fascia_id"]
                    self.parasparSessionId = response.json()["basket"]["paraspar_session_id"]
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

            try:
                response = self.session.post('https://r9udv3ar7g.execute-api.eu-west-2.amazonaws.com/prod/customer/details?checkout_client=secure',json=payload,headers=[
                    ['user-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'],
                    ['accept','application/json'],
                    ['referer','https://secure.footasylum.com/?checkoutSessionId={}'.format(self.checkoutSessionId)]
                ])
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue


            if response.status == 200:
                try:
                    self.title = response.json()["customer"]["title"]
                    self.shippingDetails = response.json()["basket"]["shipping_details"]
                    self.billingDetails = response.json()["basket"]["billing_details"]
                    self.shippingMethodCode = response.json()["basket"]["shipping_method_code"]
                    self.shippingMethodName = response.json()["basket"]["shipping_method_name"]
                    self.shippingTotal = response.json()["basket"]["shipping_total"]
                    self.authState = response.json()["customer"]["session_state"]
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

    def shipping(self):
        while True:
            self.prepare("Submitting shipping...")

            try:
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
                        "title":self.title,
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
                        "title":self.title,
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
            except Exception as e:
                log.info(e)
                self.error(f"Failed to submit shipping [failed to construct payload]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

            try:
                response = self.session.post('https://r9udv3ar7g.execute-api.eu-west-2.amazonaws.com/prod/basket/basketaddaddress?checkout_client=secure',json=payload,headers=[
                    ['user-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'],
                    ['accept','application/json'],
                    ['referer','https://secure.footasylum.com/?checkoutSessionId={}'.format(self.checkoutSessionId)]
                ])
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue


            if response.status == 200:
                try:
                    self.webhookData['price'] = '{} {}'.format(response.json()["basket"]["total"],response.json()["basket"]["currency_code"])
                except Exception as e:
                    self.error(f"Failed to submit shipping [failed to parse response]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue

                self.warning("Submitted shipping")
                return
            
            else:
                self.error(f"Failed to submit shipping [{str(response.status)}]. Retrying...")
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
                response = self.session.put('https://api.gateway.footasylum.net/basket/shipping',json=payload,params=params,headers=[
                    ['user-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'],
                    ['accept','application/json'],
                    ['referer','https://secure.footasylum.com/?checkoutSessionId={}'.format(self.checkoutSessionId)]
                ])
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue


            if response.status == 200:
                try:
                    
                    self.payload = {
                        "cartId":self.pasparBasketId,
                        "customer":{
                            "firstname":response.json()["customer"]["firstname"],
                            "lastname":response.json()["customer"]["surname"],
                            "email":response.json()["customer"]["email"],
                            "mobile":response.json()["basket"]["shipping_details"]["phone"],
                            "title":response.json()["customer"]["title"],
                            "newsletter":1,
                            "sessionId":self.parasparSessionId,
                            "parasparId":self.customerId
                        },
                        "shippingAddress":{
                            "company":"",
                            "address1":response.json()["basket"]["shipping_details"]["address1"],
                            "address2":response.json()["basket"]["shipping_details"]["address2"],
                            "city":response.json()["basket"]["shipping_details"]["city"],
                            "country":response.json()["basket"]["shipping_details"]["country_name"],
                            "postcode":response.json()["basket"]["shipping_details"]["postcode"],
                            "shortCountry":response.json()["basket"]["shipping_details"]["country_id"],
                            "delivery_instructions":""
                        },
                        "billingAddress":{
                            "company":"",
                            "address1":response.json()["basket"]["billing_details"]["address1"],
                            "address2":response.json()["basket"]["billing_details"]["address2"],
                            "city":response.json()["basket"]["billing_details"]["city"],
                            "country":response.json()["basket"]["billing_details"]["country_name"],
                            "postcode":response.json()["basket"]["billing_details"]["postcode"],
                            "shortCountry":response.json()["basket"]["billing_details"]["country_id"],
                            "delivery_instructions":""
                        },
                        "authState":self.authState
                    }
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
            except Exception as e:
                log.info(e)
                self.error(f"Failed to update customer [failed to construct payload]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

            try:
                response = self.session.put('https://api.gateway.footasylum.net/customer',json=self.payload,params=params,headers=[
                    ['user-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'],
                    ['accept','application/json'],
                    ['referer','https://secure.footasylum.com/?checkoutSessionId={}'.format(self.checkoutSessionId)]
                ])
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue


            if response.status == 200:
                try:
                    fa_stat = response.json()["status"] 
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
                response = self.session.post('https://api.gateway.footasylum.net/paypal/payment-token',data=payload,headers=[
                    ['user-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'],
                    ['accept','application/json'],
                    ['referer','https://secure.footasylum.com/?checkoutSessionId={}'.format(self.checkoutSessionId)]
                ])
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue


            if response.status == 200:
                try:
                    fa_stat = response.json()["status"] 
                    pay_id = response.json()["data"]["payment_id"]
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
                response = self.session.post('https://www.paypal.com/smart/api/payment/{}/ectoken'.format(self.paymentId),json={"meta":{}},headers=[
                    ['user-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'],
                    ['accept','application/json'],
                    ['x-csrf-jwt','__blank__'],
                    ['x-requested-by','smart-payment-buttons'],
                    ['x-requested-with','XMLHttpRequest'],
                    ['content-type','application/json']
                ])
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue


            if response.status == 200:
                try:
                    pp_stat = response.json()["ack"] 
                    ecToken = response.json()["data"]["token"]
                except Exception as e:
                    self.error(f"Failed to get paypal checkout [failed to parse response]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue
                    
                if pp_stat == "success":
                    self.warning("Got paypal checkout")
                    updateConsoleTitle(False,True,SITE)
                    paypalURL = 'https://www.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token={}&useraction=commit'.format(ecToken)
                    self.webhookData['url'] = storeCookies(
                        paypalURL,self.session,
                        self.webhookData['product'],
                        self.webhookData['image'],
                        self.webhookData['price']
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
    
    

    def sendToDiscord(self):
        while True:
            
            self.webhookData['proxy'] = self.session.proxies
            sendNotification(SITE,self.webhookData['product'])
            try:
                Webhook.success(
                    webhook=loadSettings()["webhook"],
                    site=SITE,
                    url=self.webhookData['url'],
                    image=self.webhookData['image'],
                    title=self.webhookData['product'],
                    size=self.size,
                    price=self.productPrice,
                    paymentMethod=self.task['PAYMENT'].strip().title(),
                    product=self.webhookData['product_url'],
                    profile=self.task["PROFILE"],
                    proxy=self.webhookData['proxy'],
                    speed=self.webhookData['speed']
                )
                self.secondary("Sent to discord!")
                while True:
                    pass
            except:
                self.alert("Failed to send webhook. Checkout here ==> {}".format(self.webhookData['url']))
