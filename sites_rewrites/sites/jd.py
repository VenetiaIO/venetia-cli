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
    footlocker_snare,
    decodeURIComponent
)
import utils.config as CONFIG

def getCookies(jar):
    cookieString = ""
    for c in jar:
        cookieString += '{}={};'.format(c.name,c.value)
    
    return cookieString

_SITE_ = 'JD'
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

        if self.profile['countryCode'].lower() == 'gb':
            self.region = '.co.uk'
        else:
            self.region = '.' + self.profile['countryCode'].lower()


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


        if self.task['PAYMENT'].strip().lower() == "paypal":
            self.paypal()
        else:
            self.card()

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
                            sizeSplit = s['title'].split(' ')
                            allSizes.append('{}:{}:{}'.format(sizeSplit[len(sizeSplit) - 1],s['data-sku'],s['data-upc']))
                            sizes.append(sizeSplit[len(sizeSplit) - 1])
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
                self.error(f"Failed to get product [{str(response.status)}]. Retrying...")
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
                    "country":"{}|{}".format(self.profile['country'],self.profile['countryCode'].lower()),
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
                print("here")
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

    def card(self):
        while True:
            self.prepare("Completing card checkout...")
            

            try:
                response = self.session.post(f'https://www.jdsports{self.region}/checkout/paymentV3/',headers={
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                    'cookie':getCookies(self.cookieJar),
                    'x-requested-with': 'XMLHttpRequest',
                    # 'newrelic': ''
                },data="paySelect=card&isSafari=true")
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue

            self.setCookies(response)

            if response.status in [200,302]:
                redirectUrl = response.text.replace('"','').replace('\/','/')

                try:
                    response2 = self.session.get(redirectUrl,headers={
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                        'Cookie':getCookies(self.cookieJar),
                        # 'newrelic': ''
                    })
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    log.info(e)
                    self.error(f"error: {str(e)}")
                    time.sleep(int(self.task["DELAY"]))
                    self.rotateProxy()
                    continue
                
                self.setCookies(response2)
                if response2.status in [200,302]:

                    try:
                        # payload = {}
                        soup = BeautifulSoup(response2.text,"html.parser")
                        # adyeninputs = soup.find_all("input")
                        # for item in adyeninputs:
                        #     print(item)
                        #     try:
                        #         payload.update({item["name"]:item["value"]})
                        #     except:
                        #         pass
                        cM = self.profile['card']['cardMonth']
                        if len(str(cM)) == 1:
                            cM = '0' + cM
                        else:
                            pass
                        payload = {
                            "displayGroup": "card",
                            "card.cardNumber": self.profile['card']['cardNumber'],
                            "card.cardHolderName": '{} {}'.format(self.profile['firstName'], self.profile['lastName']),
                            "card.expiryMonth": cM,
                            "card.expiryYear":  self.profile['card']['cardYear'],
                            "card.cvcCode":  self.profile['card']['cardCVV'],
                            "sig": soup.find('input',{'name':'sig'})['value'],
                            "merchantReference": decodeURIComponent(redirectUrl.split('?merchantReference=')[1].split('&')[0]),
                            "brandCode": 'brandCodeUndef',
                            "paymentAmount": decodeURIComponent(redirectUrl.split('&paymentAmount=')[1].split('&')[0]),
                            "currencyCode": decodeURIComponent(redirectUrl.split('&currencyCode=')[1].split('&')[0]),
                            "shipBeforeDate": decodeURIComponent(redirectUrl.split('&shipBeforeDate=')[1].split('&')[0]),
                            "skinCode": decodeURIComponent(redirectUrl.split('&skinCode=')[1].split('&')[0]),
                            "merchantAccount": decodeURIComponent(redirectUrl.split('&merchantAccount=')[1].split('&')[0]),
                            "shopperLocale": decodeURIComponent(redirectUrl.split('&shopperLocale=')[1].split('&')[0]),
                            "stage": "pay",
                            "sessionId": soup.find('input',{'name':'sessionId'})['value'],
                            "sessionValidity": decodeURIComponent(redirectUrl.split('&sessionValidity=')[1].split('&')[0]),
                            "shopperEmail": decodeURIComponent(redirectUrl.split('&shopperEmail=')[1].split('&')[0]),
                            "shopperReference": decodeURIComponent(redirectUrl.split('&shopperReference=')[1].split('&')[0]),
                            "recurringContract": soup.find('input',{'name':'recurringContract'})['value'],
                            "resURL": decodeURIComponent(redirectUrl.split('&resURL=')[1].split('&')[0]),
                            "allowedMethods": "card",
                            "blockedMethods": decodeURIComponent(redirectUrl.split('&blockedMethods=')[1].split('&')[0]),
                            "originalSession": soup.find('input',{'name':'originalSession'})['value'],
                            "billingAddress.street": decodeURIComponent(redirectUrl.split('&billingAddress.street=')[1].split('&')[0]),
                            "billingAddress.houseNumberOrName": decodeURIComponent(redirectUrl.split('&billingAddress.houseNumberOrName=')[1].split('&')[0]),
                            "billingAddress.city": decodeURIComponent(redirectUrl.split('&billingAddress.city=')[1].split('&')[0]),
                            "billingAddress.postalCode": decodeURIComponent(redirectUrl.split('&billingAddress.postalCode=')[1].split('&')[0]),
                            "billingAddress.stateOrProvince": decodeURIComponent(redirectUrl.split('&billingAddress.stateOrProvince=')[1].split('&')[0]),
                            "billingAddress.country": decodeURIComponent(redirectUrl.split('&billingAddress.country=')[1].split('&')[0]),
                            "billingAddressType": decodeURIComponent(redirectUrl.split('&billingAddressType=')[1].split('&')[0]),
                            "billingAddressSig": decodeURIComponent(redirectUrl.split('&billingAddressSig=')[1].split('&')[0]),
                            "deliveryAddress.street": decodeURIComponent(redirectUrl.split('&deliveryAddress.street=')[1].split('&')[0]),
                            "deliveryAddress.houseNumberOrName": decodeURIComponent(redirectUrl.split('&deliveryAddress.houseNumberOrName=')[1].split('&')[0]),
                            "deliveryAddress.city": decodeURIComponent(redirectUrl.split('&deliveryAddress.city=')[1].split('&')[0]),
                            "deliveryAddress.postalCode": decodeURIComponent(redirectUrl.split('&deliveryAddress.postalCode=')[1].split('&')[0]),
                            "deliveryAddress.stateOrProvince": decodeURIComponent(redirectUrl.split('&deliveryAddress.stateOrProvince=')[1].split('&')[0]),
                            "deliveryAddress.country": decodeURIComponent(redirectUrl.split('&deliveryAddress.country=')[1].split('&')[0]),
                            "deliveryAddressType": decodeURIComponent(redirectUrl.split('&deliveryAddressType=')[1].split('&')[0]),
                            "deliveryAddressSig": decodeURIComponent(redirectUrl.split('&deliveryAddressSig=')[1].split('&')[0]),
                            "shopper.firstName": decodeURIComponent(redirectUrl.split('&shopper.firstName=')[1].split('&')[0]),
                            "shopper.lastName": decodeURIComponent(redirectUrl.split('&shopper.lastName=')[1].split('&')[0]),
                            "merchantIntegration.type": "HPP",
                            "referrerURL": f'https://www.jdsports{self.region}/',
                            "dfValue": "ryEGX8eZpJ0030000000000000BTWDfYZVR30089146776cVB94iKzBGcnZqsrHIWv5S16Goh5Mk0045zgp4q8JSa00000qZkTE00000q6IQbnyNfpG2etdcqzfW:40",
                            "usingFrame": False,
                            "usingPopUp": False,
                            "shopperBehaviorLog": {"numberBind":"1","holderNameBind":"1","cvcBind":"1","deactivate":"4","activate":"3"}
                        }
                        # payload["displayGroup"] = "card"
                        # payload["dfValue"] = "ryEGX8eZpJ0030000000000000BTWDfYZVR30089146776cVB94iKzBGcnZqsrHIWv5S16Goh5Mk0045zgp4q8JSa00000qZkTE00000q6IQbnyNfpG2etdcqzfW:40",
                        # payload["brandCode"] = 'brandCodeUndef'
                        # payload["displayGroup"] = "card"
                        # payload["card.cardNumber"] = self.profile['card']['cardNumber']
                        # payload["card.cardHolderName"] = "{} {}".format(self.profile['firstName'], self.profile['lastName'])
                        # payload["card.cvcCode"] = self.profile['card']['cardCVV']
                        # payload["card.expiryMonth"] = self.profile['card']['cardMonth']
                        # payload["card.expiryYear"] = self.profile['card']['cardYear']
                        # payload["shopperBehaviorLog"] = {"numberBind":"1","holderNameBind":"1","cvcBind":"1","deactivate":"3","activate":"2","numberFieldFocusCount":"2","numberFieldLog":"fo@42,cl@42,cl@261,bl@347,fo@494,Cd@498,KL@499,Cu@500,ch@512,bl@512","numberFieldClickCount":"2","numberFieldBlurCount":"2","numberFieldKeyCount":"2","numberFieldChangeCount":"1","numberFieldEvHa":"total=0","holderNameFieldFocusCount":"1","holderNameFieldLog":"fo@512,cl@512,Sd@522,KL@525,KL@526,Su@526,KL@527,KL@528,Ks@530,Sd@531,Su@534,Kb@535,Kb@536,Kb@538,Kb@539,KL@543,KL@544,KL@545,Ks@548,Sd@549,KL@550,Su@551,KL@551,KL@553,KL@555,KL@556,KL@557,KL@558,KL@559,KU@560,ch@560,bl@560","holderNameFieldClickCount":"1","holderNameFieldKeyCount":"25","holderNameUnkKeysFieldLog":"9@560","holderNameFieldChangeCount":"1","holderNameFieldEvHa":"total=0","holderNameFieldBlurCount":"1","cvcFieldFocusCount":"1","cvcFieldLog":"fo@624,cl@625,KN@653,KN@656,KN@657,ch@672,bl@672","cvcFieldClickCount":"1","cvcFieldKeyCount":"3","cvcFieldChangeCount":"1","cvcFieldEvHa":"total=0","cvcFieldBlurCount":"1"}
                    except Exception:
                        self.error('Failed to checkout [failed to construct form]. Retrying...')
                        time.sleep(int(self.task["DELAY"]))
                        continue
                    
     
                    try:
                        response3 = self.session.post('https://live.adyen.com/hpp/completeCard.shtml',headers={
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                            'Accept-Language': 'en-US,en;q=0.9',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                            'Cookie':getCookies(self.cookieJar),
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'Referer':redirectUrl
                            # 'newrelic': ''
                        },data=payload)
                    except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                        log.info(e)
                        self.error(f"error: {str(e)}")
                        time.sleep(int(self.task["DELAY"]))
                        self.rotateProxy()
                        continue

                    self.setCookies(response3)

                    
                    print(response3.text)
                    print(response3.url)
                    print(response3.status)
                    sys.exit()
                        
                
                else:
                    self.error(f"Failed to complete card checkout [{str(response.status)}]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue


            elif response.status == 403:
                self.error(f"Failed to complete card checkout [{str(response.status)}]. Retrying...")
                self.rotateProxy()
                time.sleep(int(self.task['DELAY']))
                continue
                
            else:
                self.error(f"Failed to complete card checkout [{str(response.status)}]. Retrying...")
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
                while True:
                    pass