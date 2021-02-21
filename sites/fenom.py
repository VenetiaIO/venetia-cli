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
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies, updateConsoleTitle, scraper)
SITE = 'FENOM'


class FENOM:
    def __init__(self,task,taskName,rowNumber):
        self.task = task
        # self.session = Session()
        self.taskID = taskName

        twoCap = loadSettings()["2Captcha"]
        self.session = scraper()
        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)

        self.collect()

    def collect(self):
        logger.prepare(SITE,self.taskID,'Getting product page...')
        try:
            retrieve = self.session.get(self.task["PRODUCT"],headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-language": "en-US,en;q=0.9",
                "sec-ch-ua": "\"Chromium\";v=\"88\", \"Google Chrome\";v=\"88\", \";Not A Brand\";v=\"99\"",
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "cross-site",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1"
                # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.collect()

        print(retrieve)
        if retrieve.status_code == 200:

            self.start = time.time()
            logger.success(SITE,self.taskID,'Got product page')
            try:
                soup = BeautifulSoup(retrieve.text, "html.parser")
                self.token = soup.find('input',{'name':'token'})['value']
                self.product_id = soup.find('input',{'name':'id_product'})['value']
                self.groupId = soup.find('div',{'class':'prod-variant'}).find('label')["for"].split('group_')[1]
                self.foundSizes = soup.find_all('input',{'name':f'group[{self.groupId}]'})

                allSizes = []
                sizes = []
                for s in self.foundSizes:
                    sVal = s['value']
                    a = BeautifulSoup(retrieve.text,'html.parser')
                    size_eu = a.find('label',{'for':s['id']}).find('span',{'class':'size_EU'}).text.replace(' ','').replace('\n','')
                    allSizes.append('{}:{}'.format(size_eu,sVal))
                    sizes.append(size_eu)

                
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
                                self.sizeID = size.split(":")[1]
                                logger.success(SITE,self.taskID,f'Found Size => {self.size}')
    
                
                elif self.task["SIZE"].lower() == "random":
                    selected = random.choice(allSizes)
                    self.size = selected.split(":")[0]
                    self.sizeID = selected.split(":")[1]
                    logger.success(SITE,self.taskID,f'Found Size => {self.size}')

                        
            except (Exception, ConnectionError) as e:
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
        logger.prepare(SITE,self.taskID,'Carting products...')
        data = {
            'token': self.token,
            'id_product': self.product_id,
            'id_customization': 0,
            f'group[{self.groupId}]': self.sizeID,
            'add': 1,
            'action': 'update'
        }
        try:
            cart = self.session.post('https://www.fenom.com/en/cart',data=data,headers={
                'referer': self.task["PRODUCT"],
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'x-requested-with': 'XMLHttpRequest'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()
        except requests.exceptions.RequestException as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

        print(cart)
        print(cart.text)

