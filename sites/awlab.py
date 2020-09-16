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
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, birthday, injection,storeCookies)
SITE = 'AW-LAB'


class AWLAB:
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
        
        self.dwRegion = loadProfile(self.task["PROFILE"])["countryCode"].upper()
        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
        self.awlabRegion = self.task["PRODUCT"].split('https://')[1].split('/')[0]

        self.collect()

    def collect(self):
        logger.warning(SITE,self.taskID,'Solving Cloudflare...')
        try:
            retrieve = self.session.get(self.task["PRODUCT"], headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'

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
                self.productTitle = soup.find('h1',{'class':['b-pdp__product-title','h-hidden-small']}).text.replace('\n','')
                self.productPrice = soup.find('span',{'class':'b-price__sale'}).text
                self.productImage = soup.find('link',{'rel':'image_src'})["href"]
                self.productId = soup.find('div',{'id':'pdpMain'})["data-product-id"]

                try:
                    retrieveSizes = self.session.get(f'https://{self.awlabRegion}/on/demandware.store/Sites-awlab-en-Site/en_{self.dwRegion}/Product-Variation?pid={self.productId}&format=ajax', headers={
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        
                    })
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                    log.info(e)
                    logger.error(SITE,self.taskID,'Error: {}'.format(e))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    time.sleep(int(self.task["DELAY"]))
                    self.collect()

                soup = BeautifulSoup(retrieveSizes.text, "html.parser")
                foundSizes = soup.find('ul',{'class':'swatches b-size-selector__list b-size-selector_large'})
                allSizes = []
                sizes = []
                
                for s in foundSizes:
                    try:
                        s = s.find('a')

                        sizes.append(s["title"])
                        allSizes.append('{}:{}'.format(s["title"], s["data-variant-id"]))
                    except:
                        pass
                
                if len(sizes) == 0:
                    logger.error(SITE,self.taskID,'Size Not Found')
                    time.sleep(int(self.task["DELAY"]))
                    self.collect()
    
                if self.task["SIZE"].lower() == "random":
                    chosen = random.choice(allSizes)
                    self.pid = chosen.split(':')[1]
                    self.size = chosen.split(':')[0]
                    logger.success(SITE,self.taskID,f'Found Size => {self.size}')
                
        
                else:
                    if self.task["SIZE"] not in sizes:
                        logger.error(SITE,self.taskID,'Size Not Found')
                        time.sleep(int(self.task["DELAY"]))
                        self.collect()
                    for size in allSizes:
                        if self.task["SIZE"] == size.split(':')[0]:
                            self.pid = size.split(':')[1]
                            self.size = size.split(':')[0]
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
        payload = {
            'Quantity': 1,
            'sizeTable': '',
            'cartAction': 'add',
            'pid': self.pid
        }

        try:
            postCart = self.session.post(f'https://{self.awlabRegion}/on/demandware.store/Sites-awlab-en-Site/en_{self.dwRegion}/Cart-AddProduct?format=ajax', data=payload, headers={
                'accept-language': 'en-US,en;q=0.9',
                'origin': f'https://{self.awlabRegion}',
                'referer': self.task["PRODUCT"],
                'accept':'text/html, */*; q=0.01',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()

        try:
            submitCart = self.session.post(f'https://{self.awlabRegion}/on/demandware.store/Sites-awlab-en-Site/en_{self.dwRegion}/Cart-SubmitForm?format=ajax', data={'dwfrm_cart_checkoutCart': 'true'}, headers={
                'accept-language': 'en-US,en;q=0.9',
                'origin': f'https://{self.awlabRegion}',
                'referer': self.task["PRODUCT"],
                'accept':'text/html, */*; q=0.01',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()

        if postCart.status_code == 200 and submitCart.status_code == 200 and submitCart.json()["success"] == True:
            logger.success(SITE,self.taskID,'Successfully carted')
            self.method()
        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            if self.task["SIZE"].lower() == "random":
                self.collect()
            else:    
                time.sleep(int(self.task["DELAY"]))
                self.addToCart()

    def method(self):
        try:
            checkout = self.session.get(f'https://{self.awlabRegion}/checkout',headers={
                'accept-language': 'en-US,en;q=0.9',
                'origin': f'https://{self.awlabRegion}',
                'referer': self.task["PRODUCT"],
                'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()

 
        if checkout.status_code == 200:
            soup = BeautifulSoup(checkout.text,"html.parser")
            self.csrf = soup.find('input',{'name':'csrf_token'})['value']

            self.shipping()
        
        else:
            logger.error(SITE,self.taskID,'Failed to get checkout page. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.method()

    def shipping(self):
        profile = loadProfile(self.task["PROFILE"])
        bday = birthday()

        try:
            states = self.session.post(f'https://{self.awlabRegion}/on/demandware.store/Sites-awlab-en-Site/en_{self.dwRegion}/Address-UpdateAddressFormStates?format=ajax', data={'selectedCountryCode': self.dwRegion, 'formId': 'singleshipping.shippingAddress.addressFields.states.state'}, headers={
                'accept-language': 'en-US,en;q=0.9',
                'origin': f'https://{self.awlabRegion}',
                'referer':f'https://{self.awlabRegion}/shipping',
                'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.method()

        
        if states.status_code == 200:
            soup = BeautifulSoup(states.text,"html.parser")
            states = soup.find("select",{"id":"dwfrm_singleshipping_shippingAddress_addressFields_states_state"})
            for s in states:
                try:

                    if profile["region"].lower() in s.text.lower():
                        self.stateID = s["value"]
                except:
                    pass
        if states.status_code == 410:
            logger.error(SITE,self.taskID,'States not found.')
            self.shipping()
            
        try:
            payload = {
                'dwfrm_billing_billingAddress_email_emailAddress': profile["email"],
                'dwfrm_singleshipping_shippingAddress_addressFields_phonecountrycode_codes': profile["phonePrefix"],
                'dwfrm_singleshipping_shippingAddress_addressFields_phonewithoutcode': profile["phone"],
                'dwfrm_singleshipping_shippingAddress_addressFields_phone': '{}{}'.format(profile["phonePrefix"], profile["phone"]),
                'dwfrm_singleshipping_shippingAddress_addressFields_isValidated': 'false',
                'dwfrm_singleshipping_shippingAddress_addressFields_firstName': profile["firstName"],
                'dwfrm_singleshipping_shippingAddress_addressFields_lastName': profile["lastName"],
                'dwfrm_singleshipping_shippingAddress_addressFields_title': 'Mr',
                'dwfrm_singleshipping_shippingAddress_addressFields_birthdayfields_day': bday["day"],
                'dwfrm_singleshipping_shippingAddress_addressFields_birthdayfields_month': bday["month"],
                'dwfrm_singleshipping_shippingAddress_addressFields_birthdayfields_year': bday["year"],
                'dwfrm_singleshipping_shippingAddress_addressFields_birthday': '{}-{}-{}'.format(bday["year"],bday["month"],bday["day"]),
                'dwfrm_singleshipping_shippingAddress_addressFields_address1': '{} {}, {}'.format(profile["house"], profile["addressOne"], profile["addressTwo"]),
                'dwfrm_singleshipping_shippingAddress_addressFields_postal': profile["zip"],
                'dwfrm_singleshipping_shippingAddress_addressFields_city': profile["city"],
                'dwfrm_singleshipping_shippingAddress_addressFields_states_state': self.stateID,
                'dwfrm_singleshipping_shippingAddress_addressFields_country': profile["countryCode"],
                'dwfrm_singleshipping_shippingAddress_useAsBillingAddress': 'true',
                'dwfrm_singleshipping_shippingAddress_shippingMethodID': 'ANY_STD',
                'dwfrm_singleshipping_shippingAddress_save': 'Proceed to Checkout',
                'csrf_token': self.csrf
            }
        except:
            logger.error(SITE,self.taskID,'Failed to submit shipping. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.shipping()
    
        try:
            shipping = self.session.post(f'https://{self.awlabRegion}/on/demandware.store/Sites-awlab-en-Site/en_{self.dwRegion}/COShipping-SingleShipping', data=payload, headers={
                'accept-language': 'en-US,en;q=0.9',
                'origin': f'https://{self.awlabRegion}',
                'referer':f'https://{self.awlabRegion}/shipping',
                'content-type': 'application/x-www-form-urlencoded',
                'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.method()

        if shipping.status_code == 200:
            logger.success(SITE,self.taskID,'Successfully submitted shipping')
            self.paypal()
        else:
            logger.error(SITE,self.taskID,'Failed to submit shipping. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.shipping()

    
    def paypal(self):
        logger.info(SITE,self.taskID,'Starting [PAYPAL] checkout...')
        profile = loadProfile(self.task["PROFILE"])
        payload = {
            'dwfrm_billing_save': 'true',
            'dwfrm_billing_billingAddress_addressId': 'guest-shipping',
            'dwfrm_billing_billingAddress_addressFields_isValidated': '',
            'dwfrm_billing_billingAddress_addressFields_firstName': profile["firstName"],
            'dwfrm_billing_billingAddress_addressFields_lastName': profile["lastName"],
            'dwfrm_billing_billingAddress_addressFields_address1': '{} {}, {}'.format(profile["house"], profile["addressOne"], profile["addressTwo"]),
            'dwfrm_billing_billingAddress_addressFields_postal': profile["zip"],
            'dwfrm_billing_billingAddress_addressFields_city': profile["city"],
            'dwfrm_billing_billingAddress_addressFields_states_state': self.stateID,
            'dwfrm_billing_billingAddress_addressFields_country': profile["countryCode"],
            'dwfrm_billing_couponCode': '',
            'dwfrm_billing_paymentMethods_creditCard_encrypteddata': '',
            'dwfrm_billing_paymentMethods_creditCard_type': '',
            'dwfrm_adyPaydata_brandCode': '',
            'noPaymentNeeded': 'true',
            'dwfrm_billing_paymentMethods_creditCard_selectedCardID': '',
            'dwfrm_billing_paymentMethods_selectedPaymentMethodID': 'PayPal',
            'dwfrm_billing_billingAddress_personalData': 'true',
            'dwfrm_billing_billingAddress_tersmsOfSale': 'true',
            'csrf_token': self.csrf
        }

        try:
            payment = self.session.post(f'https://{self.awlabRegion}/on/demandware.store/Sites-awlab-en-Site/en_{self.dwRegion}/COBilling-Billing', data=payload, headers={
                'accept-language': 'en-US,en;q=0.9',
                'origin': f'https://{self.awlabRegion}',
                'referer':f'https://{self.awlabRegion}/billing',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'x-requested-with': 'XMLHttpRequest',
                'accept':'*/*',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.method()

        if payment.status_code == 200:
            self.end = time.time() - self.start
            try:
                data = payment.json()
            except:
                logger.error(SITE,self.taskID,'Failed to get token. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.paypal()

            logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')
            ppURL = 'https://www.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token={}&useraction=commit'.format(data["token"])

            url = storeCookies(ppURL,self.session)
            
            sendNotification(SITE,self.productTitle)
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
        
        else:
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
            logger.error(SITE,self.taskID,'Failed to get PayPal checkout link. Retrying...')
            self.paypal()