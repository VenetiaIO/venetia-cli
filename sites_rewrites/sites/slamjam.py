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

_SITE_ = 'SLAMJAM'
SITE = 'SlamJam'
class SLAMJAM:
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

    def __init__(self, task, taskName, rowNumber):
        self.task = task
        self.taskID = taskName
        self.rowNumber = rowNumber

        if self.rowNumber != 'qt': 
            threading.Thread(target=self.task_checker,daemon=True).start()

        try:
            # self.session = client.Session(browser=client.Fingerprint.CHROME_83)
            self.session = scraper()
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
            "product_url":""
        }

        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)

        self.profile = loadProfile(self.task["PROFILE"])
        if self.profile == None:
            self.error("Profile Not found. Exiting...")
            time.sleep(10)
            sys.exit()
        self.region = self.profile['countryCode'].upper()
        
        if 'https' in self.task["PRODUCT"]:
            self.pid = self.task['PRODUCT'].split('.html')[0].split('/')[ len(self.task['PRODUCT'].split('.html')[0].split('/')) - 1]
            self.prodUrl = self.task["PRODUCT"]
        else:
            self.pid = self.task['PRODUCT']
            self.prodUrl = 'https://www.slamjam.com/en_{}/{}.html'.format(self.region,self.task["PRODUCT"])


        self.webhookData['product_url'] = self.prodUrl
        self.queryString = f'https://www.slamjam.com/on/demandware.store/Sites-slamjam-Site/en_{self.region}/Product-Variation?pid={self.pid}'
        self.tasks()
    
    def tasks(self):

        self.monitor()
        # self.addToCart()


        # self.sendToDiscord()

    def monitor(self):
        while True:
            self.prepare("Getting Product...")


            try:
                response = self.session.get(self.prodUrl)
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue

            try:
                response2 = self.session.get(self.queryString,headers={
                    "accept": "*/*",
                    "accept-language": "en-US,en;q=0.9",
                    "sec-ch-ua": "\"Google Chrome\";v=\"89\", \"Chromium\";v=\"89\", \";Not A Brand\";v=\"99\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "x-requested-with": "XMLHttpRequest",
                    "referer":str(response.url)
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue

            if response.status_code == 200 and response2.status_code == 200:
                self.start = time.time()

                self.warning("Retrieved Product")

                # try:
                soup = BeautifulSoup(response.text, "html.parser")

                with open('sj.html','w') as f:
                    f.write(response.text)
                    f.close()

                self.csrf = soup.find('input',{'name':'csrf_token'})['value']

                categorys = soup.find_all("li",{"class":"breadcrumb-item"})
                self.productCategory = categorys[len(categorys) -1].find('a').find('span').text

                self.webhookData['product'] = str(soup.find("h1",{"class":"product-name"}).text)
                self.webhookData['image'] = str(soup.find("div", {"class": "slider-data-large"}).find_all('div')[0]['data-image-url'])
                self.webhookData['price'] = str(soup.find("span",{"class":"value"}).text.strip())

                print(response2)
                print(response2.url)
                data = response2.text
                print(data)
                self.uuid = data["product"]["uuid"]
                # self.productTitle = data["product"]["productName"]
                # self.productPrice = data["product"]["price"]["sales"]["formatted"]
                # self.productImage = data["product"]["images"]["hi-res"][0]["absURL"]

                sizeData = data["product"]["variationAttributes"][1]["values"]

                allSizes = []
                sizes = []
                for s in sizeData:
                    # SIZE : SIZE ID : SIZE PRODUCT ID : IN STOCK (TRUE / FALSE )
                    if s["selectable"] == True:
                        allSizes.append('{}:{}:{}:{}'.format(s["displayValue"],s["id"],s["productID"],s["selectable"]))
                        sizes.append(s["displayValue"])


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
                                self.sizeID = size.split(':')[1]
                                self.sizeProductID = size.split(":")[2]
                                
                                self.warning(f"Found Size => {self.size}")
    
                else:
                    selected = random.choice(allSizes)
                    self.size = selected.split(':')[0]
                    self.sizeID = selected.split(':')[1]
                    self.sizeProductID = selected.split(":")[2]
                    
                    self.warning(f"Found Size => {self.size}")

                # except Exception as e:
                #     log.info(e)
                #     self.error("Failed to parse product data (maybe OOS)")
                #     time.sleep(int(self.task['DELAY']))
                #     continue

                return
                    
            else:
                self.error(f"Failed to get product [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def addToCart(self):
        while True:
            self.prepare("Adding to cart...")
            
            boundary = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=16))
            payload = {
                'isAjax':'1',
                'form_key': self.formKey,
                'product': self.productId,
                'related_product': '',
                f'super_attribute[{self.attributeId}]': self.sizeID,
                'product_id': '',
                'email_notification': '',
                'parent_id': self.productId

            }
            payload_encoded = MultipartEncoder(payload, boundary=f'----WebKitFormBoundary{boundary}')
            

            try:
                response = self.session.post(self.atcUrl, data=payload_encoded.to_string(), headers={
                    'authority': 'www.allikestore.com',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': f'multipart/form-data; boundary=----WebKitFormBoundary{boundary}',
                    'origin': 'https://www.allikestore.com',
                    'referer': self.task["PRODUCT"],
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'x-requested-with': 'XMLHttpRequest',
                    'accept':'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue


            try:
                splitText = response.text.split('({')[1].split('})')[0]
                data = json.loads('{' + splitText + '}')
                status_code = data["status"]
            except Exception as e:
                log.info(e)
                self.error("Failed to cart [failed to parse response]. Retrying...")
                time.sleep(int(self.task["DELAY"]))
                continue

            if response.status_code == 200 and status_code == "SUCCESS":
                self.success("Added to cart!")
                updateConsoleTitle(True,False,SITE)
                return
            
            else:
                self.error(f"Failed to cart [{str(response.status_code)}]. Retrying...")
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
