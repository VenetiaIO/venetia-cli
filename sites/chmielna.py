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
SITE = 'CHMIELNA20'



class CHMIELNA:
    def __init__(self, task,taskName):
        self.task = task
        self.sess = requests.session()
        self.taskID = taskName

        twoCap = loadSettings()["2Captcha"]
        try:
            self.session = scraper()
        except Exception as e:
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.__init__(task,taskName)

        

        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)

        self.collect()

    def collect(self):
        logger.prepare(SITE,self.taskID,'Getting product page...')
        try:
            retrieve = self.session.get(self.task["PRODUCT"])
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.collect()


        if retrieve.status_code == 200:
            self.start = time.time()
            if retrieve.text == "":
                logger.error(SITE,self.taskID,f'Failed to get product page. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.collect()


            logger.warning(SITE,self.taskID,'Got product page')
            try:
                logger.prepare(SITE,self.taskID,'Getting product data...')
                soup = BeautifulSoup(retrieve.text, "html.parser")
                self.cartURL = soup.find('form',{'name':'product__add'})["action"]
                self.token = soup.find('input',{'name':'_token'})["value"]
                img = soup.find('div',{'class':'item zoom'})
                self.productImage = img.find('img')["src"]
                self.productTitle = soup.find('title').text.split('|')[0]
                self.productPrice = soup.find('span',{'class':'product__price_shop'}).text
    
                foundSizes = soup.find('div',{'class':'selector'})
                foundSizes = foundSizes.find('ul')
                foundSizes = foundSizes.find_all('li')
                if foundSizes:

                    sizes = []
                    for s in foundSizes:
                        soup = BeautifulSoup(str(s),"html.parser")
                        sizes.append(soup.find('li')["data-sizeus"])
    
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
                                    logger.warning(SITE,self.taskID,f'Found Size => {self.size}')
        
                    
                    elif self.task["SIZE"].lower() == "random":
                        self.size = random.choice(sizes)
                        logger.warning(SITE,self.taskID,f'Found Size => {self.size}')
                
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
        logger.prepare(SITE,self.taskID,'Carting product...')
        payload = {
            '_token': self.token,
            'size': self.size
        }

        try:
            postCart = self.session.post(self.cartURL, data=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()

        if postCart.status_code in [200,302] and "basket" in postCart.url:
            updateConsoleTitle(True,False,SITE)
            logger.warning(SITE,self.taskID,'Successfully carted')
            self.method()
        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

    def method(self):
        logger.prepare(SITE,self.taskID,'Setting method...')
        try:
            method = self.session.get('https://chmielna20.pl/order/anonymous')
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.method()

        if method.status_code in [200,302] and 'order' in method.url:
            logger.warning(SITE,self.taskID,'Successfully set method.')
            self.address() 
        else:
            logger.error(SITE,self.taskID,'Failed to set method. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.method()

    def address(self):
        logger.prepare(SITE,self.taskID,'Submitting address...')

        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        payload = {
            '_token': self.token,
            'addressValue[firstname]': profile['firstName'],
            'addressValue[lastname]': profile['lastName'],
            'addressValue[address]': profile['house'] + ' ' + profile['addressOne'],
            'addressValue[business]': '',
            'addressValue[postcode]': profile['zip'],
            'addressValue[city]': profile['city'],
            'addressValue[Country_id]': profile['countryCode'].upper(),
            'addressValue[States_id]': '',
            'addressValue[phone]': profile["phonePrefix"] + " " + profile["phone"],
            'phone_country': profile['countryCode'].lower(),
            'addressValue[company]': '',
            'addressValue[NIP]': '',
            'email': profile['email'],
            'isRegistered': 0,
            'unregistered': 1,
            'invoiceValue_select': '',
            'invoiceValue[company]': '',
            'invoiceValue[NIP]': '',
            'invoiceValue[address]': profile['house'] + ' ' + profile['addressOne'],
            'invoiceValue[postcode]': profile['zip'],
            'invoiceValue[city]': profile['city'],
            'invoiceValue[Country_id]': profile['countryCode'].upper(),
            'agree': 1
        }

        try:
            postOrder = self.session.post('https://chmielna20.pl/en/order', data=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.address()

        if postOrder.status_code == 200 and "delivery" in postOrder.url:
            logger.warning(SITE,self.taskID,'Successfully set address.')
            self.delivery()
        else:
            logger.error(SITE,self.taskID,'Failed to set address. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.address()

    def delivery(self):
        logger.prepare(SITE,self.taskID,'Setting delivery option...')
        try:
            delivery = self.session.get('https://chmielna20.pl/en/order/delivery')
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.delivery()

        if delivery.status_code == 200:
            try:
                soup = BeautifulSoup(delivery.text,"html.parser")
                self.deliveryId = soup.find_all('input',{'name':'Delivery_form_id'})[0]['value']
                self.paymentId_pp = soup.find('input',{'data-name':'PayPal'})['value']
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to set delivery method. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.delivery()


            payload = {
                '_token': self.token,
                'Delivery_form_id': self.deliveryId,
                'Payment_id': self.paymentId_pp,
                'input_summary_city': '',
                'input_summary_post_code': '',
                'input_summary_street': '',
                'input_summary_province': '',
                'InPost_machineName': '',
                'InPost_machineAddress': '',
                'Payment_type_id': '',
                'parcelshop': '',
                'parcelshop_address': '',
                'pickpack_date': ''
            }
            
            try:
                postDelivery = self.session.post('https://chmielna20.pl/en/order/delivery', data=payload)
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.address()


            if postDelivery.status_code == 200 and "confirm" in postDelivery.url:
                logger.warning(SITE,self.taskID,'Successfully set delivery method.')
                self.confirm()
            else:
                logger.error(SITE,self.taskID,'Failed to set delivery method. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.delivery()
        else:
            logger.error(SITE,self.taskID,'Failed to set delivery method. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.delivery()

    def confirm(self):
        logger.prepare(SITE,self.taskID,'Submitting checkout...')
        try:
            conf = self.session.post('https://chmielna20.pl/en/order/confirm', data={"_token":self.token})
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.confirm()

        if conf.status_code == 200:
            try:
                soup = BeautifulSoup(conf.text,"html.parser")
                createUrl = soup.find('form',{"id":"form-order"})["action"]
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to get PayPal checkout link. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.confirm()


            try:
                payCreate = self.session.post(createUrl, data={"_token":self.token})
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.confirm()

            if payCreate.status_code in [200,302] and "paypal" in payCreate.url:
                logger.prepare(SITE,self.taskID,'Checkout submitted')
                self.end = time.time() - self.start
                logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')
                updateConsoleTitle(False,True,SITE)
                url = storeCookies(payCreate.url,self.session, self.productTitle, self.productImage, self.productPrice)               
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
                        speed=self.end
                    )
                    while True:
                        pass
                except:
                    logger.alert(SITE,self.taskID,'Failed to send webhook. Checkout here ==> {}'.format(url))
            else:
                logger.error(SITE,self.taskID,'Failed to get PayPal checkout link. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.confirm()
        else:
            logger.error(SITE,self.taskID,'Failed to get PayPal checkout link. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.confirm()


            


