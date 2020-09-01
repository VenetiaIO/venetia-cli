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

from utils.logger import logger
from utils.webhook import discord
from utils.log import log
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection)
SITE = '43 EINHALB'


class EINHALB:
    def __init__(self, task,taskName):
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
        
        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)

        self.collect()

    def collect(self):
        logger.warning(SITE,self.taskID,'Solving Cloudflare...')
        try:
            retrieve = self.session.get(self.task["PRODUCT"], headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'

            })
            logger.success(SITE,self.taskID,'Solved Cloudflare')
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.collect()

        if retrieve.status_code == 200:
            logger.success(SITE,self.taskID,'Got product page')
            try:
                soup = BeautifulSoup(retrieve.text, "html.parser")
    
                productData = soup.find_all('select',{'class':'customSelectBox'})[1]

                allSizes = []
                sizes = []
                for s in productData:
                    try:
                        size = s.text.strip().split('· ')
                        US_SIZE = size[1].split(' US')[0].strip()
                        allSizes.append('{}:{}'.format(US_SIZE,s["value"].strip()))
                        sizes.append(US_SIZE)
                    except:
                        pass

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
                                self.sizeVal = size.split(':')[1]
                                logger.success(SITE,self.taskID,f'Found Size => {self.size}')
    
                
                elif self.task["SIZE"].lower() == "random":
                    selected = random.choice(allSizes)
                    self.size = selected.split(":")[0]
                    self.sizeVal = selected.split(":")[1]
                    logger.success(SITE,self.taskID,f'Found Size => {self.size}')

            
                        
            except Exception as e:
               log.info(e)
               logger.error(SITE,self.taskID,'Failed to scrape page (Most likely out of stock). Retrying...')
               time.sleep(int(self.task["DELAY"]))
               self.collect()

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
            'chosen_attribute_value': self.sizeVal,
            'returnHtmlSnippets[partials][0][module]': 'product',
            'returnHtmlSnippets[partials][0][path]': '_productDetail',
            'returnHtmlSnippets[partials][0][partialName]': 'buybox',
            'returnHtmlSnippets[partials][0][params][template]': 'default'
        }

        try:
            getSizeDetails = self.session.post(self.task["PRODUCT"], data=payload, headers={
                'authority': 'www.43einhalb.com',
                'accept-language': 'en-US,en;q=0.9',
                'origin': 'https://www.43einhalb.com',
                'referer': self.task["PRODUCT"],
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()

        try:
            data = getSizeDetails.json()
        except:
            logger.error(SITE,self.taskID,'Failed to get size details. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

        if getSizeDetails.status_code == 200 and data:
            logger.success(SITE,self.taskID,'Scraped Size IDs')

            self.productId = data["initializedProduct"]["id"]
            self.bsId = data["initializedProduct"]["bsId"]
            self.parentId = data["initializedProduct"]["parentProduct"]["id"]
            self.parentBsId = data["initializedProduct"]["parentProduct"]["bsId"]
            self.productTitle = data["initializedProduct"]["fullProductName"]
            self.productImage = 'https://43einhalb.com/media/{}/w/616/h/370/n/{}'.format(data["initializedProduct"]["firstImage"]["image"]["id"],data["initializedProduct"]["firstImage"]["image"]["displayName"])
            self.addToCart()
        else:
            logger.error(SITE,self.taskID,'Failed to get size details. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

    def addToCart(self):
        payload = {
            'product_bs_id': self.bsId,
            'product_id': self.productId,
            'amount': 1,
            'ajax': True,
            'forward[module]': 'cart',
            'forward[action]': 'wasadded',
            'addToCart': '',
            'returnHtmlSnippets[partials][0][module]': 'cart',
            'returnHtmlSnippets[partials][0][partialName]': 'headerCart',
            'returnHtmlSnippets[partials][0][returnName]': 'headerCartDesktop',
            'returnHtmlSnippets[partials][0][params][template]': 'default',
            'returnHtmlSnippets[partials][1][module]': 'cart',
            'returnHtmlSnippets[partials][1][partialName]': 'headerCart',
            'returnHtmlSnippets[partials][1][returnName]': 'headerCartMobile',
            'returnHtmlSnippets[partials][1][params][template]': 'mobile',
            'returnHtmlSnippets[partials][2][module]': 'cart',
            'returnHtmlSnippets[partials][2][partialName]': 'cartPreview',
            'returnHtmlSnippets[partials][2][returnName]': 'cartPreview',
            'returnHtmlSnippets[partials][3][module]': 'product',
            'returnHtmlSnippets[partials][3][path]': '_productDetail',
            'returnHtmlSnippets[partials][3][partialName]': 'buybox',
            'returnHtmlSnippets[partials][3][params][template]': 'default',
            'returnHtmlSnippets[partials][3][params][bsId]': self.bsId,
            'returnHtmlSnippets[partials][4][module]': 'cart',
            'returnHtmlSnippets[partials][4][partialName]': 'modalWasadded'
        }

        try:
            postCart = self.session.post(self.task["PRODUCT"], data=payload, headers={
                'authority': 'www.43einhalb.com',
                'accept-language': 'en-US,en;q=0.9',
                'origin': 'https://www.43einhalb.com',
                'referer': self.task["PRODUCT"],
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()

        try:
            data = postCart.json()
        except:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

        if postCart.status_code == 200 and data:
            print(data)
            logger.success(SITE,self.taskID,'Successfully carted')

            self.method()
        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

  