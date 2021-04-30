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
from utils.px import PX
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies, updateConsoleTitle, scraper)
import utils.config as config

_SITE_ = 'SNIPES'
SITE = 'Snipes'
class SNIPES:
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
            "product_url":self.task['PRODUCT']
        }



        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)

        self.profile = loadProfile(self.task["PROFILE"])
        if self.profile == None:
            self.error("Profile Not found. Exiting...")
            time.sleep(10)
            sys.exit()

        if 'https' in self.task['PRODUCT']:
            try:
                self.snipesRegion = self.task["PRODUCT"].split('snipes.')[1].split('/')[0]
                self.pid = '00' + self.task['PRODUCT'].split('-00')[1].split('.html')[0]
            except:
                self.error("Failed to parse PID. Please check it is a valid SNIPES url.")
                time.sleep(5)
                sys.exit()
        else:
            if self.profile['countryCode'].upper() == "DE":
                self.snipesRegion = 'com'
            elif self.profile['countryCode'].upper() == "AT":
                self.snipesRegion = 'at'
            elif self.profile['countryCode'].upper() == "NL":
                self.snipesRegion = 'nl'
            elif self.profile['countryCode'].upper() == "FR":
                self.snipesRegion = 'fr'
            elif self.profile['countryCode'].upper() == "CH":
                self.snipesRegion = 'ch'
            elif self.profile['countryCode'].upper() == "IT":
                self.snipesRegion = 'it'
            elif self.profile['countryCode'].upper() == "ES":
                self.snipesRegion = 'es'
            elif self.profile['countryCode'].upper() == "BE":
                self.snipesRegion = 'be'
            
            else:
                self.error('Region not supported. Exiting...')
                time.sleep(10)
                sys.exit()
                
            self.pid = self.task['PRODUCT']

        cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID)
        while cookies["px3"] == "error":
            cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID)

        self.cs = cookies['cs']
        self.sid = cookies['sid']
        
        cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
        cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid']) 
        self.session.cookies.set_cookie(cookie_obj)
        self.session.cookies.set_cookie(cookie_obj2)

        self.queryUrl = 'https://www.snipes.{}/p/{}.html?dwvar_{}_color=a&format=ajax'.format(self.snipesRegion,self.pid,self.pid)


        self.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'

        self.tasks()
    
    def tasks(self):

        self.monitor()
        self.csrf()

        if self.task["ACCOUNT EMAIL"].strip() != "" and self.task["ACCOUNT PASSWORD"].strip() != "": 
            self.login()

        self.addToCart()
        self.shipping()
        self.paymentMethod()
        self.placeOrder()

        self.sendToDiscord()

    def monitor(self):
        while True:
            self.prepare("Getting Product...")

            try:
                response = self.session.get(self.queryUrl, headers={
                    'user-agent': self.userAgent,
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'referer': f'https://www.snipes.{self.snipesRegion}/',
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue

            if response.status_code == 200:
                self.start = time.time()

                self.warning("Retrieved Product")

                try:
                    data = response.json()

                    self.webhookData['product'] = str(data["product"]["productName"])
                    self.webhookData['image'] = str(data["product"]["images"][0]["pdp"]["srcT"])
                    self.webhookData['price'] = str(data["product"]["price"]["sales"]["formatted"])

                    self.demandWareBase = data["product"]["quantities"][0]["url"].split('Product-Variation')[0]

                    if self.snipesRegion != 'com':
                        self.atcUrl = f'https://www.snipes.{self.snipesRegion}{self.demandWareBase}Cart-AddProduct?format=ajax'
                    else:
                        self.atcUrl = f'https://www.snipes.{self.snipesRegion}/add-product?format=ajax'


                    sizeList = data["product"]["variationAttributes"][0]["values"]

                    allSizes = []
                    sizes = []
                    for s in sizeList:
                        try:
                            sizes.append(s["value"])
                            sizePid = s["variantId"]
                            if sizePid in ['None', None]:
                                sizePid = s['pid']
                            allSizes.append('{}:{}'.format(s["value"],sizePid))
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
                                    self.size = size.split(':')[0]
                                    self.sizePID = size.split(":")[1]
                                    
                                    self.warning(f"Found Size => {self.size}")
        
                    else:
                        selected = random.choice(allSizes)
                        self.size = selected.split(":")[0]
                        self.sizePID = selected.split(":")[1]
                        
                        self.warning(f"Found Size => {self.size}")

                    
                except Exception as e:
                    log.info(e)
                    self.error("Failed to parse product data (maybe OOS)")
                    time.sleep(int(self.task['DELAY']))
                    continue
                
                self.webhookData['size'] = self.size
                return

            if response.status_code == 403:
                if 'px-captcha' in response.text:
                    self.error("Blocked by PX Captcha. Solving...")
                    try:
                        uuid = response.text.split("window._pxVid = '")[1].split("';")
                        vid = response.text.split("window._pxUuid = '")[1].split("';")
                        blockedUrl = f'https://www.snipes.{self.snipesRegion}/blocked&uuid={uuid}&vid={vid}'
                    except:
                        self.error(f"Failed to parse PX response. Retrying...")
                        time.sleep(int(self.task['DELAY']))
                        continue

                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
                    while cookies["px3"] == "error":
                        cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
        
                    cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                    cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                    self.session.cookies.set_cookie(cookie_obj)
                    self.session.cookies.set_cookie(cookie_obj2)
                    continue
                else:
                    self.error("Blocked by PX. Retrieving new cookie...")
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID)
                    while cookies["px3"] == "error":
                        cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID)
        
                    self.cs = cookies['cs']
                    self.sid = cookies['sid']
                    cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                    cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                    self.session.cookies.set_cookie(cookie_obj)
                    self.session.cookies.set_cookie(cookie_obj2)
                    continue

            if response.status_code == 429:
                self.error("Rate Limited. Rotating Proxy...")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(10)
                continue

                    
            else:
                self.error(f"Failed to get product [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def csrf(self):
        while True:
            self.prepare("Getting CSRF...")
            try:
                response = self.session.post('https://www.snipes.{}{}/CSRF-Generate'.format(self.snipesRegion,self.demandWareBase), headers={
                    'user-agent': self.userAgent,
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'referer': f'https://www.snipes.{self.snipesRegion}/',
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if response.status_code == 200:

                try:
                    self.csrf = response.json()['csrf']['token']
                except Exception as e:
                    log.info(e)
                    self.error("Failed to get csrf [failed to parse response]. Retrying...")
                    time.sleep(int(self.task["DELAY"]))
                    continue

                self.warning("Got CSRF")
                return

            if response.status_code == 403:
                if 'px-captcha' in response.text:
                    self.error("Blocked by PX Captcha. Solving...")
                    try:
                        uuid = response.text.split("window._pxVid = '")[1].split("';")
                        vid = response.text.split("window._pxUuid = '")[1].split("';")
                        blockedUrl = f'https://www.snipes.{self.snipesRegion}/blocked&uuid={uuid}&vid={vid}'
                    except:
                        self.error(f"Failed to parse PX response. Retrying...")
                        time.sleep(int(self.task['DELAY']))
                        continue

                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
                    while cookies["px3"] == "error":
                        cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
        
                    cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                    cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                    self.session.cookies.set_cookie(cookie_obj)
                    self.session.cookies.set_cookie(cookie_obj2)
                    continue
                else:
                    self.error("Blocked by PX. Retrieving new cookie...")
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID)
                    while cookies["px3"] == "error":
                        cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID)
        
                    self.cs = cookies['cs']
                    self.sid = cookies['sid']
                    cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                    cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                    self.session.cookies.set_cookie(cookie_obj)
                    self.session.cookies.set_cookie(cookie_obj2)
                    continue

            if response.status_code == 429:
                self.error("Rate Limited. Rotating Proxy...")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(10)
                continue

            else:
                self.error(f"Failed to get csrf [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue   

    def login(self):
        while True:
            self.prepare("Logging in...")
            try:
                response = self.session.get('https://www.snipes.{}/login'.format(self.snipesRegion), headers={
                    'user-agent': self.userAgent,
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'referer': f'https://www.snipes.{self.snipesRegion}/',
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if response.status_code == 200:

                try:
                    soup = BeautifulSoup(response.text,"html.parser")
                    div = soup.find('div',{'data-cmp':'recommendations'})
                    spans = div.find_all('span')
                    for s in spans:
                        if 'data-value' in str(s):
                            self.s1 = s['data-id']
                            self.s2 = s['data-value']
                except Exception as e:
                    log.info(e)
                    self.error("Failed to login [failed to parse response]. Retrying...")
                    time.sleep(int(self.task["DELAY"]))
                    continue
                
                try:
                    payload = {
                        self.s1:self.s2,
                        'dwfrm_profile_customer_email': self.task["ACCOUNT EMAIL"],
                        'dwfrm_profile_login_password': self.task["ACCOUNT PASSWORD"],
                        'csrf_token': self.csrf
                    }
                except Exception:
                    self.error("Failed to constuct login payload. Retrying...")
                    time.sleep(int(self.task["DELAY"]))
                    continue

                try:
                    response2 = self.session.post('https://www.snipes.{}/authentication?rurl=1&format=ajax'.format(self.snipesRegion),
                    data=payload, headers={
                        'accept': 'application/json, text/javascript, */*; q=0.01',
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'en-US,en;q=0.9',
                        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'origin': f'https://www.snipes.{self.snipesRegion}',
                        'referer':f'https://www.snipes.{self.snipesRegion}/login',
                        'user-agent': self.userAgent,
                        'x-requested-with': 'XMLHttpRequest'
                    })
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    log.info(e)
                    self.error(f"error: {str(e)}")
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    continue

                if response.status_code == 200:

                    try:
                        response = login.json()
                        status = response['success'] 
                    except Exception as e:
                        log.info(e)
                        self.error("Failed to login [failed to parse response]. Retrying...")
                        time.sleep(int(self.task["DELAY"]))
                        continue
                    
                    if status == True:
                        self.success("Successfully logged in")
                        return
                    else:
                        self.error("Failed to login. Retrying...")
                        time.sleep(int(self.task["DELAY"]))
                        continue
                    

                if response.status_code == 403:
                    if 'px-captcha' in response.text:
                        self.error("Blocked by PX Captcha. Solving...")
                        try:
                            uuid = response.text.split("window._pxVid = '")[1].split("';")
                            vid = response.text.split("window._pxUuid = '")[1].split("';")
                            blockedUrl = f'https://www.snipes.{self.snipesRegion}/blocked&uuid={uuid}&vid={vid}'
                        except:
                            self.error(f"Failed to parse PX response. Retrying...")
                            time.sleep(int(self.task['DELAY']))
                            continue

                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                        cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
                        while cookies["px3"] == "error":
                            cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
            
                        cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                        cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                        self.session.cookies.set_cookie(cookie_obj)
                        self.session.cookies.set_cookie(cookie_obj2)
                        continue
                    else:
                        self.error("Blocked by PX. Retrieving new cookie...")
                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                        cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID)
                        while cookies["px3"] == "error":
                            cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID)
            
                        self.cs = cookies['cs']
                        self.sid = cookies['sid']
                        cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                        cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                        self.session.cookies.set_cookie(cookie_obj)
                        self.session.cookies.set_cookie(cookie_obj2)
                        continue

                if response.status_code == 429:
                    self.error("Rate Limited. Rotating Proxy...")
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    time.sleep(10)
                    continue

                else:
                    self.error(f"Failed to login [{str(response.status_code)}]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue 

            if response.status_code == 403:
                if 'px-captcha' in response.text:
                    self.error("Blocked by PX Captcha. Solving...")
                    try:
                        uuid = response.text.split("window._pxVid = '")[1].split("';")
                        vid = response.text.split("window._pxUuid = '")[1].split("';")
                        blockedUrl = f'https://www.snipes.{self.snipesRegion}/blocked&uuid={uuid}&vid={vid}'
                    except:
                        self.error(f"Failed to parse PX response. Retrying...")
                        time.sleep(int(self.task['DELAY']))
                        continue

                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
                    while cookies["px3"] == "error":
                        cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
        
                    cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                    cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                    self.session.cookies.set_cookie(cookie_obj)
                    self.session.cookies.set_cookie(cookie_obj2)
                    continue
                else:
                    self.error("Blocked by PX. Retrieving new cookie...")
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID)
                    while cookies["px3"] == "error":
                        cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID)
        
                    self.cs = cookies['cs']
                    self.sid = cookies['sid']
                    cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                    cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                    self.session.cookies.set_cookie(cookie_obj)
                    self.session.cookies.set_cookie(cookie_obj2)
                    continue

            if response.status_code == 429:
                self.error("Rate Limited. Rotating Proxy...")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(10)
                continue

            else:
                self.error(f"Failed to login [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue   
    
    def addToCart(self):
        while True:
            self.prepare("Adding to cart...")
            
            try:
                payload = {
                    "pid": self.sizePID,
                    "options": [],
                    "quantity": 1 
                }
            except Exception as e:
                self.error(f"Failed to construct atc form ({e}). Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

            
            try:
                response = self.session.post(self.atcUrl, data=payload, headers={
                    'authority': f'www.snipes.{self.snipesRegion}',
                    'accept': 'application/json, text/javascript, */*; q=0.01',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'origin': f'https://www.snipes.{self.snipesRegion}',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': self.userAgent,
                    'x-requested-with': 'XMLHttpRequest'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if response.status_code == 200:
                try:
                    data = response.json()
                    self.uuid = data['cart']['items'][0]['UUID']
                    self.shipmentUUID = data['cart']['items'][0]['shipmentUUID']
                except Exception as e:
                    log.info(e)
                    self.error("Failed to cart [failed to parse response]. Retrying...")
                    time.sleep(int(self.task["DELAY"]))
                    continue

                self.success("Added to cart!")
                updateConsoleTitle(True,False,SITE)
                return

            if response.status_code == 403:
                if 'px-captcha' in response.text:
                    self.error("Blocked by PX Captcha. Solving...")
                    try:
                        uuid = response.text.split("window._pxVid = '")[1].split("';")
                        vid = response.text.split("window._pxUuid = '")[1].split("';")
                        blockedUrl = f'https://www.snipes.{self.snipesRegion}/blocked&uuid={uuid}&vid={vid}'
                    except:
                        self.error(f"Failed to parse PX response. Retrying...")
                        time.sleep(int(self.task['DELAY']))
                        continue

                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
                    while cookies["px3"] == "error":
                        cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
        
                    cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                    cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                    self.session.cookies.set_cookie(cookie_obj)
                    self.session.cookies.set_cookie(cookie_obj2)
                    continue
                else:
                    self.error("Blocked by PX. Retrieving new cookie...")
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID)
                    while cookies["px3"] == "error":
                        cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID)
        
                    self.cs = cookies['cs']
                    self.sid = cookies['sid']
                    cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                    cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                    self.session.cookies.set_cookie(cookie_obj)
                    self.session.cookies.set_cookie(cookie_obj2)
                    continue

            if response.status_code == 429:
                self.error("Rate Limited. Rotating Proxy...")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(10)
                continue
            
            else:
                self.error(f"Failed to cart [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    


    def shipping(self):
        while True:
            self.prepare("Submitting shipping...")

            try:
                if self.snipesRegion == 'com':
                    self.methodId = 'home-delivery'
                else:
                    self.methodId = 'home-delivery_{}'.format(profile['countryCode'].lower())

                payload = {
                    'originalShipmentUUID': self.shipmentUUID,
                    'shipmentUUID': self.shipmentUUID,
                    'dwfrm_shipping_shippingAddress_shippingMethodID': self.methodId,
                    'address-selector': 'new',
                    'dwfrm_shipping_shippingAddress_addressFields_title': 'Herr',
                    'dwfrm_shipping_shippingAddress_addressFields_firstName': self.profile['firstName'],
                    'dwfrm_shipping_shippingAddress_addressFields_lastName': self.profile['lastName'],
                    'dwfrm_shipping_shippingAddress_addressFields_postalCode': self.profile['zip'],
                    'dwfrm_shipping_shippingAddress_addressFields_city': self.profile['city'],
                    'dwfrm_shipping_shippingAddress_addressFields_street': self.profile['addressOne'],
                    'dwfrm_shipping_shippingAddress_addressFields_suite': self.profile['house'],
                    'dwfrm_shipping_shippingAddress_addressFields_address1': self.profile['addressOne'] + ', ' + self.profile['house'],
                    'dwfrm_shipping_shippingAddress_addressFields_address2': self.profile['addressTwo'],
                    'dwfrm_shipping_shippingAddress_addressFields_phone': self.profile['phone'],
                    'dwfrm_shipping_shippingAddress_addressFields_countryCode': self.profile['countryCode'],
                    'dwfrm_shipping_shippingAddress_shippingAddressUseAsBillingAddress': True,
                    'dwfrm_billing_billingAddress_addressFields_title': 'Herr',
                    'dwfrm_billing_billingAddress_addressFields_firstName': self.profile['firstName'],
                    'dwfrm_billing_billingAddress_addressFields_lastName':  self.profile['lastName'],
                    'dwfrm_billing_billingAddress_addressFields_postalCode': self.profile['zip'],
                    'dwfrm_billing_billingAddress_addressFields_city': self.profile['city'],
                    'dwfrm_billing_billingAddress_addressFields_street': self.profile['addressOne'],
                    'dwfrm_billing_billingAddress_addressFields_suite': self.profile['house'],
                    'dwfrm_billing_billingAddress_addressFields_address1': self.profile['addressOne'] + ', ' + self.profile['house'],
                    'dwfrm_billing_billingAddress_addressFields_address2': self.profile['addressTwo'],
                    'dwfrm_billing_billingAddress_addressFields_countryCode': self.profile['countryCode'],
                    'dwfrm_billing_billingAddress_addressFields_phone': self.profile['phone'],
                    'dwfrm_contact_email': self.profile['email'],
                    'dwfrm_contact_phone': self.profile['phone'],
                    'csrf_token': self.csrf
                }
            except Exception as e:
                self.error(f"Failed to construct shipping form ({e}). Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
                
            try:
                response = self.session.post('https://www.snipes.{}{}/CheckoutShippingServices-SubmitShipping?format=ajax'.format(self.snipesRegion,self.demandWareBase),
                data=payload, headers={
                    'authority': f'www.snipes.{self.snipesRegion}',
                    'accept': 'application/json, text/javascript, */*; q=0.01',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'origin': f'https://www.snipes.{self.snipesRegion}',
                    'referer': f'https://www.snipes.{self.snipesRegion}/checkout?stage=shipping',
                    'user-agent': self.userAgent,
                    'x-requested-with': 'XMLHttpRequest'
                })

            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

        
            if response.status_code == 200:
                self.warning("Successfully set shipping")
                return

            if response.status_code == 403:
                if 'px-captcha' in response.text:
                    self.error("Blocked by PX Captcha. Solving...")
                    try:
                        uuid = response.text.split("window._pxVid = '")[1].split("';")
                        vid = response.text.split("window._pxUuid = '")[1].split("';")
                        blockedUrl = f'https://www.snipes.{self.snipesRegion}/blocked&uuid={uuid}&vid={vid}'
                    except:
                        self.error(f"Failed to parse PX response. Retrying...")
                        time.sleep(int(self.task['DELAY']))
                        continue

                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
                    while cookies["px3"] == "error":
                        cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
        
                    cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                    cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                    self.session.cookies.set_cookie(cookie_obj)
                    self.session.cookies.set_cookie(cookie_obj2)
                    continue
                else:
                    self.error("Blocked by PX. Retrieving new cookie...")
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID)
                    while cookies["px3"] == "error":
                        cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID)
        
                    self.cs = cookies['cs']
                    self.sid = cookies['sid']
                    cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                    cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                    self.session.cookies.set_cookie(cookie_obj)
                    self.session.cookies.set_cookie(cookie_obj2)
                    continue

            if response.status_code == 429:
                self.error("Rate Limited. Rotating Proxy...")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(10)
                continue

            else:
                self.error(f"Failed to set shipping [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def paymentMethod(self):
        while True:
            self.prepare("Setting payment method...")

            try:
                method = ''
                if self.task["PAYMENT"].strip().lower() == 'paypal' or 'pp': method = "Paypal"
                elif self.task["PAYMENT"].strip().lower() == 'bt': method = "BANK_TRANSFER"
                elif self.task["PAYMENT"].strip().lower() == 'card' or 'cc': method = "CREDIT_CARD"
                else:
                    self.error("Invalid payment method. Exiting...")
                    time.sleep(5)
                    sys.exit()

                payload = {
                    'dwfrm_billing_paymentMethod': method,
                    'dwfrm_giftCard_cardNumber': '',
                    'dwfrm_giftCard_pin': '',
                    'csrf_token': self.csrf
                }
            except Exception as e:
                self.error(f"Failed to construct payment form ({e}). Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue    
            
            try:
                response = self.session.post('https://www.snipes.{}{}/CheckoutServices-SubmitPayment?format=ajax'.format(self.snipesRegion,self.demandWareBase),
                data=payload, headers={
                    'authority': f'www.snipes.{self.snipesRegion}',
                    'accept': 'application/json, text/javascript, */*; q=0.01',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'origin': f'https://www.snipes.{self.snipesRegion}',
                    'referer': f'https://www.snipes.{self.snipesRegion}/checkout?stage=payment',
                    'user-agent': self.userAgent,
                    'x-requested-with': 'XMLHttpRequest'
                })

            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if response.status_code == 200:
                self.warning("Set payment method")
                return

            if response.status_code == 403:
                if 'px-captcha' in response.text:
                    self.error("Blocked by PX Captcha. Solving...")
                    try:
                        uuid = response.text.split("window._pxVid = '")[1].split("';")
                        vid = response.text.split("window._pxUuid = '")[1].split("';")
                        blockedUrl = f'https://www.snipes.{self.snipesRegion}/blocked&uuid={uuid}&vid={vid}'
                    except:
                        self.error(f"Failed to parse PX response. Retrying...")
                        time.sleep(int(self.task['DELAY']))
                        continue

                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
                    while cookies["px3"] == "error":
                        cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
        
                    cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                    cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                    self.session.cookies.set_cookie(cookie_obj)
                    self.session.cookies.set_cookie(cookie_obj2)
                    continue
                else:
                    self.error("Blocked by PX. Retrieving new cookie...")
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID)
                    while cookies["px3"] == "error":
                        cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID)
        
                    self.cs = cookies['cs']
                    self.sid = cookies['sid']
                    cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                    cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                    self.session.cookies.set_cookie(cookie_obj)
                    self.session.cookies.set_cookie(cookie_obj2)
                    continue

            if response.status_code == 429:
                self.error("Rate Limited. Rotating Proxy...")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(10)
                continue

            else:
                self.error(f"Failed to set payment method [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def placeOrder(self):
        while True:
            self.prepare("Placing Order...")


            try:
                response = self.session.post('https://www.snipes.{}{}/CheckoutServices-PlaceOrder?format=ajax'.format(self.snipesRegion,self.demandWareBase),
                data={"format": "ajax"}, headers={
                    'authority': f'www.snipes.{self.snipesRegion}',
                    'accept': 'application/json, text/javascript, */*; q=0.01',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'origin': f'https://www.snipes.{self.snipesRegion}',
                    'referer': f'https://www.snipes.{self.snipesRegion}/checkout?stage=payment',
                    'user-agent': self.userAgent,
                    'x-requested-with': 'XMLHttpRequest'
                })

            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if response.status_code in [200,302]:

                try:
                    data = response.json()

                    if self.task['PAYMENT'].strip().lower() == 'paypal':
                        updateConsoleTitle(False,True,SITE)
                        place_order_res = str(data["continueUrl"])
                        self.webhookData['url'] = storeCookies(
                            place_order_res,
                            self.session,
                            self.webhookData['product'],
                            self.webhookData['image'],
                            self.webhookData['price'],
                            False
                        )

                    if self.task['PAYMENT'].strip().lower() == 'card':
                        updateConsoleTitle(False,True,SITE)
                        place_order_res = str(data["continueUrl"])

                        self.webhookData['url'] = storeCookies(
                            place_order_res,
                            self.session,
                            self.webhookData['product'],
                            self.webhookData['image'],
                            self.webhookData['price'],
                            False
                        )

                    if self.task['PAYMENT'].strip().lower() == 'bt':
                        updateConsoleTitle(False,True,SITE)
                        place_order_res = str(data["orderID"])

                except Exception as e:
                    log.info(e)
                    self.error("Failed to place order. Retrying...")

                self.success("Checkout successful")
                return

            if response.status_code == 403:
                if 'px-captcha' in response.text:
                    self.error("Blocked by PX Captcha. Solving...")
                    try:
                        uuid = response.text.split("window._pxVid = '")[1].split("';")
                        vid = response.text.split("window._pxUuid = '")[1].split("';")
                        blockedUrl = f'https://www.snipes.{self.snipesRegion}/blocked&uuid={uuid}&vid={vid}'
                    except:
                        self.error(f"Failed to parse PX response. Retrying...")
                        time.sleep(int(self.task['DELAY']))
                        continue

                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
                    while cookies["px3"] == "error":
                        cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
        
                    cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                    cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                    self.session.cookies.set_cookie(cookie_obj)
                    self.session.cookies.set_cookie(cookie_obj2)
                    continue
                else:
                    self.error("Blocked by PX. Retrieving new cookie...")
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID)
                    while cookies["px3"] == "error":
                        cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID)
        
                    self.cs = cookies['cs']
                    self.sid = cookies['sid']
                    cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                    cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                    self.session.cookies.set_cookie(cookie_obj)
                    self.session.cookies.set_cookie(cookie_obj2)
                    continue

            if response.status_code == 429:
                self.error("Rate Limited. Rotating Proxy...")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(10)
                continue

            else:
                self.error(f"Failed to set payment method [{str(response.status_code)}]. Retrying...")
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
                    size=self.webhookData['size'],
                    price=self.webhookData['price'],
                    paymentMethod=self.task['PAYMENT'].strip().title(),
                    product=self.webhookData['product_url'],
                    profile=self.task["PROFILE"],
                    proxy=self.webhookData['proxy'],
                    speed=self.webhookData['speed'],
                    region=self.profile['countryCode'].lower()
                )
                self.secondary("Sent to discord!")
                while True:
                    pass
            except:
                self.alert("Failed to send webhook. Checkout here ==> {}".format(self.webhookData['url']))
                while True:
                    pass