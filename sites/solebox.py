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
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies, updateConsoleTitle, randomUA)
SITE = 'SOLEBOX'


class SOLEBOX:
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
        self.UA = randomUA()
        self.refer = self.task["PRODUCT"]

        # self.cookies = {
            # "px3":"",
            # "vid":"e244a651-188c-11eb-8079-d3c780d947ac"
        # }
        self.sbxRegion = 'com'

        if 'https' in self.task['PRODUCT']:
            try:
                self.pid = '0' + self.task['PRODUCT'].split('-0')[1].split('.html')[0]
            except:
                logger.error(SITE,self.taskID,'Failed to parse PID. Please check it is a valid SOLEBOX url.')
                time.sleep(5)
                sys.exit()
        else:

            self.pid = self.task['PRODUCT']

        cookies = PX.solebox(self.session, f'https://www.solebox.{self.sbxRegion}', self.taskID)
        while cookies["px3"] == "error":
            cookies = PX.solebox(self.session, f'https://www.solebox.{self.sbxRegion}', self.taskID)

        cookie_obj = requests.cookies.create_cookie(domain=f'www.solebox.{self.sbxRegion}',name='_px3',value=cookies['px3'])
        cookie_obj2 = requests.cookies.create_cookie(domain=f'www.solebox.{self.sbxRegion}',name='_pxvid',value=cookies['vid'])
        self.session.cookies.set_cookie(cookie_obj)
        self.session.cookies.set_cookie(cookie_obj2)
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'referer': f'https://www.solebox.{self.sbxRegion}/',
        }
        self.start = time.time()

        self.queryUrl = 'https://www.solebox.{}/p/{}.html?dwvar_{}_color=a&format=ajax'.format(self.sbxRegion,self.pid,self.pid)

        self.query()


    def query(self):
        logger.prepare(SITE,self.taskID,'Getting product info...')
        try:
            retrieve = self.session.get(self.queryUrl)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.query()

        
        
        if retrieve.status_code == 200:
            try:
                data = retrieve.json()
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to retrieve product info. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.query()

            self.productTitle = data["product"]["productName"]
            self.productPrice = data["product"]["price"]["sales"]["formatted"]
            self.productImage = data["product"]["images"][0]["pdp"]["srcT"]
            self.csrf = data["csrf"]["token"]
            allSizes = []
            sizes = []
            for s in data["product"]["variationAttributes"][0]["values"]:
                sizes.append(s["value"])
                allSizes.append('{}:{}'.format(s["value"],s["variantId"]))

            if len(sizes) == 0:
                logger.error(SITE,self.taskID,'Sizes Not Found')
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
                            self.sizePID = size.split(":")[1]
                            logger.success(SITE,self.taskID,f'Found Size => {self.size}')

            
            elif self.task["SIZE"].lower() == "random":
                selected = random.choice(allSizes)
                self.size = selected.split(":")[0]
                self.sizePID = selected.split(":")[1]
                logger.success(SITE,self.taskID,f'Found Size => {self.size}')
            
            self.addToCart()

        if retrieve.status_code == 403:
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            cookies = PX.solebox(self.session, f'https://www.solebox.{self.sbxRegion}', self.taskID)
            while cookies["px3"] == "error":
                cookies = PX.snipes(self.session, f'https://www.solebox.{self.sbxRegion}', self.taskID)

            cookie_obj = requests.cookies.create_cookie(domain=f'www.solebox.{self.sbxRegion}',name='_px3',value=cookies['px3'])
            cookie_obj2 = requests.cookies.create_cookie(domain=f'www.solebox.{self.sbxRegion}',name='_pxvid',value=cookies['vid'])
            self.session.cookies.set_cookie(cookie_obj)
            self.session.cookies.set_cookie(cookie_obj2)
            logger.error(SITE,self.taskID,'Forbidden. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.query()

        if retrieve.status_code == 429:
            logger.error(SITE,self.taskID,'Rate Limit (Sleeping). Retrying...')
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.UA = randomUA()
            time.sleep(10)
            self.query()
    
        elif retrieve.status_code not in [200,403]:
            logger.error(SITE,self.taskID,'Failed to retrieve product info. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.query()


    def addToCart(self):

        logger.prepare(SITE,self.taskID,'Adding to cart...')
        self.session.headers = {}
        self.session.headers = {
            'authority': f'www.solebox.{self.sbxRegion}',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': f'https://www.solebox.{self.sbxRegion}',
            'referer': self.refer,
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.UA,
            'x-requested-with': 'XMLHttpRequest'
        }
        payload = {
            "pid": self.sizePID,
            "options": [],
            "quantity": 1 
        }

        try:
            cart = self.session.post(f'https://www.solebox.{self.sbxRegion}/add-product?format=ajax',data=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

        
        if cart.status_code == 200:
            try:
                data = cart.json()
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.addToCart()
            try:
                if data['cart']['items']:
                    self.uuid = data['cart']['items'][0]['UUID']
                    self.shipmentUUID = data['cart']['items'][0]['shipmentUUID']
                    self.demandWareBase = data['cart']['actionUrls']['submitCouponCodeUrl'].split('/Cart-AddCoupon')[0]
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                if self.task["SIZE"].lower() == "random":
                    self.query()
                else:
                    self.addToCart()


            updateConsoleTitle(True,False,SITE)
            logger.success(SITE,self.taskID,'Successfully Carted')
            #self.shipping()
            sys.exit()
        
        if cart.status_code == 403:
            cookies = PX.snipes(self.session, f'https://www.solebox.{self.sbxRegion}', self.taskID)
            while cookies["px3"] == "error":
                cookies = PX.snipes(self.session, f'https://www.solebox.{self.sbxRegion}', self.taskID)

            cookie_obj = requests.cookies.create_cookie(domain=f'www.solebox.{self.sbxRegion}',name='_px3',value=cookies['px3'])
            cookie_obj2 = requests.cookies.create_cookie(domain=f'www.solebox.{self.sbxRegion}',name='_pxvid',value=cookies['vid'])
            self.session.cookies.set_cookie(cookie_obj)
            self.session.cookies.set_cookie(cookie_obj2)
            logger.error(SITE,self.taskID,'Forbidden. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

        if cart.status_code == 429:
            logger.error(SITE,self.taskID,'Rate Limit. Retrying...')
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.UA = randomUA()
            current_px3 = self.session.cookies.get_dict()["_px3"]
            current_pxvid = self.session.cookies.get_dict()["_pxvid"]

            self.session.cookies.clear()

            cookie_obj = requests.cookies.create_cookie(domain=f'www.solebox.{self.sbxRegion}',name='_px3',value=current_px3)
            cookie_obj2 = requests.cookies.create_cookie(domain=f'www.solebox.{self.sbxRegion}',name='_pxvid',value=current_pxvid)
            self.session.cookies.set_cookie(cookie_obj)
            self.session.cookies.set_cookie(cookie_obj2)
            self.addToCart()
        
        elif cart.status_code not in [200,403]:
            logger.error(SITE,self.taskID,'Failed to cart [{}]. Retrying...'.format(cart.status_code))
            time.sleep(int(self.task["DELAY"]))
            if self.task["SIZE"].lower() == "random":
                self.query()
            else:
                self.addToCart()
