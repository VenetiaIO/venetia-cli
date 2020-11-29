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
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, injection, updateConsoleTitle, scraper)
SITE = 'OVERKILL'

class OVERKILL:
    def __init__(self, task,taskName):
        self.task = task
        self.sess = requests.session()
        self.taskID = taskName

        twoCap = loadSettings()["2Captcha"]
        self.session = scraper()
        
        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)

        self.collect()

    def collect(self):
        logger.prepare(SITE,self.taskID,'Getting product page...')
        try:
            retrieve = self.session.get(self.task["PRODUCT"], headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'

            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.collect()

        if retrieve.status_code == 200:
            logger.success(SITE,self.taskID,'Got product page')
            try:
                soup = BeautifulSoup(retrieve.text, "html.parser")
                self.productTitle = soup.find("title").text.split('(')[0]
                self.productImage = soup.find("a", {"data-present": ".carousel-inner"})["href"]
                self.atcUrl = soup.find("form", {"id": "product_addtocart_form"})["action"]
                self.formKey = soup.find("input", {"name": "form_key"})["value"]
                self.productId = soup.find("input", {"name": "product"})["value"]
                self.productPrice = soup.find("span",{"class":"price"}).text
                self.attributeId = soup.find("select", {
                                            "class": "row-fluid required-entry super-attribute-select"})["id"].split("attribute")[1]
    
                regex = r"{\"attributes\":(.*?)}}\)"
                matches = re.search(regex, retrieve.text, re.MULTILINE)
                if matches:
                    productData = json.loads(
                        matches.group()[:-1])["attributes"][self.attributeId]
    
                    allSizes = []
                    sizes = []
                    for s in productData["options"]:
                        allSizes.append('{}:{}:{}'.format(s["label_uk"],s["products"][0],s["id"]))
                        sizes.append(s["label"])
    
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
                                if size.split(':')[0] == self.task["SIZE"]:
                                    self.size = size.split(':')[0]
                                    self.sizeID = size.split(':')[2]
                                    self.option = size.split(":")[1]
                                    logger.success(SITE,self.taskID,f'Found Size => {self.size}')
        
                    
                    elif self.task["SIZE"].lower() == "random":
                        selected = random.choice(allSizes)
                        self.size = selected.split(":")[0]
                        self.sizeID = selected.split(":")[2]
                        self.option = selected.split(":")[1]
                        logger.success(SITE,self.taskID,f'Found Size => {self.size}')

                    self.addToCart()
                
                else:
                    logger.error(SITE,self.taskID,'Size Not Found')
                    time.sleep(int(self.task["DELAY"]))
                    self.collect()

                        
            except Exception as e:
               log.info(e)
               logger.error(SITE,self.taskID,'Failed to scrape page (Most likely out of stock). Retrying...')
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

    def addToCart(self):
        payload = {
            'product': self.productId,
            'related_product': '',
            'form_key': self.formKey,
            f'super_attribute[{self.attributeId}]': self.sizeID,
            'qty': '1',
            'gpc_add':'1'
        }

        try:
            postCart = self.session.post(self.atcUrl, data=payload, headers={
                'authority': 'www.overkillshop.com',
                'accept-language': 'en-US,en;q=0.9',
                'origin': 'https://www.overkillshop.com',
                'referer': self.task["PRODUCT"],
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()

        try:
            json = postCart.json()
        except:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

        if postCart.status_code == 200 and json["success"] == True:
            logger.success(SITE,self.taskID,'Successfully carted')
            self.method()
        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

    def method(self):
        try:
            postMethod = self.session.post('ttps://www.overkillshop.com/en/checkout/onepage/saveMethod/', data={"method": "guest"}, headers={
                'authority': 'www.overkillshop.com',
                'referer': 'https://www.overkillshop.com/en/checkout/onepage/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
                'accept':'text/javascript, text/html, application/xml, text/xml, */*'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.method()

        if postMethod.status_code == 200:
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
            'billing[street][]':profile["house"] + " " + profile["addressOne"],
            'billing[street_number]': profile["house"],
            'billing[street][]': profile["addressTwo"],
            'billing[street][]': '',
            'billing[postcode]': profile["zip"],
            'billing[region_id]': '',
            'billing[region]': profile["region"],
            'billing[city]': profile["city"],
            'billing[country_id]': countryCode,
            'billing[email]': profile["email"],
            'billing[telephone]': profile["phone"],
            'billing[fax]': '',
            'billing[customer_password]': '',
            'billing[confirm_password]': '',
            'billing[save_in_address_book]': 1,
            'billing[use_for_shipping]': 1
        }

        try:
            postBilling = self.session.post('https://www.overkillshop.com/en/checkout/onepage/saveBilling/', data=payload, headers={
                'authority': 'www.overkillshop.com',
                'accept-language': 'en-US,en;q=0.9',
                'origin': 'https://www.overkillshop.com',
                'referer': 'https://www.overkillshop.com/en/checkout/onepage/',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
                'accept': 'text/javascript, text/html, application/xml, text/xml, */*'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
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
                self.shippingMethods = soup.find_all('input',{'class':'radio'})
                #self.shippingMethod = shippingMethods[0]["value"]
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

  