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
from utils.px import PX
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies, updateConsoleTitle, urlEncode, randomUA, randomString, scraper)
SITE = 'SNIPES'


class SNIPES:
    def __init__(self, task,taskName):
        self.task = task
        self.sess = requests.session()
        self.taskID = taskName

        twoCap = loadSettings()["2Captcha"]
        self.session = scraper()
        
        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
        self.countryCode = loadProfile(self.task["PROFILE"])["countryCode"]
        self.logged = False


        self.collect()
    
    def collect(self):
        self.UA = randomUA()
        self.refer = self.task["PRODUCT"]

        # self.cookies = {
            # "px3":"",
            # "vid":"e244a651-188c-11eb-8079-d3c780d947ac"
        # }

        if 'https' in self.task['PRODUCT']:
            try:
                self.snipesRegion = self.task["PRODUCT"].split('snipes.')[1].split('/')[0]
                self.pid = '00' + self.task['PRODUCT'].split('-00')[1].split('.html')[0]
            except:
                logger.error(SITE,self.taskID,'Failed to parse PID. Please check it is a valid SNIPES url.')
                time.sleep(5)
                sys.exit()
        else:
            if self.countryCode.upper() == "DE":
                self.snipesRegion = 'com'
            if self.countryCode.upper() == "AT":
                self.snipesRegion = 'at'
            if self.countryCode.upper() == "NL":
                self.snipesRegion = 'nl'
            if self.countryCode.upper() == "FR":
                self.snipesRegion = 'fr'
            if self.countryCode.upper() == "CH":
                self.snipesRegion = 'ch'
            if self.countryCode.upper() == "IT":
                self.snipesRegion = 'it'
            if self.countryCode.upper() == "ES":
                self.snipesRegion = 'es'
            if self.countryCode.upper() == "BE":
                self.snipesRegion = 'be'
                
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
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'referer': f'https://www.snipes.{self.snipesRegion}/',
        }
        self.start = time.time()

        self.queryUrl = 'https://www.snipes.{}/p/{}.html?dwvar_{}_color=a&format=ajax'.format(self.snipesRegion,self.pid,self.pid)
        # https://www.snipes./p/00013801882838.html?dwvar_00013801882838_color=a&format=ajax
        self.query()


    def query(self):
        logger.prepare(SITE,self.taskID,'Getting product info...')
        try:
            retrieve = self.session.get(self.queryUrl)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
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
            self.demandWareBase = data["product"]["quantities"][0]["url"].split('Product-Variation')[0]
            if self.snipesRegion != 'com':
                self.atcUrl = f'https://www.snipes.{self.snipesRegion}{self.demandWareBase}Cart-AddProduct?format=ajax'
            else:
                self.atcUrl = f'https://www.snipes.{self.snipesRegion}/add-product?format=ajax'
            allSizes = []
            sizes = []
            for s in data["product"]["variationAttributes"][0]["values"]:
                sizes.append(s["value"])
                sizePid = s["variantId"]
                if sizePid in ['None', None]:
                    sizePid = s['pid']
                allSizes.append('{}:{}'.format(s["value"],sizePid))

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
                            logger.warning(SITE,self.taskID,f'Found Size => {self.size}')

            
            elif self.task["SIZE"].lower() == "random":
                selected = random.choice(allSizes)
                self.size = selected.split(":")[0]
                self.sizePID = selected.split(":")[1]
                logger.warning(SITE,self.taskID,f'Found Size => {self.size}')
            
            if self.task["ACCOUNT EMAIL"] != "" and self.task["ACCOUNT PASSWORD"] != "":
                self.login()
            else:
                self.addToCart()

        if retrieve.status_code == 403:
            if 'px-captcha' in retrieve.text:
                uuid = retrieve.text.split("window._pxVid = '")[1].split("';")
                vid = retrieve.text.split("window._pxUuid = '")[1].split("';")
                blockedUrl = f'https://www.snipes.{self.snipesRegion}/blocked&uuid={uuid}&vid={vid}'
                # Captcha required
                logger.error(SITE,self.taskID,'PX Captcha Found. Solving...')
                time.sleep(int(self.task["DELAY"]))

                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
                while cookies["px3"] == "error":
                    cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
    
                cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                self.session.cookies.set_cookie(cookie_obj)
                self.session.cookies.set_cookie(cookie_obj2)

                self.query()
            else:
                logger.error(SITE,self.taskID,'Forbidden. Retrying...')
                time.sleep(int(self.task["DELAY"]))
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

            


    def login(self):
        if self.logged == True:
            self.addToCart()
        logger.prepare(SITE,self.taskID,'Logging in...')

        try:
            loginPage = self.session.get('https://www.snipes.{}/login'.format(self.snipesRegion))
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.login()

        soup = BeautifulSoup(loginPage.text,"html.parser")
        div = soup.find('div',{'data-cmp':'recommendations'})
        # self.csrf = soup.find('input',{'name':'csrf_token'})['value']
        try:
            spans = div.find_all('span')
            for s in spans:
                if 'data-value' in str(s):
                    self.s1 = s['data-id']
                    self.s2 = s['data-value']
        except Exception as e:
            log.info(e)
            pass
        


        payload = {
            self.s1:self.s2,
            'dwfrm_profile_customer_email': self.task["ACCOUNT EMAIL"],
            'dwfrm_profile_login_password': self.task["ACCOUNT PASSWORD"],
            'csrf_token': self.csrf
        }
        self.session.headers = {}
        self.session.headers = {
            'authority': f'www.snipes.{self.snipesRegion}',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': f'https://www.snipes.{self.snipesRegion}',
            'referer':f'https://www.snipes.{self.snipesRegion}/login',
            'user-agent': self.UA,
            'x-requested-with': 'XMLHttpRequest'
        }
        try:
            login = self.session.post('https://www.snipes.{}/authentication?rurl=1&format=ajax'.format(self.snipesRegion),data=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.login()




        if login.status_code == 200:

            try:
                response = login.json()
                status = response['success'] 
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to login. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.login()

            logger.warning(SITE,self.taskID,'Successfully Logged in.')
            self.logged = True
            
            
            self.addToCart()

        if login.status_code == 403:
            if 'px-captcha' in login.text:
                uuid = login.text.split("window._pxVid = '")[1].split("';")
                vid = login.text.split("window._pxUuid = '")[1].split("';")
                blockedUrl = f'https://www.snipes.{self.snipesRegion}/blocked&uuid={uuid}&vid={vid}'
                # Captcha required
                logger.error(SITE,self.taskID,'PX Captcha Found. Solving...')
                time.sleep(int(self.task["DELAY"]))

                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
                while cookies["px3"] == "error":
                    cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
    
                cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                self.session.cookies.set_cookie(cookie_obj)
                self.session.cookies.set_cookie(cookie_obj2)

                self.query()
            else:
                logger.error(SITE,self.taskID,'Forbidden. Retrying...')
                time.sleep(int(self.task["DELAY"]))
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
                self.query()

        if login.status_code == 429:
            logger.error(SITE,self.taskID,'Rate Limit (Sleeping). Retrying...')
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(10)
            self.UA = randomUA()
            self.login()

        elif login.status_code not in [200,403]:
            logger.error(SITE,self.taskID,'Failed to cart [{}]. Retrying...'.format(login.status_code))
            time.sleep(int(self.task["DELAY"]))
            self.login()
    
    
    def addToCart(self):

        logger.prepare(SITE,self.taskID,'Adding to cart...')
        self.session.headers = {}
        self.session.headers = {
            'authority': f'www.snipes.{self.snipesRegion}',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': f'https://www.snipes.{self.snipesRegion}',
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
            cart = self.session.post(self.atcUrl,data=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
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
                else:
                    logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.addToCart()
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                if self.task["SIZE"].lower() == "random":
                    self.query()
                else:
                    self.addToCart()


            updateConsoleTitle(True,False,SITE)
            logger.warning(SITE,self.taskID,'Successfully Carted')
            self.shipping()

        # if cart.status_code == 410:
            # print(cart.text)
        
        if cart.status_code == 403:
            if 'px-captcha' in cart.text:
                uuid = cart.text.split("window._pxVid = '")[1].split("';")
                vid = cart.text.split("window._pxUuid = '")[1].split("';")
                blockedUrl = f'https://www.snipes.{self.snipesRegion}/blocked&uuid={uuid}&vid={vid}'
                # Captcha required
                logger.error(SITE,self.taskID,'PX Captcha Found. Solving...')
                time.sleep(int(self.task["DELAY"]))

                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
                while cookies["px3"] == "error":
                    cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
    
                cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                self.session.cookies.set_cookie(cookie_obj)
                self.session.cookies.set_cookie(cookie_obj2)

                self.addToCart()
            else:
                logger.error(SITE,self.taskID,'Forbidden. Retrying...')
                time.sleep(int(self.task["DELAY"]))
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
                self.addToCart()

        if cart.status_code == 429:
            logger.error(SITE,self.taskID,'Rate Limit. Retrying...')
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.UA = randomUA()
            self.refer = self.task["PRODUCT"] + "#%253F_={}".format(randomString(20))
            current_px3 = self.session.cookies.get_dict()["_px3"]
            current_pxvid = self.session.cookies.get_dict()["_pxvid"]

            self.session.cookies.clear()

            cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=current_px3)
            cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=current_pxvid)
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





    def shipping(self):
        logger.prepare(SITE,self.taskID,'Submitting shipping...')
        profile = loadProfile(self.task["PROFILE"])

        try:
            getShiping = self.session.get('https://www.snipes.{}/Checkout'.format(self.snipesRegion))
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.shipping()
        
        try:
            soup = BeautifulSoup(getShiping.text,'html.parser')
            self.csrf = soup.find('input',{'name':'csrf_token'})['value']
        except:
            pass


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
            'dwfrm_shipping_shippingAddress_addressFields_firstName': profile['firstName'],
            'dwfrm_shipping_shippingAddress_addressFields_lastName': profile['lastName'],
            'dwfrm_shipping_shippingAddress_addressFields_postalCode': profile['zip'],
            'dwfrm_shipping_shippingAddress_addressFields_city': profile['city'],
            'dwfrm_shipping_shippingAddress_addressFields_street': profile['addressOne'],
            'dwfrm_shipping_shippingAddress_addressFields_suite': profile['house'],
            'dwfrm_shipping_shippingAddress_addressFields_address1': profile['addressOne'] + ', ' + profile['house'],
            'dwfrm_shipping_shippingAddress_addressFields_address2': profile['addressTwo'],
            'dwfrm_shipping_shippingAddress_addressFields_phone': profile['phone'],
            'dwfrm_shipping_shippingAddress_addressFields_countryCode': profile['countryCode'],
            'dwfrm_shipping_shippingAddress_shippingAddressUseAsBillingAddress': True,
            'dwfrm_billing_billingAddress_addressFields_title': 'Herr',
            'dwfrm_billing_billingAddress_addressFields_firstName': profile['firstName'],
            'dwfrm_billing_billingAddress_addressFields_lastName':  profile['lastName'],
            'dwfrm_billing_billingAddress_addressFields_postalCode': profile['zip'],
            'dwfrm_billing_billingAddress_addressFields_city': profile['city'],
            'dwfrm_billing_billingAddress_addressFields_street': profile['addressOne'],
            'dwfrm_billing_billingAddress_addressFields_suite': profile['house'],
            'dwfrm_billing_billingAddress_addressFields_address1': profile['addressOne'] + ', ' + profile['house'],
            'dwfrm_billing_billingAddress_addressFields_address2': profile['addressTwo'],
            'dwfrm_billing_billingAddress_addressFields_countryCode': profile['countryCode'],
            'dwfrm_billing_billingAddress_addressFields_phone': profile['phone'],
            'dwfrm_contact_email': profile['email'],
            'dwfrm_contact_phone': profile['phone'],
            'csrf_token': self.csrf
        }
        self.session.headers = {}
        self.session.headers = {
            'authority': f'www.snipes.{self.snipesRegion}',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': f'https://www.snipes.{self.snipesRegion}',
            'referer': f'https://www.snipes.{self.snipesRegion}/checkout?stage=shipping',
            'user-agent': self.UA,
            'x-requested-with': 'XMLHttpRequest'
        }
        try:
            submitShipping = self.session.post('https://www.snipes.{}{}/CheckoutShippingServices-SubmitShipping?format=ajax'.format(self.snipesRegion,self.demandWareBase),data=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.shipping()
        if submitShipping.status_code == 200:
            logger.warning(SITE,self.taskID,'Shipping submitted successfully')
            self.payment_method()

        if submitShipping.status_code == 429:
            logger.error(SITE,self.taskID,'Rate Limit (Sleeping). Retrying...')
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.UA = randomUA()
            time.sleep(10)
            self.shipping()

        if submitShipping.status_code == 403:
            if 'px-captcha' in submitShipping.text:
                uuid = submitShipping.text.split("window._pxVid = '")[1].split("';")
                vid = submitShipping.text.split("window._pxUuid = '")[1].split("';")
                blockedUrl = f'https://www.snipes.{self.snipesRegion}/blocked&uuid={uuid}&vid={vid}'
                # Captcha required
                logger.error(SITE,self.taskID,'PX Captcha Found. Solving...')
                time.sleep(int(self.task["DELAY"]))

                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
                while cookies["px3"] == "error":
                    cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
    
                cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                self.session.cookies.set_cookie(cookie_obj)
                self.session.cookies.set_cookie(cookie_obj2)

                self.shipping()
            else:
                logger.error(SITE,self.taskID,'Forbidden. Retrying...')
                time.sleep(int(self.task["DELAY"]))
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
                self.shipping()
        elif submitShipping.status_code not in [200,403]:
            logger.error(SITE,self.taskID,'Failed to submit shipping. Retrying...')
            time.sleep(int(self.task("DELAY")))
            self.shipping()



    def payment_method(self):
        logger.prepare(SITE,self.taskID,'Setting payment method...')
        if self.task["PAYMENT"].lower() == "paypal":
            method = 'Paypal'
        if self.task["PAYMENT"].lower() == "bt":
            method = 'BANK_TRANSFER'
        if self.task["PAYMENT"].lower() == "card":
            method = 'CREDIT_CARD'
        payload = {
            'dwfrm_billing_paymentMethod': method,
            'dwfrm_giftCard_cardNumber': '',
            'dwfrm_giftCard_pin': '',
            'csrf_token': self.csrf
        }
        self.session.headers = {}
        self.session.headers = {
            'authority': f'www.snipes.{self.snipesRegion}',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': f'https://www.snipes.{self.snipesRegion}',
            'referer': f'https://www.snipes.{self.snipesRegion}/checkout?stage=payment',
            'user-agent': self.UA,
            'x-requested-with': 'XMLHttpRequest'
        }
        try:
            submitPayment= self.session.post('https://www.snipes.{}{}/CheckoutServices-SubmitPayment?format=ajax'.format(self.snipesRegion,self.demandWareBase),data=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.payment_method()

        if submitPayment.status_code == 200:
            logger.warning(SITE,self.taskID,'Successfully set payment method')
            if self.task["PAYMENT"].lower() == "paypal":
                self.placeOrder_pp()
            if self.task["PAYMENT"].lower() == "bt":
                self.placeOrder_bt()
            if self.task["PAYMENT"].lower() == "card":
                self.placeOrder_card()

        if submitPayment.status_code == 429:
            logger.error(SITE,self.taskID,'Rate Limit (Sleeping). Retrying...')
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.UA = randomUA()
            time.sleep(10)
            self.payment_method()

        if submitPayment.status_code == 403:
            if 'px-captcha' in submitPayment.text:
                uuid = submitPayment.text.split("window._pxVid = '")[1].split("';")
                vid = submitPayment.text.split("window._pxUuid = '")[1].split("';")
                blockedUrl = f'https://www.snipes.{self.snipesRegion}/blocked&uuid={uuid}&vid={vid}'
                # Captcha required
                logger.error(SITE,self.taskID,'PX Captcha Found. Solving...')
                time.sleep(int(self.task["DELAY"]))

                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
                while cookies["px3"] == "error":
                    cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
    
                cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                self.session.cookies.set_cookie(cookie_obj)
                self.session.cookies.set_cookie(cookie_obj2)

                self.payment_method()
            else:
                logger.error(SITE,self.taskID,'Forbidden. Retrying...')
                time.sleep(int(self.task["DELAY"]))
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
                self.payment_method()

        elif submitPayment.status_code not in [200,403]:
            logger.error(SITE,self.taskID,'Failed to submit payment method. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.payment_method()
        

    def placeOrder_bt(self):
        logger.prepare(SITE,self.taskID,'Placing order...')
        self.session.headers = {}
        self.session.headers = {
            'authority': f'www.snipes.{self.snipesRegion}',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': f'https://www.snipes.{self.snipesRegion}',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'referer': f'https://www.snipes.{self.snipesRegion}/checkout?stage=placeOrder',
            'user-agent': self.UA,
            'x-requested-with': 'XMLHttpRequest'
        }
        try:
            place = self.session.post('https://www.snipes.{}{}/CheckoutServices-PlaceOrder?format=ajax'.format(self.snipesRegion,self.demandWareBase))
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.placeOrder_bt()


        if place.status_code in [200,302]:

            try:
                response = place.json()
            except Exception as e:
                logger.error(SITE,self.taskID,'Failed to place order. Retrying...')
                log.info(e)
                time.sleep(int(self.task["DELAY"]))
                self.placeOrder_bt()

            self.end = time.time() - self.start
            updateConsoleTitle(False,True,SITE)
            logger.alert(SITE,self.taskID,'Order Placed ({}). Check your email to plete bank transfer.'.format(response["orderID"]))


            sendNotification(SITE,self.productTitle)
            try:
                discord.success(
                    webhook=loadSettings()["webhook"],
                    site=SITE,
                    image=self.productImage,
                    title=self.productTitle,
                    size=self.size,
                    price=self.productPrice,
                    paymentMethod='Bank Transfer',
                    profile=self.task["PROFILE"],
                    product=self.task["PRODUCT"],
                    proxy=self.session.proxies,
                    speed=self.end,
                    region=self.countryCode
                )
                while True:
                    pass
            except Exception as e:
                logger.alert(SITE,self.taskID,'Failed to send webhook.')
        
        if place.status_code == 429:
            logger.error(SITE,self.taskID,'Rate Limit (Sleeping). Retrying...')
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.UA = randomUA()
            time.sleep(10)
            self.placeOrder_bt()

        if place.status_code == 403:
            if 'px-captcha' in place.text:
                uuid = place.text.split("window._pxVid = '")[1].split("';")
                vid = place.text.split("window._pxUuid = '")[1].split("';")
                blockedUrl = f'https://www.snipes.{self.snipesRegion}/blocked&uuid={uuid}&vid={vid}'
                # Captcha required
                logger.error(SITE,self.taskID,'PX Captcha Found. Solving...')
                time.sleep(int(self.task["DELAY"]))

                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
                while cookies["px3"] == "error":
                    cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
    
                cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                self.session.cookies.set_cookie(cookie_obj)
                self.session.cookies.set_cookie(cookie_obj2)

                self.placeOrder_bt()
            else:
                logger.error(SITE,self.taskID,'Forbidden. Retrying...')
                time.sleep(int(self.task["DELAY"]))
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
                self.placeOrder_bt()

        elif place.status_code not in [200,403]:
            try:
                response = place.json()
                msg = response["errorMessage"]
            except Exception as e:
                log.info(e)
                msg = 'n/a'

            log.info(str(response))
            logger.error(SITE,self.taskID,f'Failed to place order [{msg}]. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

    def placeOrder_card(self):
        logger.prepare(SITE,self.taskID,'Placing order...')
        self.session.headers = {}
        self.session.headers = {
            'authority': f'www.snipes.{self.snipesRegion}',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': f'https://www.snipes.{self.snipesRegion}',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'referer': f'https://www.snipes.{self.snipesRegion}/checkout?stage=placeOrder',
            'user-agent': self.UA,
            'x-requested-with': 'XMLHttpRequest'
        }
        try:
            place = self.session.post('https://www.snipes.{}{}/CheckoutServices-PlaceOrder?format=ajax'.format(self.snipesRegion,self.demandWareBase))
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.placeOrder_card()

        if place.status_code in [200,302]:

            try:
                response = place.json()
                response['continueUrl']
            except Exception as e:
                logger.error(SITE,self.taskID,'Failed to place order. Retrying...')
                log.info(e)
                log.info(str(place.text))
                time.sleep(int(self.task["DELAY"]))
                self.placeOrder_card()

            profile = loadProfile(self.task["PROFILE"])
            if profile == None:
                logger.error(SITE,self.taskID,'Profile Not Found.')
                time.sleep(10)
                sys.exit()
                number = profile["card"]["cardNumber"]
                if str(number[0]) == "4":
                    cType = '1_Card&1091'
                if str(number[0]) == "5":
                    cType = '1_Card&1090'
                else:
                    cType = None


            self.end = time.time() - self.start
            updateConsoleTitle(False,True,SITE)
            logger.alert(SITE,self.taskID,'Sending card checkout to discord...'.format())
            url = storeCookies( response['continueUrl'],self.session, self.productTitle, self.productImage, self.productPrice)


            sendNotification(SITE,self.productTitle)
            try:
                discord.success(
                    webhook=loadSettings()["webhook"],
                    site=SITE,
                    url=url,
                    image=self.productImage,
                    title=self.productTitle,
                    size=self.size,
                    price=self.productPrice,
                    paymentMethod='Bank Transfer',
                    profile=self.task["PROFILE"],
                    product=self.task["PRODUCT"],
                    proxy=self.session.proxies,
                    speed=self.end,
                    region=self.countryCode
                )
                while True:
                    pass
            except Exception as e:
                logger.alert(SITE,self.taskID,'Failed to send webhook. Checkout here ==> {}'.format(url))

        if place.status_code == 403:
            if 'px-captcha' in place.text:
                uuid = place.text.split("window._pxVid = '")[1].split("';")
                vid = place.text.split("window._pxUuid = '")[1].split("';")
                blockedUrl = f'https://www.snipes.{self.snipesRegion}/blocked&uuid={uuid}&vid={vid}'
                # Captcha required
                logger.error(SITE,self.taskID,'PX Captcha Found. Solving...')
                time.sleep(int(self.task["DELAY"]))

                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
                while cookies["px3"] == "error":
                    cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
    
                cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                self.session.cookies.set_cookie(cookie_obj)
                self.session.cookies.set_cookie(cookie_obj2)

                self.placeOrder_card()
            else:
                logger.error(SITE,self.taskID,'Forbidden. Retrying...')
                time.sleep(int(self.task["DELAY"]))
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
                self.placeOrder_card()

        if place.status_code == 429:
            logger.error(SITE,self.taskID,'Rate Limit (Sleeping). Retrying...')
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.UA = randomUA()
            time.sleep(10)
            self.placeOrder_card()

        elif place.status_code not in [200,403]:
            try:
                response = place.json()
                msg = response["errorMessage"]
            except Exception as e:
                log.info(e)
                msg = 'n/a'

            log.info(str(response))
            logger.error(SITE,self.taskID,f'Failed to place order [{msg}]. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

    def placeOrder_pp(self):
        logger.prepare(SITE,self.taskID,'Placing order...')
        self.session.headers = {}
        self.session.headers = {
            'authority': f'www.snipes.{self.snipesRegion}',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': f'https://www.snipes.{self.snipesRegion}',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'referer': f'https://www.snipes.{self.snipesRegion}/checkout?stage=placeOrder',
            'user-agent': self.UA,
            'x-requested-with': 'XMLHttpRequest'
        }
        try:
            place = self.session.post('https://www.snipes.{}{}/CheckoutServices-PlaceOrder?format=ajax'.format(self.snipesRegion,self.demandWareBase))
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.placeOrder_pp()


        if place.status_code in [200,302]:
            try:
                response = place.json()
                cUrl = response["continueUrl"]
            except Exception as e:
                log.info(e)
                log.info(str(response))
                time.sleep(int(self.task["DELAY"]))
                if place.json()['cartError'] == True:
                    logger.error(SITE,self.taskID,'Failed to place order (Cart Error) Redirect=> {}. Retrying...'.format(place.json()['redirectUrl']))
                    self.query()
                else:
                    logger.error(SITE,self.taskID,'Failed to place order. Retrying...')
                    self.addToCart()
            
            if "paypal" in cUrl:
                logger.warning(SITE,self.taskID,'Order placed')
                self.end = time.time() - self.start
                updateConsoleTitle(False,True,SITE)
                logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')
    
                url = storeCookies(cUrl,self.session, self.productTitle, self.productImage, self.productPrice)
    
                sendNotification(SITE,self.productTitle)
                try:
                    discord.success(
                        webhook=loadSettings()["webhook"],
                        site=SITE,
                        url=url,
                        image=self.productImage,
                        title=self.productTitle,
                        size=self.size,
                        price=self.productPrice,
                        paymentMethod='PayPal',
                        profile=self.task["PROFILE"],
                        product=self.task["PRODUCT"],
                        proxy=self.session.proxies,
                        speed=self.end,
                        region=self.countryCode
                    )
                    while True:
                        pass
                except Exception as e:
                    logger.alert(SITE,self.taskID,'Failed to send webhook. Checkout here ==> {}'.format(url))
            
            else:
                logger.error(SITE,self.taskID,'Failed to place order (Cart may have duplicates). Retrying...')
                log.info(str(response))
                time.sleep(int(self.task["DELAY"]))
                self.placeOrder_pp()

        if place.status_code == 403:
            if 'px-captcha' in place.text:
                uuid = place.text.split("window._pxVid = '")[1].split("';")
                vid = place.text.split("window._pxUuid = '")[1].split("';")
                blockedUrl = f'https://www.snipes.{self.snipesRegion}/blocked&uuid={uuid}&vid={vid}'
                # Captcha required
                logger.error(SITE,self.taskID,'PX Captcha Found. Solving...')
                time.sleep(int(self.task["DELAY"]))

                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
                while cookies["px3"] == "error":
                    cookies = PX.captchaSolve(self.session, f'https://www.snipes.{self.snipesRegion}', self.taskID, SITE, blockedUrl, self.cs, self.sid)
    
                cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                self.session.cookies.set_cookie(cookie_obj)
                self.session.cookies.set_cookie(cookie_obj2)

                self.placeOrder_pp()
            else:
                logger.error(SITE,self.taskID,'Forbidden. Retrying...')
                time.sleep(int(self.task["DELAY"]))
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
                self.placeOrder_pp()

        if place.status_code == 429:
            logger.error(SITE,self.taskID,'Rate Limit (Sleeping). Retrying...')
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.UA = randomUA()
            time.sleep(10)
            self.placeOrder_pp()

        elif place.status_code not in [200,403]:
            try:
                response = place.json()
                msg = response["errorMessage"]
            except Exception as e:
                log.info(e)
                msg = 'n/a'

            log.info(str(place.text))
            logger.error(SITE,self.taskID,f'Failed to place order [{msg}]. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()
        



