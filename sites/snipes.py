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
        self.snipesRegion = self.task["PRODUCT"].split('snipes.')[1].split('/')[0]


        self.collect()
    
    def collect(self):
        logger.prepare(SITE,self.taskID,'Getting product page...')
        cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}')
        while cookies["px3"] == "error":
            cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}')

        # self.cookies = {
            # "px3":"a418523820048d71e8302f43532b092440ebb8da092c5b7e3c3aca25c9409375:IAgTwFwnrFqUsO4LBulH1EwOH77aETwSBV7TDHxaGABxTDj7N7B/3lbJ+06ALmyvcghaf6rBaQFTOkxjay4XbQ==:1000:EaXwrXDpXnAMxpwNrjh1Ggxb/eh/hUJNnLx2oAaPcc3GkgGitw1ofQ7ZjytYvLBkJgqNpG8XT7HTFwcxKXhLySRrdwd9hQiIjXW5emt832KafQY0jpzlailyoBOHifUemJZyn2u4PcbCoXf/PQUn98BzmjxZrGn3NmN7RZvlcNE=",
            # "vid":"1c1cd10-1714-11eb-a6c4-0242ac120009"
        # }
        cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
        cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
        self.session.cookies.set_cookie(cookie_obj)
        self.session.cookies.set_cookie(cookie_obj2)
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'referer': f'https://www.snipes.{self.snipesRegion}/',
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
            logger.success(SITE,self.taskID,'Got size info => {}'.format(self.sizePID))
            self.addToCart()
        else:
            logger.error(SITE,self.taskID,'Failed to retrieve size info. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.query()
    

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
            'referer': self.task["PRODUCT"],
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        payload = {
            "pid": self.sizePID,
            "options": [],
            "quantity": 1 
        }

        try:
            cart = self.session.post(f'https://www.snipes.{self.snipesRegion}/add-product?format=ajax',data=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()


        try:
            data = cart.json()
        except Exception as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()
        
        if cart.status_code == 200 and data['error'] == False:
            try:
                self.productTitle = data['cart']['items'][0]['productName']
                self.productPrice = data['cart']['items'][0]['price']['sales']['formatted']
                self.productImage = data['cart']['items'][0]['images'][0]['pdp']['srcT']
                self.uuid = data['cart']['items'][0]['UUID']
                self.shipmentUUID = data['cart']['items'][0]['shipmentUUID']
                self.demandWareBase = data['cart']['actionUrls']['submitCouponCodeUrl'].split('/Cart-AddCoupon')[0]
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.addToCart()

            updateConsoleTitle(True,False,SITE)
            logger.success(SITE,self.taskID,'Successfully Carted')
            if self.task["ACCOUNT EMAIL"] != "" and self.task["ACCOUNT EMAIL"] != "":
                self.login()
            else:
                self.shipping()
        
        if cart.status_code == 403:
            cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}')
            while cookies["px3"] == "error":
                cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}')

            cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
            cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
            self.session.cookies.set_cookie(cookie_obj)
            self.session.cookies.set_cookie(cookie_obj2)
            logger.error(SITE,self.taskID,'Forbidden. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()
        
        elif cart.status_code not in [200,403]:
            logger.error(SITE,self.taskID,'Failed to cart [{}]. Retrying...'.format(cart.status_code))
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()
    

    def login(self):
        logger.prepare(SITE,self.taskID,'Logging in...')
        payload = {
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
            'referer': 'https://www.snipes.{}{}/Checkout-Login'.format(self.snipesRegion,self.demandWareBase),
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        try:
            login = self.session.post('https://www.snipes.{}/authentication?rurl=2&format=ajax'.format(self.snipesRegion),data=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.login()

        try:
            response = login.json()
            status = response['success'] 
        except Exception as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Failed to login. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.login()

        

        if login.status_code == 200 and response:
            logger.success(SITE,self.taskID,'Successfully Logged in.')
            
            if self.task["COUPON"] != "":
                self.applyDiscount()
            else:
                self.shipping()
    
        if login.status_code == 403:
            cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}')
            while cookies["px3"] == "error":
                cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}')
            cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
            cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
            self.session.cookies.set_cookie(cookie_obj)
            self.session.cookies.set_cookie(cookie_obj2)
            logger.error(SITE,self.taskID,'Forbidden. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.login()

        elif login.status_code not in [200,403]:
            logger.error(SITE,self.taskID,'Failed to cart [{}]. Retrying...'.format(login.status_code))
            time.sleep(int(self.task["DELAY"]))
            self.login()

    
    def applyDiscount(self):
        logger.prepare(SITE,self.taskID,'Applying Coupon...')
        params = {
            'format': "ajax",
            'couponCode': self.task["COUPON"],
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
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        try:
            discount = self.session.get('https://www.snipes.{}{}/Cart-AddCoupon'.format(self.snipesRegion,self.demandWareBase),params=params)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.applyDiscount()

        if discount.status_code in [200,302] and 'AjaxFail' not in discount.url:
            logger.success(SITE,self.taskID,'Successfully applied coupon.')
            self.shipping()
    
        if discount.status_code == 403:
            cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}')
            while cookies["px3"] == "error":
                cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}')
            cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
            cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
            self.session.cookies.set_cookie(cookie_obj)
            self.session.cookies.set_cookie(cookie_obj2)
            logger.error(SITE,self.taskID,'Forbidden. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.login()

        elif discount.status_code not in [403,302]:
            logger.error(SITE,self.taskID,'Failed to apply coupon. Skipping')
            self.shipping()
        


    def shipping(self):
        logger.prepare(SITE,self.taskID,'Submitting shipping...')
        profile = loadProfile(self.task["PROFILE"])
        payload = {
            'originalShipmentUUID': self.shipmentUUID,
            'shipmentUUID': self.shipmentUUID,
            'dwfrm_shipping_shippingAddress_shippingMethodID': 'home-delivery',
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
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        try:
            submitShipping = self.session.post('https://www.snipes.{}{}/CheckoutShippingServices-SubmitShipping?format=ajax'.format(self.snipesRegion,self.demandWareBase),data=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.shipping()
        if submitShipping.status_code == 200:
            logger.success(SITE,self.taskID,'Shipping submitted successfully')
            self.payment_method()
        if shipping.status_code == 403:
            cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}')
            while cookies["px3"] == "error":
                cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}')
            cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
            cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
            self.session.cookies.set_cookie(cookie_obj)
            self.session.cookies.set_cookie(cookie_obj2)
            logger.error(SITE,self.taskID,'Forbidden. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.shipping()
        elif shipping.status_code not in [200,403]:
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
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        try:
            submitPayment= self.session.post('https://www.snipes.{}{}/CheckoutServices-SubmitPayment?format=ajax'.format(self.snipesRegion,self.demandWareBase),data=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.payment_method()

        if submitPayment.status_code == 200:
            logger.success(SITE,self.taskID,'Successfully set payment method')
            if self.task["PAYMENT"].lower() == "paypal":
                self.placeOrder_pp()
            if self.task["PAYMENT"].lower() == "bt":
                self.placeOrder_bt()
            if self.task["PAYMENT"].lower() == "card":
                self.placeOrder_card()

        if submitPayment.status_code == 403:
            cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}')
            while cookies["px3"] == "error":
                cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}')
            cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
            cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
            self.session.cookies.set_cookie(cookie_obj)
            self.session.cookies.set_cookie(cookie_obj2)
            logger.error(SITE,self.taskID,'Forbidden. Retrying...')
            time.sleep(int(self.task["DELAY"]))
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
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        try:
            place = self.session.post('https://www.snipes.{}{}/CheckoutServices-PlaceOrder?format=ajax'.format(self.snipesRegion,self.demandWareBase))
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.placeOrder_bt()


        try:
            response = place.json()
        except Exception as e:
            logger.error(SITE,self.taskID,'Failed to place order. Retrying...')
            log.info(e)
            time.sleep(int(self.task["DELAY"]))
            self.placeOrder_bt()


        if place.status_code in [200,302]:
            self.end = time.time() - self.start
            updateConsoleTitle(False,True,SITE)
            logger.alert(SITE,self.taskID,'Order confirmed ({}). Check your email to complete bank transfer.'.format(response["orderID"]))


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
                    speed=self.end
                )
                while True:
                    pass
            except Exception as e:
                logger.secondary(SITE,self.taskID,'Failed to send webhook. Checkout here ==> {}'.format(url))

        if place.status_code == 403:
            cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}')
            while cookies["px3"] == "error":
                cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}')
            cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
            cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
            self.session.cookies.set_cookie(cookie_obj)
            self.session.cookies.set_cookie(cookie_obj2)
            logger.error(SITE,self.taskID,'Forbidden. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.placeOrder_bt()

        elif place.status_code not in [200,403]:
            if response["errorMessage"]:
                msg = response["errorMessage"]
            else:
                msg = 'n/a'
            logger.error(SITE,self.taskID,f'Failed to place order [{msg}]. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.placeOrder_bt()

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
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        try:
            place = self.session.post('https://www.snipes.{}{}/CheckoutServices-PlaceOrder?format=ajax'.format(self.snipesRegion,self.demandWareBase))
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.placeOrder_card()


        try:
            response = place.json()
        except Exception as e:
            logger.error(SITE,self.taskID,'Failed to place order. Retrying...')
            log.info(e)
            time.sleep(int(self.task["DELAY"]))
            self.placeOrder_card()


        if place.status_code in [200,302] and 'saferpay' in response['continueUrl']:
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
            url = storeCookies( response['continueUrl'],self.session)


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
                    speed=self.end
                )
                while True:
                    pass
            except Exception as e:
                logger.secondary(SITE,self.taskID,'Failed to send webhook. Checkout here ==> {}'.format(url))

        if place.status_code == 403:
            cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}')
            while cookies["px3"] == "error":
                cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}')
            cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
            cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
            self.session.cookies.set_cookie(cookie_obj)
            self.session.cookies.set_cookie(cookie_obj2)
            logger.error(SITE,self.taskID,'Forbidden. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.placeOrder_card()

        elif place.status_code not in [200,403] and 'saferpay' not in response['continueUrl']:
            if response["errorMessage"]:
                msg = response["errorMessage"]
            else:
                msg = 'n/a'
            logger.error(SITE,self.taskID,f'Failed to place order [{msg}]. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.placeOrder_card()

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
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        try:
            place = self.session.post('https://www.snipes.{}{}/CheckoutServices-PlaceOrder?format=ajax'.format(self.snipesRegion,self.demandWareBase))
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.placeOrder_pp()



        try:
            response = place.json()
            cUrl = response["continueUrl"]
        except Exception as e:
            logger.error(SITE,self.taskID,'Failed to place order (Cart may have duplicates). Retrying...')
            log.info(e)
            time.sleep(int(self.task["DELAY"]))
            self.placeOrder_pp()


        if place.status_code in [200,302] and "paypal" in cUrl:
            self.end = time.time() - self.start
            updateConsoleTitle(False,True,SITE)
            logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')

            url = storeCookies(response["continueUrl"],self.session)

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
            except Exception as e:
                logger.secondary(SITE,self.taskID,'Failed to send webhook. Checkout here ==> {}'.format(url))

        if place.status_code == 403:
            cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}')
            while cookies["px3"] == "error":
                cookies = PX.snipes(self.session, f'https://www.snipes.{self.snipesRegion}')
            cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
            cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
            self.session.cookies.set_cookie(cookie_obj)
            self.session.cookies.set_cookie(cookie_obj2)
            logger.error(SITE,self.taskID,'Forbidden. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.placeOrder_pp()

        elif place.status_code not in [200,403] and "paypal" not in cUrl:
            if response["errorMessage"]:
                msg = response["errorMessage"]
            else:
                msg = 'n/a'
            logger.error(SITE,self.taskID,f'Failed to place order [{msg}]. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.placeOrder_pp()
        



