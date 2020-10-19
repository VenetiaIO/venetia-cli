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
from utils.adyen import ClientSideEncrypter
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
            if self.task["PAYMENT"].lower() == "paypal":
                self.paypal()
            if self.task["PAYMENT"].lower() == "cad":
                self.cad()
            elif self.task["PAYMENT"].lower() == "card":
                self.card()
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
                    logger.secondary(SITE,self.taskID,'Failed to send webhook. Checkout here ==> {}'.format(url))
        
        else:
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
            logger.error(SITE,self.taskID,'Failed to get PayPal checkout link. Retrying...')
            self.paypal()


    def cad(self):
        logger.info(SITE,self.taskID,'Starting [CAD] checkout...')
        profile = loadProfile(self.task["PROFILE"])

    
        payload = {
            'dwfrm_billing_save': 'true',
            'dwfrm_billing_billingAddress_addressId': 'guest-shipping',
            'dwfrm_billing_billingAddress_addressFields_isValidated': 'true',
            'dwfrm_billing_billingAddress_addressFields_firstName': profile["firstName"],
            'dwfrm_billing_billingAddress_addressFields_lastName': profile["lastName"],
            'dwfrm_billing_billingAddress_addressFields_address1': '{} {}, {}'.format(profile["house"], profile["addressOne"], profile["addressTwo"]),
            'dwfrm_billing_billingAddress_addressFields_postal': profile["zip"],
            'dwfrm_billing_billingAddress_addressFields_city': profile["city"],
            'dwfrm_billing_billingAddress_addressFields_states_state': self.stateID,
            'dwfrm_billing_billingAddress_addressFields_country': profile["countryCode"],
            'dwfrm_billing_billingAddress_invoice_accountType': 'private',
            'dwfrm_billing_couponCode': '',
            'dwfrm_billing_paymentMethods_creditCard_encrypteddata': '',
            'dwfrm_billing_paymentMethods_creditCard_type': '',
            'dwfrm_adyPaydata_brandCode': '',
            'noPaymentNeeded': 'true',
            'dwfrm_billing_paymentMethods_creditCard_selectedCardID': '',
            'dwfrm_billing_paymentMethods_selectedPaymentMethodID': 'CASH_ON_DELIVERY',
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
            self.card()

        if payment.status_code in [200,302]:
            self.end = time.time() - self.start
            logger.alert(SITE,self.taskID,'Checkout complete!')
            
            try:
                discord.success(
                    webhook=loadSettings()["webhook"],
                    site=SITE,
                    image=self.productImage,
                    title=self.productTitle,
                    size=self.size,
                    price=self.productPrice,
                    paymentMethod="Card",
                    profile=self.task["PROFILE"],
                    product=self.task["PRODUCT"],
                    proxy=self.session.proxies,
                    speed=self.end
                )
                while True:
                    pass
            except:
                pass
        else:
            logger.error(SITE,self.taskID,'Checkout Failed. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.cad()


    
    def card(self):
        logger.info(SITE,self.taskID,'Starting [CARD] checkout...')
        profile = loadProfile(self.task["PROFILE"])
        number = profile["card"]["cardNumber"]
        if str(number[0]) == "3":
            cType = 'amex'
        if str(number[0]) == "4":
            cType = 'visa'
        if str(number[0]) == "5":
            cType = 'mastercard'


        encryptedInfo = ClientSideEncrypter("10001|A58F2F0D8A4A08232DD1903F00A3F99E99BB89D5DEDF7A9612A3C0DC9FA9D8BDB2A20A233B663B0A48D47A0A1DDF164B3206985EFF19686E3EF75ADECF77BA10013B349C9F95CEBB5A66C48E3AD564410DB77A5E0798923E849E48A6274A80CBE1ACAA886FF3F91C40C6F2038D90FABC9AEE395D4872E24183E8B2ACB28025964C5EAE8058CB06288CDA80D44F69A7DFD3392F5899886094DB23F703DAD458586338BF21CF84288C22020CD2AB539A35BF1D98582BE5F79184C84BE877DB30C3C2DE81E394012511BFE9749E35C3E40D28EE3338DE7CBB1EDD253951A7B66A85E9CC920CA2A40CAD48ACD8BD1AE681997D1655E59005F1887B872A7A873EDBD1", "_0_1_18")
        adyenEncrypted = str(encryptedInfo.generate_adyen_nonce(profile["firstName"] + " " + profile["lastName"], profile["card"]["cardNumber"], profile["card"]["cardCVV"], profile["card"]["cardMonth"],  profile["card"]["cardYear"]).replace("b'", "").replace("'", ""))
        payload = {
            'dwfrm_billing_save': 'true',
            'dwfrm_billing_billingAddress_addressId': 'guest-shipping',
            'dwfrm_billing_billingAddress_addressFields_isValidated': 'true',
            'dwfrm_billing_billingAddress_addressFields_firstName': profile["firstName"],
            'dwfrm_billing_billingAddress_addressFields_lastName': profile["lastName"],
            'dwfrm_billing_billingAddress_addressFields_address1': '{} {}, {}'.format(profile["house"], profile["addressOne"], profile["addressTwo"]),
            'dwfrm_billing_billingAddress_addressFields_postal': profile["zip"],
            'dwfrm_billing_billingAddress_addressFields_city': profile["city"],
            'dwfrm_billing_billingAddress_addressFields_states_state': self.stateID,
            'dwfrm_billing_billingAddress_addressFields_country': profile["countryCode"],
            'dwfrm_billing_couponCode': '',
            'dwfrm_billing_paymentMethods_creditCard_encrypteddata': adyenEncrypted,
            'dwfrm_billing_paymentMethods_creditCard_type': cType,
            'dwfrm_adyPaydata_brandCode': '',
            'noPaymentNeeded': 'true',
            'dwfrm_billing_paymentMethods_creditCard_selectedCardID': '',
            'dwfrm_billing_paymentMethods_selectedPaymentMethodID': 'CREDIT_CARD',
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
            self.card()

        if payment.status_code in [200,302] and "orderNo" in payment.url:
            logger.info(SITE,self.taskID,'Initiating 3DS checkout')
            soup = BeautifulSoup(payment.text, 'html.parser')
            self.termURL = soup.find('input',{'name':'TermUrl'})['value'] 
            self.PaReq = soup.find('input',{'name':'PaReq'})['value'] 
            self.MD = soup.find('input',{'name':'MD'})['value'] 

            Dpayload = {
               "TermUrl":self.termURL,
               "PaReq":self.PaReq,
               "MD":self.MD 
            }

            try:
                payerAuth = self.session.post('https://verifiedbyvisa.acs.touchtechpayments.com/v1/payerAuthentication', data=Dpayload, headers={
                    'referer':f'https://{self.awlabRegion}',
                    'content-type': 'application/x-www-form-urlencoded',
                    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.card()

            if payerAuth.status_code == 200:
                soup = BeautifulSoup(payerAuth.text,"html.parser")
                transToken = str(soup.find_all("script")[0]).split('"')[1]
                try:
                    payload = {"transToken":transToken}
                    poll = self.session.post('https://poll.touchtechpayments.com/poll', json=payload, headers={
                        'authority': 'verifiedbyvisa.acs.touchtechpayments.com',
                        'accept-language': 'en-US,en;q=0.9',
                        'referer': 'https://verifiedbyvisa.acs.touchtechpayments.com/v1/payerAuthentication',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                        'accept':'*/*',
                    })
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                    log.info(e)
                    logger.error(SITE,self.taskID,'Error: {}'.format(e))
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    self.card()

                if poll.json()["status"] == "blocked":
                    logger.error(SITE,self.taskID,'Card Blocked. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.card()
                if poll.json()["status"] == "pending":
                    logger.warning(SITE,self.taskID,'Polling 3DS...')
                    while poll.json()["status"] == "pending":
                        poll = self.session.post('https://poll.touchtechpayments.com/poll',headers={
                            'authority': 'verifiedbyvisa.acs.touchtechpayments.com',
                            'accept-language': 'en-US,en;q=0.9',
                            'referer': 'https://verifiedbyvisa.acs.touchtechpayments.com/v1/payerAuthentication',
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                            'accept':'*/*',}, json=payload)
                
                try:
                    json = poll.json()
                except:
                    logger.error(SITE,self.taskID,'Failed to retrieve auth token for 3DS. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.card()
                if poll.json()["status"] == "success":
                    authToken = poll.json()['authToken']
                else:
                    logger.error(SITE,self.taskID,'Failed to retrieve auth token for 3DS. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.card()

                authToken = poll.json()['authToken']
                logger.alert(SITE,self.taskID,'3DS Authorised')
        
                data = '{"transToken":"%s","authToken":"%s"}' % (transToken, authToken)

                headers = {
                    'authority': 'macs.touchtechpayments.com',
                    'sec-fetch-dest': 'empty',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                    'content-type': 'application/json',
                    'accept': '*/*',
                    'origin': 'https://verifiedbyvisa.acs.touchtechpayments.com',
                    'referer': 'https://verifiedbyvisa.acs.touchtechpayments.com/v1/payerAuthentication',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                }

                try:
                    r = self.session.post("https://macs.touchtechpayments.com/v1/confirmTransaction",headers=headers, data=data)
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                    log.info(e)
                    logger.error(SITE,self.taskID,'Error: {}'.format(e))
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    self.card()

                pares = r.json()['Response']

                data = {"MD":self.MD, "PaRes":pares}
                try:
                    r = self.session.post(f'https://{self.awlabRegion}/on/demandware.store/Sites-awlab-en-Site/en_{self.dwRegion}/Adyen-RedirectToTop?type=treedscontinue',headers={
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                        'content-type': 'application/x-www-form-urlencoded',
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'origin': 'https://verifiedbyvisa.acs.touchtechpayments.com',
                        'referer':'https://verifiedbyvisa.acs.touchtechpayments.com/v1/payerAuthentication',
                    }, data=data)
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                    log.info(e)
                    logger.error(SITE,self.taskID,'Error: {}'.format(e))
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    self.card()
                
                if r.status_code in [200,302]:
                    try:
                        closeFrame = self.session.post(f'https://{self.awlabRegion}/on/demandware.store/Sites-awlab-en-Site/en_{self.dwRegion}/Adyen-CloseIFrame',headers={
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                            'content-type': 'application/x-www-form-urlencoded',
                            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                            'origin': 'https://verifiedbyvisa.acs.touchtechpayments.com',
                            'referer':'https://verifiedbyvisa.acs.touchtechpayments.com/v1/payerAuthentication',
                        }, data={"dwfrm_redirecttotop_redirecttop":"Submit","MD":self.MD,"PaRes":pares,"csrf_token":self.csrf})
                    except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                        log.info(e)
                        logger.error(SITE,self.taskID,'Error: {}'.format(e))
                        time.sleep(int(self.task["DELAY"]))
                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                        self.card()

                    try:
                        confirm = self.session.post(f'https://{self.awlabRegion}/orderconfirmed',headers={
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                            'content-type': 'application/x-www-form-urlencoded',
                            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                            'referer':f'https://{self.awlabRegion}/on/demandware.store/Sites-awlab-en-Site/en_{self.dwRegion}/Adyen-CloseIFrame',
                        }, data={"MD":None,"PaReq":None})
                    except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                        log.info(e)
                        logger.error(SITE,self.taskID,'Error: {}'.format(e))
                        time.sleep(int(self.task["DELAY"]))
                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                        self.card()

                    if confirm.status_code == 200 and "orderconfirmed" in confirm.url or "riepilogoordine" in confirm.url:
                        self.end = time.time() - self.start
                        logger.alert(SITE,self.taskID,'Checkout complete!')
            
                        try:
                            discord.success(
                                webhook=loadSettings()["webhook"],
                                site=SITE,
                                image=self.productImage,
                                title=self.productTitle,
                                size=self.size,
                                price=self.productPrice,
                                paymentMethod="Card",
                                profile=self.task["PROFILE"],
                                product=self.task["PRODUCT"],
                                proxy=self.session.proxies,
                                speed=self.end
                            )
                            while True:
                                pass
                        except:
                            pass
                    
                    else:
                        logger.error(SITE,self.taskID,'Checkout failed. Retrying...')
                        time.sleep(int(self.task["DELAY"]))
                        self.card()

        if payment.status_code in [200,302] and "revieworder" in payment.url:
            try:
                confirm = self.session.post(f'https://{self.awlabRegion}/orderconfirmed',headers={
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                    'content-type': 'application/x-www-form-urlencoded',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'referer':f'https://{self.awlabRegion}/on/demandware.store/Sites-awlab-en-Site/en_{self.dwRegion}/Adyen-CloseIFrame',
                }, data={"MD":None,"PaReq":None})
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.card()

            if confirm.status_code == 200 and "orderconfirmed" in confirm.url:
                self.end = time.time() - self.start
                logger.alert(SITE,self.taskID,'Checkout complete!')
    
                try:
                    discord.success(
                        webhook=loadSettings()["webhook"],
                        site=SITE,
                        image=self.productImage,
                        title=self.productTitle,
                        size=self.size,
                        price=self.productPrice,
                        paymentMethod="Card",
                        profile=self.task["PROFILE"],
                        product=self.task["PRODUCT"],
                        proxy=self.session.proxies,
                        speed=self.end
                    )
                    while True:
                        pass
                except:
                    pass
        else:
            logger.error(SITE,self.taskID,'Failed to get 3DS. Retrying')
            time.sleep(int(self.task["DELAY"]))
            self.card()

                