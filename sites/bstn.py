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
import cloudscraper
import string

SITE = 'BSTN'

from utils.logger import logger
from utils.captcha import captcha
from utils.log import log
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, injection, updateConsoleTitle)


class BSTN:
    def __init__(self,task,taskName):
        self.task = task
        self.sess = requests.session()
        self.taskID = taskName

        twoCap = loadSettings()["2Captcha"]
        self.session = cloudscraper.create_scraper(
            requestPostHook=injection,
            sess=self.sess,
            interpreter='nodejs',
            browser={
                'browser': 'chrome',
                'mobile': False,
                'platform': 'windows'
                #'platform': 'darwin'
            },
            captcha={
                'provider': '2captcha',
                'api_key': twoCap
            }
        )
        self.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
        self.session.proxies = self.proxies
        self.userAgent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1'

        self.session.headers.update({
            'User-Agent':self.userAgent
        })

        self.collect()

    def collect(self):
        try:
            retrieve = self.session.get(self.task["PRODUCT"])
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.collect()

        if retrieve.status_code == 200:
            logger.success(SITE,self.taskID,'Got product page')
            soup = BeautifulSoup(retrieve.text,"html.parser")
            self.hash = soup.find("input",{"name":"hash"})["value"]
            self.secret = soup.find("input",{"name":"secret"})["value"]
            secretDecoded = base64.b64decode(self.secret)
            self.cartId = json.loads(secretDecoded.decode('Utf-8'))["action"]
            selectBox = soup.find("select",{"class":"customSelectBox"})
            all_sizes = []
            sizes = []
            for s in selectBox:
                try:
                    size = s.text.strip().split('-')
                    US_SIZE = size[1].split('US')[1].strip()
                    all_sizes.append('{}:{}'.format(US_SIZE,s["value"].strip()))
                    sizes.append(US_SIZE)
                    #EU_SIZE = size[0].split('EU')[1].strip()
                        
                except:
                    pass

            if self.task["SIZE"].lower() != "random":
                if self.task["SIZE"] not in sizes:
                    logger.error(SITE,self.taskID,'Size Not Found')
                    time.sleep(int(self.task["DELAY"]))
                    self.collect()
                else:
                    for size in all_sizes:
                        if size.split(':')[0] == self.task["SIZE"]:
                            self.size = size.split(':')[0];
                            self.sizeValue = size.split(':')[1];
                            logger.success(SITE,self.taskID,f'Found Size => {self.size}')
                            self.getIds()

            
            
            elif self.task["SIZE"].lower() == "random":
                selected = random.choice(all_sizes)
                self.size = selected.split(":")[0]
                self.sizeValue = selected.split(":")[1]
                logger.success(SITE,self.taskID,f'Found Size => {self.size}')
                self.getIds()

        else:
            try:
                status = retrieve.status_code
            except:
                status = 'Unknown'
            logger.error(SITE,self.taskID,f'Failed to get product page => {status}. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.collect()


    def getIds(self):
        payload = {
            'token': self.hash,
            'chosen_attribute_value': self.sizeValue,
            'returnHtmlSnippets[partials][0][module]': 'product',
            'returnHtmlSnippets[partials][0][path]': '_productDetail',
            'returnHtmlSnippets[partials][0][partialName]': 'buybox'
        }

        try:
            getSizeDetails = self.session.post(self.task["PRODUCT"],data=payload,headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'accept': '*/*',
                'authority': 'www.bstn.com',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://www.bstn.com',
                'referer': self.task["PRODUCT"],
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
    
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.getIds()

            
        if getSizeDetails.status_code == 200:
            if getSizeDetails.text:
                jsonDetails = json.loads(getSizeDetails.text)
                self.productId = jsonDetails["initializedProduct"]["id"]
                self.bsId = jsonDetails["initializedProduct"]["bsId"]
                self.parentId = jsonDetails["initializedProduct"]["parentProduct"]["id"]
                self.parentBsId = jsonDetails["initializedProduct"]["parentProduct"]["bsId"]
                self.productTitle = jsonDetails["initializedProduct"]["fullProductName"]
                imgID = jsonDetails["initializedProduct"]["firstImage"]["image"]["id"]
                imgDisplay = jsonDetails["initializedProduct"]["firstImage"]["image"]["displayName"]
                self.image = f'https://www.bstn.com/media/{imgID}/w/1000/h/1000/n/{imgDisplay}'
                logger.success(SITE,self.taskID,'Scraped Size IDs')
                self.addToCart()
            else:
                logger.error(SITE,self.taskID,'Failed to scrape size IDs')
                time.sleep(int(self.task["DELAY"]))
                self.getIds()

        elif getSizeDetails.status_code != 200:
            logger.error(SITE,self.taskID,'Failed to scrape size IDs')
            time.sleep(int(self.task["DELAY"]))
            self.getIds()


    def addToCart(self):
        captchaResponse = captcha.v3('6Le9G8cUAAAAANrlPVYknZGUZw8lopZAqe8_SfRQ','https://www.bstn.com/',self.proxies,SITE,self.taskID)
        payload = {
            'hash': self.hash,
            'secret': self.secret,
            'product_id': self.productId,
            'product_bs_id': self.bsId,
            'amount': 1,
            'g-recaptcha-response':captchaResponse,
            'ajax': True,
            'redirectRooting': '',
            'addToCart': '',
            'returnHtmlSnippets[partials][0][module]': 'cart',
            'returnHtmlSnippets[partials][0][partialName]': 'cartHeader',
            'returnHtmlSnippets[partials][0][returnName]': 'headerCartDesktop',
            'returnHtmlSnippets[partials][0][params][template]': 'Standard',
            'returnHtmlSnippets[partials][1][module]': 'cart',
            'returnHtmlSnippets[partials][1][partialName]': 'cartHeader',
            'returnHtmlSnippets[partials][1][returnName]': 'cartErrors',
            'returnHtmlSnippets[partials][1][params][template]': 'errorMessage',
            'returnHtmlSnippets[partials][2][module]': 'cart',
            'returnHtmlSnippets[partials][2][partialName]': 'cartHeader',
            'returnHtmlSnippets[partials][2][returnName]': 'headerCartMobile',
            'returnHtmlSnippets[partials][2][params][template]': 'mobileNavbar',
            'returnHtmlSnippets[partials][3][module]': 'product',
            'returnHtmlSnippets[partials][3][path]': '_productDetail',
            'returnHtmlSnippets[partials][3][partialName]': 'buybox',
            'returnHtmlSnippets[partials][3][returnName]': 'buybox',
            'returnHtmlSnippets[partials][3][params][bsId]': self.bsId,
            'returnHtmlSnippets[partials][4][module]':'cart',
            'returnHtmlSnippets[partials][4][partialName]': 'modalWasadded'
        }
        print(self.cartId)
        cartUrl = 'https://www.bstn.com{}?g={}'.format(self.cartId,captchaResponse)
        print(cartUrl)
        print(payload)

        try:
            postCart = self.session.post(cartUrl,data=payload,headers={
                'authority': 'www.bstn.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://www.bstn.com',
                'referer': self.task["PRODUCT"],
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
            })
        except:
            logger.error(SITE,self.taskID,'Connection Error. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()

            
        print(postCart)
        print(postCart.text)


