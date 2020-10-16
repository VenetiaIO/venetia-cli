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
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies)
SITE = 'DISNEY'



class DISNEY:
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
        if "shopdisney" in self.task["PRODUCT"]:
            self.product = self.task["PRODUCT"]
        else:
            self.product = "https://www.shopdisney.co.uk/{}.html".format(self.task["PRODUCT"])
        logger.warning(SITE,self.taskID,'Solving Cloudflare...')
        try:
            retrieve = self.session.get(self.product, headers={
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
            })
            logger.success(SITE,self.taskID,'Solved Cloudflare')
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.collect()

        if retrieve.status_code == 200:
            self.start = time.time()
            logger.success(SITE,self.taskID,'Got product page')
            try:
                soup = BeautifulSoup(retrieve.text, "html.parser")
                self.productTitle = soup.find("title").text.strip(" ").strip("\n")
                self.productImage = soup.find("meta", {"property": "og:image"})["content"]
                self.csrf = soup.find("input",{"name":"csrf_token"})["value"]
                self.pid = soup.find("input",{"name":"pid"})["value"]
                self.cartURL = soup.find("form",{"class":"js-pdp-form"})["action"]

                self.siteBase = soup.find('a',{'class':'waymark__link no-transform bc1'})['href']
                self.demandwareBase = self.cartURL.split('Cart-AddProduct')[0]

                self.size = "One Size"

    
                logger.success(SITE,self.taskID,f'Found Size => {self.size}')

                        
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
        logger.prepare(SITE,self.taskID,'Adding to cart...')

        payload = {
            'format': 'ajax',
            'Quantity': 1,
            'pid': self.pid,
            'csrf_token': self.csrf
        }

        try:
            postCart = self.session.post(self.cartURL, data=payload, headers={
                'accept': '*/*',
                'referer': self.product,
                'x-requested-with': 'XMLHttpRequest',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()




        if postCart.status_code == 200:
            logger.success(SITE,self.taskID,'Successfully carted')
            self.initiate()
        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

    def initiate(self):
        logger.prepare(SITE,self.taskID,'Getting keys...')
        try:
            bag = self.session.get(self.siteBase + '/bag', headers={
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'referer': self.product,
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.initiate()

        
        if bag.status_code == 200:
            try:
                soup = BeautifulSoup(bag.text,"html.parser")
                self.bagUrl = soup.find('form',{'name':'dwfrm_cart'})['action']
                self.secureKey = self.bagUrl.split('?dwcont=')[1]
            except:
                logger.error(SITE,self.taskID,'Failed to get keys')
                time.sleep(int(self.task["DELAY"]))
                self.initiate()
        else:
            logger.error(SITE,self.taskID,'Failed to get shipping')
            time.sleep(int(self.task["DELAY"]))
            self.initiate()

        try:
            initiate = self.session.post(self.bagUrl,data={"dwfrm_cart_checkoutCart": "Checkout"} ,headers={
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'referer': self.siteBase + "/bag",
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.initiate()

        if initiate.status_code == 200:
            soup = BeautifulSoup(initiate.text,"html.parser")
            self.shippingKey = soup.find('input',{'name':'dwfrm_singleshipping_securekey'})['value']
    
            logger.success(SITE,self.taskID,'Successfully got keys')
            self.methods()
        else:
            logger.error(SITE,self.taskID,'Failed to get keys')
            time.sleep(int(self.task["DELAY"]))
            self.initiate()


    def methods(self):
        logger.prepare(SITE,self.taskID,'Getting shipping methods')
        profile = loadProfile(self.task["PROFILE"])

        try:
            shippingMethods = self.session.get(self.demandwareBase + "COShippingHook-UpdateShippingMethodList",params={
            'countryCode': profile["countryCode"],
            'postalCode': profile["zip"],
            'city': profile["city"],
            '_': int(time.time())
        },headers={
                'accept': '*/*',
                'referer': 'https://www.shopdisney.co.uk/bag',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.methods()

        if shippingMethods.status_code == 200:
            soup = BeautifulSoup(shippingMethods.text,"html.parser")
            methods = soup.find_all('input',{'name':'dwfrm_singleshipping_shippingAddress_shippingMethodList'})
            self.method = methods[0]["value"]
            logger.success(SITE,self.taskID,'Retrieved shipping method.')
            self.shipping()
        else:
            logger.error(SITE,self.taskID,'Failed to get shipping')
            time.sleep(int(self.task["DELAY"]))
            self.methods()


    def shipping(self):
        profile = loadProfile(self.task["PROFILE"])
        payload = {
            'dwfrm_singleshipping_securekey': self.shippingKey,
            'dwfrm_singleshipping_shippingAddress_addressFields_addressid': None,
            'dwfrm_singleshipping_shippingAddress_addressFields_firstName': profile["firstName"],
            'dwfrm_singleshipping_shippingAddress_addressFields_lastName': profile["lastName"],
            'dwfrm_singleshipping_shippingAddress_addressFields_phone': profile["phonePrefix"] + profile["phone"],
            'dwfrm_singleshipping_shippingAddress_addressFields_email': profile["email"],
            'dwfrm_singleshipping_shippingAddress_addressFields_country': profile["countryCode"],
            'dwfrm_singleshipping_shippingAddress_addressFields_houseNumber': profile["house"],
            'dwfrm_singleshipping_shippingAddress_addressFields_zip': profile["zip"],
            'dwfrm_singleshipping_shippingAddress_addressFields_address1': profile["addressOne"],
            'dwfrm_singleshipping_shippingAddress_addressFields_address2': profile["addressTwo"],
            'dwfrm_singleshipping_shippingAddress_addressFields_city': profile["city"],
            'accordionSectionCheckbox': 'on',
            'dwfrm_singleshipping_shippingAddress_shippingMethodList': self.method,
            'dwfrm_singleshipping_shippingAddress_addressFields_deliveryInstructions': '',
            'dwfrm_singleshipping_shippingAddress_save': 1,
        }
        try:
            postShipping = self.session.post(self.bagUrl,data=payload,headers={
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'referer': self.bagUrl,
                'authority': 'www.shopdisney.co.uk',
                'origin': 'https://www.shopdisney.co.uk',
                'content-type': 'application/x-www-form-urlencoded',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.shipping()



        soup = BeautifulSoup(postShipping.text,"html.parser")
        self.billingSecureKey = soup.find('input',{'name':'dwfrm_billing_securekey'})['value']
        self.paypal()
        

    def paypal(self):
        profile = loadProfile(self.task["PROFILE"])
        payload = {
            'dwfrm_billing_paymentMethods_selectedPaymentMethodID': 'WORLDPAY_PAYPAL',
            'dwfrm_billing_paymentMethods_creditCard_type': '',
            'dwfrm_billing_paymentMethods_creditCard_owner': '',
            'dwfrm_billing_paymentMethods_creditCard_number': '',
            'dwfrm_billing_paymentMethods_creditCard_month': '',
            'dwfrm_billing_paymentMethods_creditCard_yearshort': '',
            'dwfrm_billing_paymentMethods_creditCard_year': None,
            'dwfrm_billing_paymentMethods_creditCard_cvn': '',
            'dwfrm_billing_paymentMethods_creditCard_uuid': '',
            'paymentmethods': 'WORLDPAY_PAYPAL',
            'dwfrm_billing_threeDSReferenceId': '',
            'dwfrm_billing_useShippingAddress': 0,
            'dwfrm_billing_save': True,
            'dwfrm_billing_billingAddress_addressFields_firstName': profile["firstName"],
            'dwfrm_billing_billingAddress_addressFields_lastName': profile["lastName"],
            'dwfrm_billing_billingAddress_addressFields_country': profile["countryCode"],
            'dwfrm_billing_billingAddress_addressFields_houseNumber': profile["house"],
            'dwfrm_billing_billingAddress_addressFields_zip': profile["zip"],
            'dwfrm_billing_billingAddress_addressFields_address1': profile["addressOne"],
            'dwfrm_billing_billingAddress_addressFields_address2': profile["addressTwo"],
            'dwfrm_billing_billingAddress_addressFields_city': profile["city"],
            'dwfrm_billing_securekey': self.billingSecureKey
        }

        try:
            postFinal = self.session.post(self.demandwareBase + 'COShipping-Start/{}'.format(self.secureKey),data=payload,headers={
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'referer': self.demandwareBase + 'COShipping-Start/{}'.format(self.secureKey),
                'authority': 'www.shopdisney.co.uk',
                'origin': 'https://www.shopdisney.co.uk',
                'content-type': 'application/x-www-form-urlencoded',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.paypal()
        

        try:
            pp = self.session.post(self.demandwareBase + "COSummary-Submit",data={'submit-order': 'Submit Order'},headers={
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'referer': self.siteBase + '/bag?dwcont={}'.format(self.secureKey),
                'content-type': 'application/x-www-form-urlencoded',
                'authority': 'www.shopdisney.co.uk',
                'origin': 'https://www.shopdisney.co.uk',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.paypal()

        print(pp)
        print(pp.url)

