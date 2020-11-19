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
from urllib.parse import urlencode, quote_plus


from utils.logger import logger
from utils.webhook import discord
from utils.log import log
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies, updateConsoleTitle)
SITE = 'CORNER-STREET'



class CORNERSTREET:
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
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'authority': 'www.cornerstreet.fr'
            })
            logger.success(SITE,self.taskID,'Solved Cloudflare')
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.collect()

        self.frontend = retrieve.headers['set-cookie'].split('frontend=')[1].split(';')[0]
        self.frontend_cid = retrieve.headers['set-cookie'].split('frontend_cid=')[1].split(';')[0]

        if retrieve.status_code == 200:
            self.start = time.time()
            logger.success(SITE,self.taskID,'Got product page')
            try:
                soup = BeautifulSoup(retrieve.text, "html.parser")
                self.productTitle = soup.find("title").text.split('-')[0]
                imgs = soup.find('ul',{'class':'product-image-thumbs row'})
                self.productImage = imgs.find_all('li')[0].find('img')["src"]

                self.atcUrl = soup.find("form", {"id": "product_addtocart_form"})["action"] #.replace("checkout/cart", "oxajax/cart")
                self.formKey = soup.find("input", {"name": "form_key"})["value"]
                self.productId = soup.find("input", {"name": "product"})["value"]
                self.productPrice = soup.find("span",{"class":"price"}).text
                self.attributeId = soup.find("select", {
                                            "class": "required-entry super-attribute-select"})["id"].split("attribute")[1]
    
                regex = r"{\"attributes\":(.*?)}}\)"
                matches = re.search(regex, retrieve.text, re.MULTILINE)
                if matches:
                    productData = json.loads(
                        matches.group()[:-1])["attributes"][self.attributeId]
    
                    allSizes = []
                    sizes = []
                    for s in productData["options"]:
                        allSizes.append('{}:{}:{}'.format(s["label"],s["products"][0],s["id"]))
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
        logger.prepare(SITE,self.taskID,'Carting products...')
        payload = {
            'form_key': self.formKey,
            'product': self.productId,
            'related_product': '',
            f'super_attribute[{self.attributeId}]': self.sizeID,
            'qty': '1'
        }
        payloadEncoded = urlencode(payload, quote_via=quote_plus)


        try:
            postCart = self.session.post(self.atcUrl, data=payloadEncoded, headers={
                'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'referer': self.task["PRODUCT"],
                'content-type': 'application/x-www-form-urlencoded',
                'cookie':'frontend={}; frontend_cid={};'.format(self.frontend,self.frontend_cid)
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()

        self.frontend = postCart.headers['set-cookie'].split('frontend=')[1].split(';')[0]
        self.frontend_cid = postCart.headers['set-cookie'].split('frontend_cid=')[1].split(';')[0]

        try:
            soup = BeautifulSoup(postCart.text,"html.parser")
            qty = soup.find('span',{'class':'count'}).text
        except:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

        if postCart.status_code in [200,302] and int(qty) > 0:
            updateConsoleTitle(True,False,SITE)
            logger.success(SITE,self.taskID,'Successfully carted')
            self.login()
        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            if self.task["SIZE"].lower() == "random":
                self.collect()
            else:
                time.sleep(int(self.task["DELAY"]))
                self.addToCart()


    def login(self):
        logger.prepare(SITE,self.taskID,'Preparing login...')

        try:
            getOnepage = self.session.get('https://www.cornerstreet.fr/checkout/onepage/',headers={
                'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-language': 'en-US,en;q=0.9',
                'referer': 'https://www.cornerstreet.fr/checkout/cart/',
                'Cookie':'frontend={}; frontend_cid={}; _mcnc=1;'.format(self.frontend,self.frontend_cid)
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.login()

        self.frontend = getOnepage.headers['set-cookie'].split('frontend=')[1].split(';')[0]
        self.frontend_cid = getOnepage.headers['set-cookie'].split('frontend_cid=')[1].split(';')[0]


        payload = "form_key={}&login[username]={}&login[password]={}&context={}".format(self.formKey,self.task["ACCOUNT EMAIL"],self.task["ACCOUNT PASSWORD"],'checkout')
        try:
            postLogin = self.session.post('https://www.cornerstreet.fr/customer/account/loginPost/', data=payload, headers={
                'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-language': 'en-US,en;q=0.9',
                'referer': 'https://www.cornerstreet.fr/checkout/onepage/',
                'content-type': 'application/x-www-form-urlencoded',
                'cookie':'frontend={}; frontend_cid={}; _mcnc=1;'.format(self.frontend,self.frontend_cid)
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.login()

        self.frontend = postLogin.headers['set-cookie'].split('frontend=')[1].split(';')[0]
        self.frontend_cid = postLogin.headers['set-cookie'].split('frontend_cid=')[1].split(';')[0]
        
        
        if postLogin.status_code == 200 and 'index' in postLogin.url:
            logger.success(SITE,self.taskID,'Successfully logged in')
            self.billing()
        else:
            logger.error(SITE,self.taskID,'Failed to login. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.login()
    

    def billing(self):
        logger.prepare(SITE,self.taskID,'Submitting address...')
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        try:
            getOnepage = self.session.get('https://www.cornerstreet.fr/checkout/onepage',headers={
                'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-language': 'en-US,en;q=0.9',
                'referer': 'https://www.cornerstreet.fr/checkout/onepage/',
                'Cookie':'frontend={}; frontend_cid={}; _mcnc=1;'.format(self.frontend,self.frontend_cid)
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.billing()



        print(self.session.cookies)
        self.frontend = getOnepage.headers['set-cookie'].split('frontend=')[1].split(';')[0]
        self.frontend_cid = getOnepage.headers['set-cookie'].split('frontend_cid=')[1].split(';')[0]
        self.visitor_id = getOnepage.headers['set-cookie'].split('spm_visitor_id=')[1].split(';')[0]
        self.tawk_uuid = getOnepage.headers['set-cookie'].split('__tawkuuid=')[1].split(';')[0]

        print(getOnepage,getOnepage.url)

        if getOnepage.status_code == 200 and 'onepage' in getOnepage.url:
            try:
                soup = BeautifulSoup(getOnepage.text,"html.parser")
                self.addressId = soup.find('input',{'name':'billing[address_id]'})['value']
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to scrape page. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.billing()
            
            payload = {
                'billing[address_id]': self.addressId,
                'billing[prefix]': 'Mr',
                'billing[firstname]': profile['firstName'],
                'billing[lastname]': profile['lastName'],
                'billing[company]': '',
                'billing[street][]': profile['house'] + ' ' + profile['addressOne'],
                #'billing[street][]': profile['addressTwo'],
                'billing[city]': profile['city'],
                'billing[region_id]': '',
                'billing[region]': profile['region'],
                'billing[postcode]': profile['zip'],
                'billing[country_id]': profile['countryCode'],
                'billing[telephone]': profile['phone'],
                'billing[fax]': '',
                'billing[save_in_address_book]': 1,
                'billing[use_for_shipping]': 1,
                'form_key': self.formKey
            }
            payloadEncoded = urlencode(payload, quote_via=quote_plus)
            #e::cornerstreet.fr::SSIekepEYHjQB+GkHevkaeMt8qBHfun14pt2/+RnD91LyMqTpZ5C0ejGMCk0R+Y2::2	



            try:
                postBilling = self.session.post('https://www.cornerstreet.fr/checkout/onepage/saveBilling/',data=payloadEncoded,headers={
                    'authority': 'www.cornerstreet.fr',
                    'accept': 'text/javascript, text/html, application/xml, text/xml, */*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'cookie': 'frontend={}; frontend_cid={}; _mcnc=1; __tawkuuid={}'.format(self.frontend,self.frontend_cid, self.visitor_id, self.tawk_uuid),
                    'origin': 'https://www.cornerstreet.fr',
                    'referer': 'https://www.cornerstreet.fr/checkout/onepage/',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
                    'x-prototype-version':'1.7',
                    'x-requested-with': 'XMLHttpRequest'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.billing()


            print(postBilling.text)

            self.frontend = postBilling.headers['set-cookie'].split('frontend=')[1].split(';')[0]
            self.frontend_cid = postBilling.headers['set-cookie'].split('frontend_cid=')[1].split(';')[0]





  