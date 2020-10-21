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
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies, updateConsoleTitle)
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

        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        self.region = profile["countryCode"].lower()
        
        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
        self.collect()

    def collect(self):
        if "shopdisney" in self.task["PRODUCT"]:
            self.product = self.task["PRODUCT"]
            self.disneyRegion = self.task["PRODUCT"].split('shopdisney.')[1].split('/')[0]
        else:
            self.disneyRegion = 'co.uk'
            self.product = "https://www.shopdisney.{}/{}.html".format(self.disneyRegion,self.task["PRODUCT"])
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
                self.productTitle = soup.find("title").text.strip(" ").replace("\n","").split(' - ')[0]
                self.productImage = soup.find("meta", {"property": "og:image"})["content"]
                self.productPrice = soup.find("meta", {"itemprop": "price"}).text.replace('\n','')
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



        soup = BeautifulSoup(postCart.text,"html.parser")
        count = soup.find("span",{"class":"bag-count"}).text
        if postCart.status_code == 200 and int(count) > 0:
            updateConsoleTitle(True,False,SITE)
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
            self.bagUrl = soup.find('form',{'id':'checkout-shipping-form'})['action']
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
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()

        params = {
            'countryCode': profile["countryCode"],
            'postalCode': profile["zip"],
            'city': profile["city"],
            '_': int(time.time())
        }
        try:
            shippingMethods = self.session.get(self.demandwareBase + "COShippingHook-UpdateShippingMethodList",params=params,headers={
                'accept': '*/*',
                'referer': self.bagUrl,
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
            try:
                soup = BeautifulSoup(shippingMethods.text,"html.parser")
                methods = soup.find_all('input',{'name':'dwfrm_singleshipping_shippingAddress_shippingMethodList'})
                self.method = methods[0]["value"]
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to get shipping')
                time.sleep(int(self.task["DELAY"]))
                self.methods()

            logger.success(SITE,self.taskID,'Retrieved shipping method.')
            self.shipping()
        else:
            logger.error(SITE,self.taskID,'Failed to get shipping')
            time.sleep(int(self.task["DELAY"]))
            self.methods()


    def shipping(self):
        logger.prepare(SITE,self.taskID,'Submitting shipping...')
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
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
                'authority': f'www.shopdisney.{self.disneyRegion}',
                'origin': f'https://www.shopdisney.{self.disneyRegion}',
                'content-type': 'application/x-www-form-urlencoded',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.shipping()


        if postShipping.status_code in [200,302]:
            logger.success(SITE,self.taskID,'Successfully submitted shipping')
            try:
                soup = BeautifulSoup(postShipping.text,"html.parser")
                self.billingSecureKey = soup.find('input',{'name':'dwfrm_billing_securekey'})['value']
                self.bagUrl = soup.find('form',{'id':'js-checkout-billing-form'})['action']
            except Exception as e:
                logger.info(SITE,self.taskID,'Failed to submit shipping. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.shipping()

            if self.task["PAYMENT"].lower() == "paypal":
                self.paypal()
            if self.task["PAYMENT"].lower() == "card":
                self.card()
        else:
            logger.info(SITE,self.taskID,'Failed to submit shipping. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.shipping()
        

    def paypal(self):
        logger.prepare(SITE,self.taskID,'Submitting payment...')
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
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
            postFinal = self.session.post(self.bagUrl,data=payload,headers={
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'referer': self.demandwareBase + 'COShipping-Start/{}'.format(self.secureKey),
                'authority': f'www.shopdisney.{self.disneyRegion}',
                'origin': f'https://www.shopdisney.{self.disneyRegion}',
                'content-type': 'application/x-www-form-urlencoded',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.paypal()

        if postFinal.status_code in [200,302]:
            try:
                pp = self.session.post(self.demandwareBase + "COSummary-Submit",data={'submit-order': 'Submit Order', 'csrf_token':self.csrf},headers={
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'referer': self.siteBase + '/bag?dwcont={}'.format(self.secureKey),
                    'content-type': 'application/x-www-form-urlencoded',
                    'authority': f'www.shopdisney.{self.disneyRegion}',
                    'origin': f'https://www.shopdisney.{self.disneyRegion}',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.paypal()
    
            if pp.status_code in [200,302] and "paypal" in pp.url:
                self.end = time.time() - self.start
                logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')
                updateConsoleTitle(False,True,SITE)
                url = storeCookies(pp.url,self.session)
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
        else:
            logger.error(SITE,self.taskID,'Failed to submit payment. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.paypal()


    def card(self):
        logger.info(SITE,self.taskID,'Starting [CREDIT CARD] checkout...')
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        number = profile["card"]["cardNumber"]
        if str(number[0]) == "3":
            cType = 'Amex'
        if str(number[0]) == "4":
            cType = 'Visa'
        if str(number[0]) == "5":
            cType = 'Master'

        n = 4
        cardSplit = [number[i:i+n] for i in range(0, len(number), n)]
        cardNumbers = f'{cardSplit[0]} / {cardSplit[1]} / {cardSplit[2]} / {cardSplit[3]}'
        print(cardNumbers)


        payload = {
            'dwfrm_billing_paymentMethods_selectedPaymentMethodID': 'WORLDPAY_CREDIT_CARD',
            'dwfrm_billing_paymentMethods_creditCard_type': cType,
            'dwfrm_billing_paymentMethods_creditCard_owner': profile["firstName"] + " " + profile["lastName"],
            'dwfrm_billing_paymentMethods_creditCard_number': cardNumbers,
            'dwfrm_billing_paymentMethods_creditCard_month': profile["card"]["cardMonth"],
            'dwfrm_billing_paymentMethods_creditCard_yearshort': profile["card"]["cardYear"][2:],
            'dwfrm_billing_paymentMethods_creditCard_year': profile["card"]["cardYear"],
            'dwfrm_billing_paymentMethods_creditCard_cvn': profile["card"]["cardCVV"],
            'dwfrm_billing_paymentMethods_creditCard_uuid': '',
            'paymentmethods': 'WORLDPAY_CREDIT_CARD',
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
            postFinal = self.session.post(self.bagUrl,data=payload,headers={
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'referer': self.demandwareBase + 'COShipping-Start/{}'.format(self.secureKey),
                'authority': f'www.shopdisney.{self.disneyRegion}',
                'origin': f'https://www.shopdisney.{self.disneyRegion}',
                'content-type': 'application/x-www-form-urlencoded',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.card()

        if postFinal.status_code in [200,302]:
            try:
                submit = self.session.post(self.demandwareBase + "COSummary-Submit",data={'submit-order': 'Submit Order', 'csrf_token':self.csrf},headers={
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'referer': self.siteBase + '/bag?dwcont={}'.format(self.secureKey),
                    'content-type': 'application/x-www-form-urlencoded',
                    'authority': f'www.shopdisney.{self.disneyRegion}',
                    'origin': f'https://www.shopdisney.{self.disneyRegion}',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.card()
            
            logger.success(SITE,self.taskID,'Successfully submitted card details.')
            if submit.status_code == 200:
                try:
                    soup = BeautifulSoup(submit.text, "html.parser")
                    PaReq = soup.find('input',{'name':'PaReq'})['value']
                    termUrl = soup.find('input',{'name':'TermUrl'})['value']
                    MD = soup.find('input',{'name':'MD'})['value']
                except Exception as e:
                    log.info(e)
                    self.card()

                try:
                    payload = {"PaReq":PaReq, "TermUrl":termUrl,  "MD":MD}
                    payAuth = self.session.post('https://verifiedbyvisa.acs.touchtechpayments.com/v1/payerAuthentication', data=payload, headers={
                        'authority': 'verifiedbyvisa.acs.touchtechpayments.com',
                        'accept-language': 'en-US,en;q=0.9',
                        'referer': 'https://www.workingclassheroes.co.uk/ssl/controls/3DAuthentication/3DRedirect.aspx',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    })
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                    log.info(e)
                    logger.error(SITE,self.taskID,'Error: {}'.format(e))
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    self.card()
            
                if payAuth.status_code == 200:
                    soup = BeautifulSoup(payAuth.text, "html.parser")
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

                    data = {"MD":MD, "PaRes":pares}
                    try:
                        r = self.session.post(termUrl,headers={
                            'authority': 'www.workingclassheroes.co.uk',
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
                    
                    if r.status_code in [200,302] and 'WorldPay' in r.url:
                        self.end = time.time() - self.start
                        logger.alert(SITE,self.taskID,'Checkout Successful!')
                        updateConsoleTitle(False,True,SITE)
                        try:
                            discord.success(
                                webhook=loadSettings()["webhook"],
                                site=SITE,
                                image=self.productImage,
                                title=self.productTitle,
                                size=self.size,
                                price=self.productPrice,
                                paymentMethod='Card',
                                profile=self.task["PROFILE"],
                                product=self.task["PRODUCT"],
                                proxy=self.session.proxies,
                                speed=self.end
                            )
                            sendNotification(SITE,self.productTitle)
                            while True:
                                pass
                        except:
                            pass
                    
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
                                paymentMethod='Card',
                                profile=self.task["PROFILE"],
                                proxy=self.session.proxies
                            )
                        except:
                            pass
                        logger.error(SITE,self.taskID,'Checkout Failed [{}]. Retrying...'.format(r.status_code))
                        time.sleep(int(self.task["DELAY"]))
                        self.card()

