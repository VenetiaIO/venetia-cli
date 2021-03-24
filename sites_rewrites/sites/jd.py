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

from utils.captcha import captcha
from utils.logger import logger
from utils.webhook import Webhook
from utils.log import log
from utils.functions import (
    loadSettings,
    loadProfile,
    loadProxy,
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

SITE = 'JD'
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

        self.profile = loadProfile(self.task["PROFILE"])
        if self.profile == None:
            self.error("Profile Not found. Exiting...")
            time.sleep(10)
            sys.exit()

        if 'https' in self.task['PRODUCT']:
            self.prodUrl = self.task['PRODUCT']
        else:
            self.prodUrl = f'https://www.jdsports{self.region}/product/-/' + self.task['PRODUCT'] + '/stock/?_=' + str(int(time.time()))

        self.tasks()
    
    def tasks(self):

        self.monitor()
        self.addToCart()
        self.guestCheckout()

        # if self.task['PAYMENT'].strip().lower() == "paypal":
        #     self.paypal()
        # else:
        #     self.card()

        # self.sendToDiscord()

    def monitor(self):
        while True:
            self.prepare("Getting Product...")

            self.region = '.co.uk'
            try:
                response = self.session.get(self.prodUrl,headers={
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/json',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue

            if response.status_code == 200:
                self.start = time.time()

                self.warning("Retrieved Product")

                try:
                    soup = BeautifulSoup(response.text, "html.parser")

                    self.webhookData['product'] = str(soup.find("title").text)
                    self.webhookData['image'] = str(soup.find("img", {"id": "image-0"})["src"])
                    self.webhookData['price'] = str(soup.find("span",{"class":"price"}).text)

                    self.atcUrl = soup.find("form", {"id": "product_addtocart_form"})["action"].replace("checkout/cart", "oxajax/cart")
                    self.formKey = soup.find("input", {"name": "form_key"})["value"]
                    self.productId = soup.find("input", {"name": "product"})["value"]
                    self.attributeId = soup.find("select", {"class": "required-entry super-attribute-select no-display swatch-select"})["id"].split("attribute")[1]

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
                    
            else:
                self.error(f"Failed to get product [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def addToCart(self):
        while True:
            self.prepare("Adding to cart...")
            
            

            try:
                response = self.session.post(f'https://www.jdsports{self.region}/cart/{self.sizeSKU}/',headers={
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/json',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                    'newrelic': ''
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
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue


            if response.status_code == 200:
                try:
                    responseBody = json.loads(response.text)
                    self.deliveryData = responseBody['delivery']
                    self.cartID = responseBody['ID']
                    self.productTitle = responseBody['contents'][0]['name']
                    self.productPrice = '{} {}'.format(responseBody['productsSubtotal']['amount'],responseBody['productsSubtotal']['currency'])
                    self.productImage = responseBody['contents'][0]['image']['originalURL']
                except Exception as e:
                    self.error("Failed to cart [failed to parse response]. Retrying...")
                    log.info(e)
                    time.sleep(int(self.task["DELAY"]))
                    continue

                self.success("Added to cart!")
                updateConsoleTitle(True,False,SITE)
                return
            
            else:
                self.error(f"Failed to cart [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def guestCheckout(self):
        while True:
            self.prepare("Setting email...")
            
            

            try:
                response = self.session.post(f'https://www.jdsports{self.region}/checkout/guest/',headers={
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/json',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                    'newrelic': ''
                },data=json.dumps({
                    "email":self.profile['email']
                }))
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue


            if response.status_code == 200:
                try:
                    responseBody = json.loads(response.text)
                    print(responseBody)
                except Exception as e:
                    self.error("Failed to set email [failed to parse response]. Retrying...")
                    log.info(e)
                    time.sleep(int(self.task["DELAY"]))
                    continue

                self.success("Set email")
                updateConsoleTitle(True,False,SITE)
                return
            
            else:
                self.error(f"Failed to set email [{str(response.status_code)}]. Retrying...")
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
