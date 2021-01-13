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
import string
from urllib3.exceptions import HTTPError
import csv
SITE = 'QUEENS'

from utils.logger import logger
from utils.webhook import discord
from utils.log import log
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification,storeCookies, updateConsoleTitle)


def findProduct(text, kws, SITE, taskID, region):
    logger.prepare(SITE,taskID,'Searching for product...')
    soup = BeautifulSoup(text, "html.parser")
    items = soup.find("div",{"id":"categoryItems"})
    
    kws = [x.lower() for x in kws]
    foundItem = []
    for i in items:
        if "visible-xs-block" in i["class"] or "clearfix" in i["class"]:
            pass
        else:
            aTag = i.find('a')
            if all(kw in aTag.text.lower() for kw in kws):
                aLink = aTag["href"]
                foundItem.append('https://www.queens.{}{}|{}'.format(region,aLink, aTag.text))
    
    if len(foundItem) > 0:
        logger.warning(SITE,taskID,'Successfully found product => {}'.format(foundItem[0].split('|')[1]))
        return foundItem[0].split('|')[0]
    else:
        return None




class QUEENS:
    def task_checker(self):
        originalTask = self.task
        while True:
            with open('./{}/tasks.csv'.format(SITE.lower()),'r') as csvFile:
                csv_reader = csv.DictReader(csvFile)
                row = [row for idx, row in enumerate(csv_reader) if idx in (self.rowNumber,self.rowNumber)]
                self.task = row[0]
                try:
                    self.task['ACCOUNT EMAIL'] = originalTask['ACCOUNT EMAIL']
                    self.task['ACCOUNT PASSWORD'] = originalTask['ACCOUNT PASSWORD']
                except:
                    pass
                self.task['PROXIES'] = 'proxies'
                csvFile.close()
            time.sleep(2)
            
    def __init__(self,task,taskName,rowNumber):
        self.task = task
        self.session = requests.session()
        self.taskID = taskName
        self.rowNumber = rowNumber

        self.region = self.task["PRODUCT"].split('queens.')[1].split('/')[0]

        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }

        threading.Thread(target=self.task_checker,daemon=True).start()
        self.collect()

    def collect(self):
        logger.prepare(SITE,self.taskID,'Getting product page...')
        if 'https' in self.task["PRODUCT"]:
            link = self.task["PRODUCT"]
            mode = 'link'
        else:
            if '|' in self.task["PRODUCT"]:
                mode = 'kws'
                kws = self.task["PRODUCT"].split('|')
                link = f'https://www.queens.{self.region}/new-arrivals/#n=100'
        try:
            retrieve = self.session.get(link)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.collect()
            

        if retrieve.status_code == 200 and retrieve.url != f'https://www.queens.{self.region}/':
            self.start = time.time()
            if mode == 'kws':
                logger.info(SITE,self.taskID, 'Searching for product')
                kwProduct = findProduct(retrieve.text, kws, SITE, self.taskID, self.region)
                while kwProduct == None:
                    time.sleep(int(self.task["DELAY"]))
                    kwProduct = findProduct(retrieve.text, kws, SITE, self.taskID, self.region)

                self.task["PRODUCT"] = kwProduct
            logger.warning(SITE,self.taskID,'Got product page')
            try:
                logger.prepare(SITE,self.taskID,'Getting product data...')
                soup = BeautifulSoup(retrieve.text,"html.parser")
                self.item_id = soup.find("i",{"class":"icon-star"})["data-id"]
                self.csrf = soup.find("input",{"name":"_csrf"})["value"]
                self.productImage = soup.find("a",{"class":"rsImg"})["href"]
                self.productTitle = soup.find("a",{"class":"rsImg"})["alt"]
                SizeSelect = soup.find("select",{"id":"variant"})
                all_sizes = []
                sizes = []
    
                if SizeSelect == None:
                    logger.error(SITE,self.taskID,'No sizes available. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.collect()
    
                try:
                    for s in SizeSelect:
                        size = s.text.split('(')[1]
                        size = size.replace(')','')
                        size = size.split('eur ')[1]
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
                    logger.warning(SITE,self.taskID,f'Found Size => {self.size}')
                
    
                else:
                    if self.task["SIZE"] not in sizes:
                        logger.error(SITE,self.taskID,'Size Not Found')
                        time.sleep(int(self.task["DELAY"]))
                        self.collect()
                    for size in all_sizes:
                        if self.task["SIZE"] == size.split(':')[0]:
                            self.size = size.split(':')[0]
                            logger.warning(SITE,self.taskID,f'Found Size => {self.size}')
                            self.sizeValue = size.split(':')[1]

            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to scrape page (Most likely out of stock). Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.collect()

            self.addToCart()

        if retrieve.url == f'https://www.queens.{self.region}/':
            logger.warning(SITE,self.taskID,'Product Page does not exist. Retrying...')
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
        logger.prepare(SITE,self.taskID,'Carting product...')
        payload = {
            '_csrf': self.csrf,
            'variant': self.sizeValue,
            'item_id': self.item_id,
            'quantity': 1
        }

        try:
            postCart = self.session.post(f'https://www.queens.{self.region}/ajax/addcart/',data=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()

        try:
            checkCart = self.session.get(f'https://www.queens.{self.region}/ajax/cartupdatestatus/')
            soup = BeautifulSoup(checkCart.text,"html.parser")
            cart = soup.find("span",{"class":"cart-notify"}).text
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()

        if postCart.status_code == 200 and checkCart.status_code == 200 and int(cart) > 0:
            updateConsoleTitle(True,False,SITE)
            logger.warning(SITE,self.taskID,'Successfully carted')
            self.country()
        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            if self.task["SIZE"] == "random":
                self.collect()
            else:
                self.addToCart()



    #def login(self):
    #    payload = {
    #        '_csrf': self.csrf,
    #        'email': self.task["ACCOUNT EMAIL"],
    #        'password': self.task["ACCOUNT PASSWORD"],
    #        'redirect_url': '/cart/'
    #    }
    #    try:
    #        log_in = self.session.post('https://www.queens.global/login/',data=payload)
    #    except ConnectionError:
    #        logger.login('',False,SITE,self.taskID)
    #        time.sleep(int(self.task["DELAY"]))
    #        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
    #        self.login()
    #        
    #    if log_in.status_code == 200:
    #        logger.login('',True,SITE,self.taskID)
    #        self.country()
    #    else:
    #        logger.login('',False,SITE,self.taskID)
    #        time.sleep(int(self.task["DELAY"]))
    #        self.login()


    def country(self):
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        countryCode = profile["countryCode"]
        logger.prepare(SITE,self.taskID,'Setting country...')

        try:
            getCountry = self.session.get(f'https://www.queens.{self.region}/checkout/country/')
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.country()

        if getCountry.status_code == 200:
            soup = BeautifulSoup(getCountry.text,"html.parser") 
            self.csrf = soup.find("input",{"name":"_csrf"})["value"]
            payload = {
                '_csrf': self.csrf,
                'state': countryCode,
                'state_id':'Different country...'
            }
            try:
                country = self.session.post(f'https://www.queens.{self.region}/checkout/country/',data=payload)
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.country()

            if country.status_code == 200:
                logger.warning(SITE,self.taskID,'Country Set')
                self.shipping()
            else:
                logger.error(SITE,self.taskID,'Failed to set Country. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.country()
        
        else:
            logger.error(SITE,self.taskID,'Failed to get country page. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.country()

    def shipping(self):
        logger.prepare(SITE,self.taskID,'Setting shipping...')
        try:
            shipping = self.session.get(f'https://www.queens.{self.region}/checkout/shipping/')
        except:
            logger.error(SITE,self.taskID,'Connection Error. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.shipping()

        if shipping.status_code == 200:
            soup = BeautifulSoup(shipping.text,"html.parser")
            self.shippingID = soup.find_all('input',{'name':'shipping'})[0]["value"]
        else:
            logger.error(SITE,self.taskID,'Faile to retrieve shipping ID')
            time.sleep(int(self.task["DELAY"]))
            self.shipping()

        payload = {
            '_csrf': self.csrf,
            'shipping': self.shippingID,
            'payment': 4
        }
        try:
            methods = self.session.post(f'https://www.queens.{self.region}/checkout/shipping/',data=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.shipping()

        if methods.status_code == 200:
            logger.warning(SITE,self.taskID,'Successfully set shipping')
            self.delivery()
        else:
            logger.error(SITE,self.taskID,'Failed to set shipping. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.shipping()


    def delivery(self):
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        logger.prepare(SITE,self.taskID,'Submitting delivery....')
        payload = {
            '_csrf': self.csrf,
            'CheckoutForm[first_name]': profile["firstName"],
            'CheckoutForm[surname]': profile["lastName"],
            'CheckoutForm[company_name]': '',
            'CheckoutForm[email]': profile["email"],
            'CheckoutForm[phone]': profile["phone"],
            'CheckoutForm[street]': profile["addressOne"],
            'CheckoutForm[street_number]': profile["house"],
            'CheckoutForm[city]': profile["city"],
            'CheckoutForm[zip]': profile["zip"],
            'CheckoutForm[note]': '',
            'CheckoutForm[accept_tc]': 1,
            'finish_order':''
        }
        try:
            finish = self.session.post(f'https://www.queens.{self.region}/checkout/delivery/',data=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.delivery()
            
        if finish.status_code == 200 and 'checkout/done' in finish.url:
            logger.warning(SITE,self.taskID,'Submitted delivery')
            split = finish.text.split('return actions.order.create(')[1].split(',application_context')[0].replace('purchase_units','"purchase_units"').replace('amount','"amount"').replace('custom_id','"custom_id"').replace("'",'"')
            checkoutDetails = json.loads(split + '}')
            orderNumber = checkoutDetails["purchase_units"][0]["custom_id"]
            self.orderCurrency = checkoutDetails["purchase_units"][0]["amount"]["currency_code"]
            self.orderTotal = checkoutDetails["purchase_units"][0]["amount"]["value"]
            self.productPrice = '{} {}'.format(self.orderTotal,self.orderCurrency)
            tracking = f'https://www.queens.{self.region}' + finish.text.split('Track your order <b><a href="')[1].split('">here</a></b>.')[0]


            logger.prepare(SITE,self.taskID,'Getting paypal link...')
            try:
                smartButton = self.session.get('https://www.paypal.com/smart/buttons/?clientID=AR-aWcHvERa9mDAl3Jwyo39Yc7-4uaiiLom6Rhc8vkfxMkXlx0pzA9aEdoD7WMzsh-E6ICBRR7veqdWd')
                self.facilitatorAccessToken = smartButton.text.split('"facilitatorAccessToken":"')[1].split('"')[0]
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = None
                self.delivery()

            self.session.headers["authorization"] = 'Bearer {}'.format(self.facilitatorAccessToken)
            try:
                paypalOrder = self.session.post('https://www.paypal.com/v2/checkout/orders',json={"purchase_units":[{"amount":{"currency_code":self.orderCurrency,"value":self.orderTotal},"custom_id":orderNumber}],"application_context":{"shipping_preference":"NO_SHIPPING"},"intent":"CAPTURE"})
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = None
                self.delivery()

            if paypalOrder.status_code == 201 and paypalOrder.json()["status"] == "CREATED":
                logger.warning(SITE,self.taskID,'Got paypal link')
                self.end = time.time() - self.start
                logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')
                updateConsoleTitle(False,True,SITE)

                url = storeCookies(paypalOrder.json()["links"][1]["href"],self.session, self.productTitle, self.productImage, self.productPrice)
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
                        tracking=tracking,
                        order=orderNumber,
                        product=self.task["PRODUCT"],
                        proxy=self.session.proxies,
                        speed=self.end
                    )
                    sendNotification(SITE,self.productTitle)
                    while True:
                        pass
                except:
                    logger.alert(SITE,self.taskID,'Failed to send webhook. Checkout here ==> {}'.format(url))
            
            elif paypalOrder.status_code != 201:
                logger.error(SITE,self.taskID,'Could not complete PayPal Checkout. Retrying...')
                try:
                    discord.failed(
                        webhook=loadSettings()["webhook"],
                        site=SITE,
                        url=self.task["PRODUCT"],
                        image=self.productImage,
                        title=self.productTitle,
                        size=self.size,
                        price=self.productPrice,
                        paymentMethod='PayPal',
                        profile=self.task["PROFILE"],
                        proxy=self.session.proxies
                    )
                except:
                    pass
                time.sleep(int(self.task["DELAY"]))
                self.delivery()

            
        elif 'checkout/done' not in finish.url:
            logger.error(SITE,self.taskID,'Failed to finalize checkout. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.delivery()


