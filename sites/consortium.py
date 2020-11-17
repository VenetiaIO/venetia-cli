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
# import binascii
# from collections import OrderedDict
# from Cryptodome.Cipher import AES

from utils.logger import logger
from utils.webhook import discord
from utils.log import log
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection, updateConsoleTitle)
SITE = 'CONSORTIUM'



def solveAES(response):
    if 'slowAES.decrypt' in response.text:
        try:
            cryptVars = OrderedDict(re.findall(r'(a|b|c)=toNumbers\("(.*?)"\)', response.text))

            check = binascii.hexlify(
                AES.new(
                    binascii.unhexlify(cryptVars['a']),
                    AES.MODE_CBC,
                    binascii.unhexlify(cryptVars['b'])
                ).decrypt(
                    binascii.unhexlify(cryptVars['c'])
                )
            ).decode('ascii')

            data = {
                'url': response.text.split('location.href="')[1].split('"')[0],
                'cookie': [
                    response.text.split('document.cookie="')[1].split('=')[0],
                    check
                ]
            }
            print(data)

            return data
        except:
            return 0
    else:
        return 0
    

class CONSORTIUM:
    def __init__(self, task,taskName):
        self.task = task
        self.sess = requests.session()
        self.taskID = taskName

        twoCap = loadSettings()["2Captcha"]
        self.session = cloudscraper.create_scraper(
            requestPostHook=injection,
            sess=self.sess,
            interpreter='nodejs',
            captcha={
                'provider': '2captcha',
                'api_key': twoCap
            }
        )

        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
        self.session.headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }

        self.collect()

    def collect(self):
        #logger.warning(SITE,self.taskID,'Solving Cloudflare...')
        try:
            retrieve = self.session.get(self.task["PRODUCT"])
            #logger.success(SITE,self.taskID,'Solved Cloudflare')
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.collect()


        if 'slowAES' in retrieve.text:
            #solve challenge
            solveAES(retrieve.text)
        else:
            if retrieve.status_code == 200:
                logger.success(SITE,self.taskID,'Got product page')
                try:
                    soup = BeautifulSoup(retrieve.text, "html.parser")
                    self.productId = soup.find('input',{'name':'product'})["value"]
                    self.formKey = soup.find('input',{'name':'form_key'})["value"]
                    self.productUrlKey = soup.find('input',{'name':'full_product_url_key'})["value"]
                    self.attributeId = soup.find("select", {"class": "required-entry super-attribute-select"})["id"].split("attribute")[1]
        
                    regex = r"{\"attributes\":(.*?)}}\)"
                    matches = re.search(regex, retrieve.text, re.MULTILINE)
                    if matches:
                        productData = json.loads(
                            matches.group()[:-1])["attributes"][self.attributeId]
        
                        allSizes = []
                        sizes = []
                        for s in productData["options"]:
                            size = s["label"].split('UK ')[1]
                            allSizes.append('{}:{}:{}'.format(s["label"],size,s["id"]))
                            sizes.append(size)
        
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
                                    if size.split(':')[1] == self.task["SIZE"]:
                                        self.size = size.split(':')[0]
                                        self.sizeID = size.split(':')[2]
                                        logger.success(SITE,self.taskID,f'Found Size => {self.size}')
            
                        
                        elif self.task["SIZE"].lower() == "random":
                            selected = random.choice(allSizes)
                            self.size = selected.split(':')[0]
                            self.sizeID = selected.split(':')[2]
                            logger.success(SITE,self.taskID,f'Found Size => {self.size}')
                    
                    else:
                        logger.error(SITE,self.taskID,'Size Not Found')
                        time.sleep(int(self.task["DELAY"]))
                        self.collect()
    
                except Exception as e:
                    log.info(e)
                    logger.error(SITE,self.taskID,'Failed to scrape page (Most likely out of stock). Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.collect()
    
                self.addToCart()
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
            'form_key': self.formKey,
            'product': self.productId,
            'related_product': '',
            f'super_attribute[{self.attributeId}]': self.sizeID,
            'full_product_url_key': self.productUrlKey
        }
        self.session.headers['x-requested-with'] = 'XMLHttpRequest'
        self.session.headers['accept'] = 'text/javascript, text/html, application/xml, text/xml, */*'
        self.session.headers['referer'] = self.task["PRODUCT"]
        try:
            cart = self.session.post('https://www.consortium.co.uk/consortium_checkout/ajaxs_cart/add/',data=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()


        try:
            json = cart.json()
        except:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            if self.task["SIZE"] == "random":
                self.collect()
            else:
                self.addToCart()
        
        if cart.status_code == 200 and json["success"] == True:
            logger.success(SITE,self.taskID,'Successfully carted')
            self.emailMethod()
        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            if self.task["SIZE"] == "random":
                self.collect()
            else:
                self.addToCart()



    def emailMethod(self):
        self.session.headers = {}
        self.session.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'content-type':'application/x-www-form-urlencoded',
            'origin': 'https://www.consortium.co.uk',
            'referer': 'https://www.consortium.co.uk/checkout/secure/login/',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
        }
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        payload = {
            'register[email]': profile["email"],
            'register[password]': None,
            'register[confirm]': None
        }

        try:
            method = self.session.post('https://www.consortium.co.uk/checkout/secure/registerPost/',data=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.emailMethod()

        print(method)
        print(method.url)

    def billing(self):
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()

        try:
            securePage = self.session.get('https://www.consortium.co.uk/checkout/secure/billing/')
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.billing()


        if securePage.status_code == 200:
            soup = BeautifulSoup(securePage.text,"html.parser")
            self.addressId = soup.find('input',{'id':'billing:address_id'})
            self.session.headers = {}
            self.session.headers = {
                'origin': 'https://www.consortium.co.uk',
                'referer': 'https://www.consortium.co.uk/checkout/secure/billing/',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
            }

            payload = {
                'billing[address_id]': self.addressId,
                'billing[email]': profile["email"],
                'billing[email_confirm]': profile["email"],
                'billing[firstname]': profile["firstName"],
                'billing[lastname]': profile["lastName"],
                'billing[postcode]': profile["zip"],
                'billing[country_id]': profile["countryCode"],
                'billing[company]': '',
                'billing[street][]': '{} {}'.format(profile["house"],profile["addressOne"]),
                'billing[street][]': profile["addressTwo"],
                'billing[city]': profile["city"],
                'billing[region_id]': '',
                'billing[region]': profile["region"],
                'billing[telephone]': profile["phone"],
                'billing[save_in_address_book]': 1,
                'billing[use_for_shipping]': 1,
            }
            print(payload)
            self.session.headers['referer'] = 'https://www.consortium.co.uk/checkout/secure/billing/'
    
            try:
                billPost = self.session.post('https://www.consortium.co.uk/checkout/secure/billingPost/',data=payload)
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                self.billing()

        else:
            logger.error(SITE,self.taskID,'Failed to retrieve billing page. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.billing()



        


