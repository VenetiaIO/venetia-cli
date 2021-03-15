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

        self.profile = loadProfile(self.task["PROFILE"])
        if self.profile == None:
            self.error("Profile Not found. Exiting...")
            time.sleep(10)
            sys.exit()

        self.tasks()
    
    def tasks(self):

        self.monitor()
        self.addToCart()
        self.startSession()


        # if self.task['PAYMENT'].strip().lower() == "paypal":
        #     self.paypal()
        # else:
        #     self.card()

        # self.sendToDiscord()

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
                                        return
            
                        else:
                            selected = random.choice(allSizes)
                            self.size = selected.split('#')[0]
                            self.sizeSku = selected.split('#')[1]
                            self.sizeColour = selected.split("#")[2]
                            
                            self.webhookData['product'] = selected.split("#")[5]
                            self.webhookData['image'] = selected.split("#")[4]
                            self.webhookData['price'] = selected.split("#")[3]


                            self.warning(f"Found Size => {self.size}")
                            return

                        

                    else:
                        raise Exception

                except Exception as e:
                    log.info(e)
                    self.error("Failed to parse product data (maybe OOS)")
                    time.sleep(int(self.task['DELAY']))
                    continue
                    
            else:
                self.error(f"Failed to get product [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def addToCart(self):
        while True:
            self.prepare("Adding to cart...")
            
            params = {
                "target":"ajx_basket.asp",
                "sku":self.sizeSku,
                "_":int(time.time())
            }
            try:
                response = self.session.post('https://www.footasylum.com/page/xt_orderform_additem/', params=params, headers={
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
                    'accept': '*/*',
                    'referer':'https://www.footasylum.com',
                    # 'referer':'{}?sessionid={}'.format(self.task["PRODUCT"],self.sessionId),
                    'authority': 'www.footasylum.com',
                    'x-requested-with': 'XMLHttpRequest'
                })
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
                print(response.text)
                time.sleep(100)
                self.error(f"Failed to cart [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def startSession(self):
        while True:
            self.prepare("Getting checkout session...")

            try:
                response = self.session.post('https://www.footasylum.com/page/nw-api/initiatecheckout/', headers={
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                    'accept': 'text/plain, */*; q=0.01',
                    'origin':'https://www.footasylum.com',
                    'x-requested-with': 'XMLHttpRequest',
                    # 'referer': 'https://www.footasylum.com/page/basket/' + self.sessionId
                    'referer':'https://www.footasylum.com/page/basket/'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue


            if response.status in [200,302]:
                print(response.status)
                print(response.url)
                self.warning("Got session")
                return
            
            else:
                self.error(f"Failed to get session [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    

    def sendToDiscord(self):
        while True:
            
            self.webhookData['proxy'] = self.session.proxies
            sendNotification(SITE,self.productTitle)
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
