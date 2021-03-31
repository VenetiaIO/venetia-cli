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
from requests_toolbelt import MultipartEncoder
import http.cookiejar

from utils.captcha import captcha
from utils.logger import logger
from utils.webhook import Webhook
from utils.log import log
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
    footlocker_snare
)
import utils.config as CONFIG

def getCookies(jar):
    cookieString = ""
    for c in jar:
        cookieString += '{}={};'.format(c.name,c.value)
    
    return cookieString

SITE = 'JDSports'
class JD:
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
            with open('./{}/tasks.csv'.format('JD'.lower()),'r') as csvFile:
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

    def rotateProxy(self):
        self.proxy = loadProxy2(self.task["PROXIES"],self.taskID,SITE)
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


        self.profile = loadProfile(self.task["PROFILE"])
        if self.profile == None:
            self.error("Profile Not found. Exiting...")
            time.sleep(10)
            sys.exit()

        self.region = '.co.uk'


        self.prodUrl = f'https://www.jdsports{self.region}/product/-/' + self.task['PRODUCT'] + '/stock/?_=' + str(int(time.time()))

        self.tasks()

    def setCookies(self,response):
        for c in response.cookies:
            self.cookieJar.set_cookie(http.cookiejar.Cookie(
                version=0,
                name=c,
                value=response.cookies[c],
                port=None,
                port_specified=False,
                domain="www.offspring.co.uk",
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
    

    
    def tasks(self):

        self.monitor()
        self.addToCart()
        self.guestCheckout()
        # self.deliveryMethod()
        self.shipping()
        # self.updateDelivery_plus_method()

        self.paypal()

        # if self.task['PAYMENT'].strip().lower() == "paypal":
        #     self.paypal()
        # else:
        #     self.card()

        self.sendToDiscord()
    
    def monitor(self):
        while True:
            self.prepare("Getting Product...")

            try:
                response = self.session.get(self.prodUrl,headers={
                    'accept': '*/*',
                    # 'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/json',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                    'cookie':getCookies(self.cookieJar),
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                self.rotateProxy()
                time.sleep(int(self.task["DELAY"]))
                continue
            
            self.setCookies(response)
            if response.status == 200:
                self.start = time.time()

                self.warning("Retrieved Product")

                try:
                    soup = BeautifulSoup(response.text, "html.parser")

                    foundSizes = soup.find_all('button',{'data-e2e':'pdp-productDetails-size'})

                    allSizes = []
                    sizes = []
                    for s in foundSizes:
                        try:
                            allSizes.append('{}:{}:{}'.format(s['title'].split(' ')[2],s['data-sku'],s['data-upc']))
                            sizes.append(s['title'].split(' ')[2])
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
                                    self.size = size.split(':')[0]
                                    self.sizeSKU = size.split(':')[1]
                                    self.sizeUPC = size.split(":")[2]
                                    
                                    self.warning(f"Found Size => {self.size}")
        
                    else:
                        selected = random.choice(allSizes)
                        self.size = selected.split(":")[0]
                        self.sizeSKU = selected.split(":")[1]
                        self.sizeUPC = selected.split(":")[2]
                        
                        self.warning(f"Found Size => {self.size}")

                except Exception as e:
                    log.info(e)
                    self.error("Failed to parse product data (maybe OOS)")
                    time.sleep(int(self.task['DELAY']))
                    continue

                return

            elif response.status == 403:
                self.error(f"Failed to cart [{str(response.status)}]. Retrying...")
                self.rotateProxy()
                time.sleep(int(self.task['DELAY']))
                continue
                    
            else:
                self.error(f"Failed to get product [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def addToCart(self):
        while True:
            self.prepare("Adding to cart...")
            
            try:
                response = self.session.post(f'https://www.jdsports{self.region}/cart/{self.sizeSKU}/',headers={
                    'accept': '*/*',
                    'referer':f'https://www.jdsports{self.region}/product/-/' + self.task['PRODUCT'],
                    # 'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/json',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                    'cookie':getCookies(self.cookieJar),
                    'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjEwNDEzNTUiLCJhcCI6Ijg4OTU5MjA1IiwiaWQiOiJjYjI5YjRjNTUxMDVlYTZiIiwidHIiOiJmYWU5NzQwNzgwYjg0YTliIiwidGkiOjE2MTcyMzE3OTc3ODZ9fQ=='
                },data=json.dumps({
                    "customisations":False,
                    "cartPosition":'null',
                    "recaptchaResponse":False,
                    "cartProductNotification":'null',
                    "quantityToAdd":1
                }))
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue

            self.setCookies(response)
            if response.status == 200:
                try:
                    responseBody = json.loads(response.text)
                    self.deliveryData = responseBody['delivery']
                    self.cartID = responseBody['ID']
                    self.webhookData['product'] = responseBody['contents'][0]['name']
                    self.webhookData['price'] = '{} {}'.format(responseBody['productsSubtotal']['amount'],responseBody['productsSubtotal']['currency'])
                    self.webhookData['image'] = responseBody['contents'][0]['image']['originalURL']
                except Exception as e:
                    self.error("Failed to cart [failed to parse response]. Retrying...")
                    log.info(e)
                    time.sleep(int(self.task["DELAY"]))
                    continue

                self.success("Added to cart!")
                updateConsoleTitle(True,False,SITE)
                return

            elif response.status == 403:
                self.cookieJar.clear()
                self.error(f"Failed to cart [{str(response.status)}]. Retrying...")
                self.rotateProxy()
                time.sleep(int(self.task['DELAY']))
                continue
                
            
            else:
                self.error(f"Failed to cart [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def guestCheckout(self):
        while True:
            self.prepare("Setting email...")
                

            try:
                response = self.session.post(f'https://www.jdsports{self.region}/checkout/guest/',headers={
                    'accept': '*/*',
                    # 'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/json',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                    'cookie':getCookies(self.cookieJar),
                    'newrelic': ''
                },data=json.dumps({
                    "email":self.profile['email']
                }))
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue

            self.setCookies(response)
            if response.status == 200:
                try:
                    responseBody = json.loads(response.text)
                    message = responseBody['message']
                except Exception as e:
                    self.error("Failed to set email [failed to parse response]. Retrying...")
                    log.info(e)
                    time.sleep(int(self.task["DELAY"]))
                    continue
                
                if message.lower() == 'success':
                    self.warning("Set email")
                    return
                else:
                    self.error(f"Failed to set email [{message}]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue

            elif response.status == 403:
                self.error(f"Failed to set email [{str(response.status)}]. Retrying...")
                self.rotateProxy()
                time.sleep(int(self.task['DELAY']))
                continue
                
            else:
                self.error(f"Failed to set email [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def deliveryMethod(self):
        while True:
            self.prepare("Setting delivery method...")
                
            data = str(json.dumps({
                "deliveryMethodID":self.deliveryData["deliveryMethodID"],
                "deliveryLocation":self.profile['countryCode'].lower()
            }))
            try:
                response = self.session.put(f'https://www.jdsports{self.region}/cart/',headers={
                    'accept': '*/*',
                    # 'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                    'cookie':getCookies(self.cookieJar),
                    'newrelic': ''
                },data=data)
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue

            self.setCookies(response)

            if response.status == 200:
                try:
                    responseBody = json.loads(response.text)
                except Exception as e:
                    self.error("Failed to set delivery method [failed to parse response]. Retrying...")
                    log.info(e)
                    time.sleep(int(self.task["DELAY"]))
                    continue
                
                self.warning("Set delivery method")
                return

            elif response.status == 403:
                self.error(f"Failed to set delivery method [{str(response.status)}]. Retrying...")
                self.rotateProxy()
                time.sleep(int(self.task['DELAY']))
                continue
                
            else:
                self.error(f"Failed to set delivery method [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def shipping(self):
        while True:
            self.prepare("Setting shipping...")
            
            

            try:
                response = self.session.post(f'https://www.jdsports{self.region}/myaccount/addressbook/add/',headers={
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/json',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                    'cookie':getCookies(self.cookieJar),
                    # 'newrelic': ''
                },data=json.dumps({
                    "useDeliveryAsBilling":True,
                    "country":"United Kingdom|gb",
                    "locale":"",
                    "firstName":self.profile['firstName'],
                    "lastName":self.profile['lastName'],
                    "phone":self.profile['phone'],
                    "address1":'{} {}'.format(self.profile['house'], self.profile['addressOne']),
                    "address2":self.profile['addressTwo'],
                    "town":self.profile['city'],
                    "county":self.profile['region'],
                    "postcode":self.profile['zip'],
                    "addressPredict":"",
                    "setOnCart":"deliveryAddressID",
                    "addressPredictflag":"false"
                }))
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue

            self.setCookies(response)
            if response.status in [200,201]:
                try:
                    responseBody = json.loads(response.text)
                    self.addressId = responseBody['ID']
                except Exception as e:
                    self.error("Failed to set shipping [failed to parse response]. Retrying...")
                    log.info(e)
                    time.sleep(int(self.task["DELAY"]))
                    continue
                
                self.warning("Set shipping")
                return

            elif response.status == 403:
                self.error(f"Failed to cart [{str(response.status)}]. Retrying...")
                self.rotateProxy()
                time.sleep(int(self.task['DELAY']))
                continue
                
            else:
                self.error(f"Failed to set shipping [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def updateDelivery_plus_method(self):
        while True:
            self.prepare("Updating Delivery & Method")
            
            

            try:
                response = self.session.post(f'https://www.jdsports{self.region}/checkout/updateDeliveryAddressAndMethod/ajax/',headers={
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/json',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                    'cookie':getCookies(self.cookieJar),
                    # 'newrelic': ''
                },data=json.dumps({
                    # "useDeliveryAsBilling":True,
                    "addressId":self.addressId,
                    "locale":{},
                    "methodId":self.deliveryData["deliveryMethodID"],
                }))
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue

            self.setCookies(response)
            if response.status in [200,201]:
                try:
                    responseBody = json.loads(response.text)
                except Exception as e:
                    self.error("Failed to update delivery & method [failed to parse response]. Retrying...")
                    log.info(e)
                    time.sleep(int(self.task["DELAY"]))
                    continue
                
                self.warning("Updated delivery & method")
                return

            elif response.status == 403:
                self.error(f"Failed to update delivery & method [{str(response.status)}]. Retrying...")
                self.rotateProxy()
                time.sleep(int(self.task['DELAY']))
                continue
                
            else:
                self.error(f"Failed to update delivery & method [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def paypal(self):
        while True:
            self.prepare("Getting paypal checkout...")
            

            try:
                response = self.session.get(f'https://www.jdsports{self.region}/checkout/payment/?paySelect=paypalViaHosted',headers={
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/json',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                    'cookie':getCookies(self.cookieJar),
                    # 'newrelic': ''
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
                    response2 = self.session.get(response.url,headers={
                        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "accept-language": "en-US,en;q=0.9",
                        "sec-ch-ua": "\"Google Chrome\";v=\"89\", \"Chromium\";v=\"89\", \";Not A Brand\";v=\"99\"",
                        "sec-ch-ua-mobile": "?0",
                        "sec-fetch-dest": "document",
                        "sec-fetch-mode": "navigate",
                        "sec-fetch-site": "cross-site",
                        "sec-fetch-user": "?1",
                        "upgrade-insecure-requests": "1",
                        'Cookie':getCookies(self.cookieJar),
                        'Referer':f'https://www.jdsports{self.region}',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                        # 'newrelic': ''
                    })
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    log.info(e)
                    self.error(f"error: {str(e)}")
                    time.sleep(int(self.task["DELAY"]))
                    self.rotateProxy()
                    continue
                
                if response2.status in [200,302] and 'paypal' in response2.url:
                    self.end = time.time() - self.start
                    self.webhookData['speed'] = self.end

                    self.success("Got paypal checkout!")
                    updateConsoleTitle(False,True,SITE)

                    self.webhookData['url'] = storeCookies(
                        response2.url,self.cookieJar,
                        self.webhookData['product'],
                        self.webhookData['image'],
                        self.webhookData['price'],
                        True
                    )
                    return
                
                else:
                    self.error(f"Failed to get paypal checkout [{str(response.status)}]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue  
         

            elif response.status == 403:
                self.error(f"Failed to get paypal checkout [{str(response.status)}]. Retrying...")
                self.rotateProxy()
                time.sleep(int(self.task['DELAY']))
                continue
                
            else:
                self.error(f"Failed to get paypal checkout [{str(response.status)}]. Retrying...")
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
                    region=self.profile['countryCode'].lower(),
                    size=self.size,
                    price=self.webhookData['price'],
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
