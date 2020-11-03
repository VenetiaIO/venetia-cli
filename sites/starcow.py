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
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, starcow_datadome, sendNotification, injection)
SITE = 'STARCOW'


class STARCOW:
    def __init__(self, task,taskName):
        self.task = task
        self.sess = requests.session()
        self.taskID = taskName

        twoCap = loadSettings()["2Captcha"]
        try:
            self.session = cloudscraper.create_scraper(
                requestPostHook=injection,
                sess=self.sess,
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
        except Exception as e:
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.__init__()
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'referer':'https://www.starcowparis.com/'
        }


        self.collect()

    def collect(self):
        logger.prepare(SITE,self.taskID,'Getting product page...')

        self.cookie = loadCookie('STARCOW')["cookie"]
        if self.cookie == 'empty':
            # del self.session.cookies["datadome"]
            self.cookie = starcow_datadome(self.session.proxies,self.taskID)
            self.session.cookies["datadome"]  = self.cookie
        else:
            # del self.session.cookies["datadome"]
            self.session.cookies["datadome"]  = self.cookie
            self.session.proxies = self.cookie["proxy"]


        try:
            retrieve = self.session.get(self.task["PRODUCT"])
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.collect()

        if retrieve:
            print(retrieve.url)
            if 'DDUser' in retrieve.url:
                self.cookie = loadCookie('STARCOW')
                if self.cookie == 'empty':
                    del self.session.cookies["datadome"]
                    self.cookie = starcow_datadome(self.session.proxies,self.taskID)
                else:
                    del self.session.cookies["datadome"]
                    self.session.cookies["datadome"]  = self.cookie["cookie"]
                    self.session.proxies = self.cookie["proxy"]
            else:
                if retrieve.status_code == 200:
                    logger.success(SITE,self.taskID,'Got product page')
                    try:
                        soup = BeautifulSoup(retrieve.text, "html.parser")
                        SizeSelect = soup.find('select',{'class':['form-control','form-control-select']})
                        self.sizeGroup = SizeSelect["name"]
        
                        all_sizes = []
                        sizes = []
            
                        if SizeSelect == None:
                            logger.error(SITE,self.taskID,'No sizes available. Retrying...')
                            time.sleep(int(self.task["DELAY"]))
                            self.collect()
            
                        try:
                            for s in SizeSelect:
                                size = s.text.split(' US /')[0]
                                sizeValue = s["value"]
                                all_sizes.append(f'{size}:{sizeValue}')
                                sizes.append(size)
                        except Exception as e:
                            log.info(e)
                            logger.error(SITE,self.taskID,'Size Not Found')
                            time.sleep(int(self.task["DELAY"]))
                            self.collect()
            
                        if self.task["SIZE"].lower() == "random":
                            chosen = random.choice(all_sizes)
                            self.sizeValue = chosen.split(':')[1]
                            self.size = chosen.split(':')[0]
                            logger.success(SITE,self.taskID,f'Found Size => {self.size}')
                            #self.addToCart()
                        
            
                        else:
                            if self.task["SIZE"] not in sizes:
                                logger.error(SITE,self.taskID,'Size Not Found')
                                time.sleep(int(self.task["DELAY"]))
                                self.collect()
                            for size in all_sizes:
                                if self.task["SIZE"] == size.split(':')[0]:
                                    self.size = size.split(':')[0]
                                    logger.success(SITE,self.taskID,f'Found Size => {self.size}')
                                    self.sizeValue = size.split(':')[1]
                                    #self.addToCart()
        
                                
                    except Exception as e:
                        log.info(e)
                        logger.error(SITE,self.taskID,'Failed to scrape page (Most likely out of stock). Retrying...')
                        time.sleep(int(self.task["DELAY"]))
                        self.collect()
                else:
                    logger.error(SITE,self.taskID,'Failed to get product page. Retrying...')
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
        cartPayload = {
            'token': '9d2812a5efc11b666a70ce4403b30df3',
            'id_product': 3480,
            'id_customization': 0,
            'group[36]': 487,
            'qty': 1,
            'add': 1,
            'action': 'update'
        }
        try:
            cart = self.session.post('https://www.starcowparis.com/panier')
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.collect()



  