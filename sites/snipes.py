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
from utils.px import PX
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies, updateConsoleTitle, urlEncode)
SITE = 'SNIPES'


class SNIPES:
    def __init__(self, task,taskName):
        self.task = task
        self.session = requests.session()
        self.taskID = taskName

        twoCap = loadSettings()["2Captcha"]
        # self.session = cloudscraper.create_scraper(
            # requestPostHook=injection,
            # sess=self.sess,
            # interpreter='nodejs',
            # browser={
                # 'browser': 'chrome',
                # 'mobile': False,
                # 'platform': 'windows'
                # 'platform': 'darwin'
            # },
            # captcha={
                # 'provider': '2captcha',
                # 'api_key': twoCap
            # }
        # )
        
        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)

        self.collect()
    
    def collect(self):
        logger.prepare(SITE,self.taskID,'Getting product page...')
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'referer': 'https://www.snipes.com/'

        }
        self.queryUrl = '{}chosen=size&dwvar_00013801855356_212=60&format=ajax'.format(self.task["PRODUCT"],)
        try:
            retrieve = self.session.get(self.task["PRODUCT"])
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.collect()
        print(retrieve.headers)
        
        if retrieve.status_code == 200:
            self.start = time.time()
            logger.success(SITE,self.taskID,'Got product page')
            try:
                soup = BeautifulSoup(retrieve.text,"html.parser")
                found_sizes = soup.find_all('a',{'data-attr-id':'size'})
                self.productPid = soup.find('input',{'name':'pid'})['value']
                self.selectedValId = found_sizes[0]["data-href"].split(f'{self.productPid}_')[1].split('=')[0]
                sizes = []
                for s in found_sizes:
                    sizes.append(s["data-value"])
               
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
                        for size in sizes:
                            if size == self.task["SIZE"]:
                                self.size = size
                                logger.success(SITE,self.taskID,f'Found Size => {self.size}')
    
                
                elif self.task["SIZE"].lower() == "random":
                    self.size = random.choice(sizes)
                    logger.success(SITE,self.taskID,f'Found Size => {self.size}')
                        
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to scrape page. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.collect()

            self.query()
    
    def query(self):
        logger.prepare(SITE,self.taskID,'Getting size info...')
        self.queryUrl = '{}?chosen=size&dwvar_{}_{}={}&format=ajax'.format(self.task["PRODUCT"],self.productPid,self.selectedValId,self.size)
        try:
            retrieve = self.session.get(self.queryUrl)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.query()
        
        try:
            data = retrieve.json()
        except:
            logger.error(SITE,self.taskID,'Failed to retrieve size info. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.query()
        
        if retrieve.status_code == 200 and data:
            self.csrf = data["csrf"]["token"]
            self.sizePID = data["product"]["id"]
            self.productPrice = data["product"]["price"]["list"]["formatted"]
            self.productTitle = data["product"]["productName"]
            logger.success(SITE,self.taskID,'Got size info => {}'.format(self.sizePID))
            self.addToCart()
        else:
            logger.error(SITE,self.taskID,'Failed to retrieve size info. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.query()
    

    def addToCart(self):
        logger.prepare(SITE,self.taskID,'Adding to cart...')
        cookies = PX.snipes()
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'referer': self.task["PRODUCT"],
            'cookie':'_px3={}; _pxvid={};'.format(cookies['px3'],cookies['vid']),
            'x-requested-with': 'XMLHttpRequest'
        }
        payload = {
            "pid": self.sizePID,
            "options": [{"optionId":self.selectedValId,"selectedValueId":self.size}],
            "quantity": 1 
        }
        try:
            retrieve = self.session.post('https://www.snipes.com/add-product?format=ajax',data=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.query()

        print(retrieve)
        with open('snipes.txt','w') as snipes:
            snipes.write(str(retrieve.text))
            snipes.close()
        