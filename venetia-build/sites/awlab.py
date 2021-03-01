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

from utils.captcha import captcha
from utils.logger import logger
from utils.webhook import discord
from utils.log import log
from utils.adyen import ClientSideEncrypter
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, birthday, injection,storeCookies, updateConsoleTitle, scraper, b64Decode)
SITE = 'AWLAB'


class AWLAB:
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
        self.taskID = taskName
        self.rowNumber = rowNumber

        twoCap = loadSettings()["2Captcha"]
        self.session = scraper()
        
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        self.dwRegion = profile["countryCode"].upper()

        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
        self.awlabRegion = self.task["PRODUCT"].split('https://')[1].split('/')[0]

        threading.Thread(target=self.task_checker,daemon=True).start()
        self.collect()

    def collect(self):
        while True:
            logger.prepare(SITE,self.taskID,'Getting product page...')
            try:
                retrieve = self.session.get(self.task["PRODUCT"])
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue

            if retrieve.status_code == 200:
                self.start = time.time()
                logger.warning(SITE,self.taskID,'Got product page')
                try:
                    soup = BeautifulSoup(retrieve.text, "html.parser")

                    self.productPrice = str(soup.find_all('span',{'class':'b-price__sale'})[0].text)
                    self.productTitle = str(soup.find('title').text.split('-')[0])
                    self.productImage = str(soup.find('link',{'rel':'image_src'})["href"])
                    self.productId = soup.find('div',{'id':'pdpMain'})["data-product-id"]

                    if self.productId == None: continue

                    try:
                        retrieveSizes = self.session.get(f'https://{self.awlabRegion}/on/demandware.store/Sites-awlab-en-Site/en_{self.dwRegion}/Product-Variation?pid={self.productId}&format=ajax', headers={
                            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                            'referer':self.task['PRODUCT']
                        })
                    except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                        log.info(e)
                        logger.error(SITE,self.taskID,'Error: {}'.format(e))
                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                        time.sleep(int(self.task["DELAY"]))
                        continue

                    foundSizes = soup.find('ul',{'class':'swatches b-size-selector__list b-size-selector_large b-size-selector_large-sticky'})
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
                        continue
        
                    if self.task["SIZE"].lower() == "random":
                        chosen = random.choice(allSizes)
                        self.pid = chosen.split(':')[1]
                        self.size = chosen.split(':')[0]
                        logger.warning(SITE,self.taskID,f'Found Size => {self.size}')
                    
            
                    else:
                        if self.task["SIZE"] not in sizes:
                            logger.error(SITE,self.taskID,'Size Not Found')
                            time.sleep(int(self.task["DELAY"]))
                            continue
                        for size in allSizes:
                            if self.task["SIZE"] == size.split(':')[0]:
                                self.pid = size.split(':')[1]
                                self.size = size.split(':')[0]
                                logger.warning(SITE,self.taskID,f'Found Size => {self.size}')
                            
                except Exception as e:
                    log.info(e)
                    logger.error(SITE,self.taskID,'Failed to scrape page (Most likely out of stock). Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    continue

                self.addToCart()

            else:
                logger.error(SITE,self.taskID,f'Failed to get product page => {str(retrieve.status_code)}. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                continue

    def addToCart(self):
        logger.prepare(SITE,self.taskID,'Carting product...')
        payload = {
            'Quantity': 1,
            'sizeTable': '',
            'cartAction': 'add',
            'pid': self.pid
        }

        try:
            postCart = self.session.post(f'https://{self.awlabRegion}/on/demandware.store/Sites-awlab-en-Site/en_{self.dwRegion}/Cart-AddProduct?format=ajax',data=payload, headers={
                'accept-language': 'en-US,en;q=0.9',
                'origin': f'https://{self.awlabRegion}',
                'referer': self.task["PRODUCT"],
                'accept':'text/html, */*; q=0.01',
                'x-requested-with': 'XMLHttpRequest'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
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
                'x-requested-with': 'XMLHttpRequest'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()

        if postCart.status_code == 200 and submitCart.status_code == 200 and submitCart.json()["success"] == True:
            logger.warning(SITE,self.taskID,'Successfully carted')
            updateConsoleTitle(True,False,SITE)
            self.method()
        if postCart.status_code == 429 or submitCart.status_code == 429:
            logger.error(SITE,self.taskID,'Rate Limited. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()
        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            if self.task["SIZE"].lower() == "random":
                self.collect()
            else:    
                time.sleep(int(self.task["DELAY"]))
                self.addToCart()

    def method(self):
        logger.prepare(SITE,self.taskID,'Setting checkout method...')
        try:
            checkout = self.session.get(f'https://{self.awlabRegion}/checkout',headers={
                'accept-language': 'en-US,en;q=0.9',
                'origin': f'https://{self.awlabRegion}',
                'referer': self.task["PRODUCT"],
                'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()

 
        if checkout.status_code == 200:
            logger.warning(SITE,self.taskID,'Set checkout method')
            soup = BeautifulSoup(checkout.text,"html.parser")
            self.csrf = soup.find('input',{'name':'csrf_token'})['value']
            self.shipping()
        
        else:
            logger.error(SITE,self.taskID,'Failed to get checkout page. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.method()

    def shipping(self):
        logger.prepare(SITE,self.taskID,'Submitting shipping...')
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        bday = birthday()

        try:
            states = self.session.post(f'https://{self.awlabRegion}/on/demandware.store/Sites-awlab-en-Site/en_{self.dwRegion}/Address-UpdateAddressFormStates?format=ajax', data={'selectedCountryCode': self.dwRegion, 'formId': 'singleshipping.shippingAddress.addressFields.states.state'}, headers={
                'accept-language': 'en-US,en;q=0.9',
                'origin': f'https://{self.awlabRegion}',
                'referer':f'https://{self.awlabRegion}/shipping',
                'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
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
                'dwfrm_singleshipping_shippingAddress_addressFields_isValidated': False,
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
                'dwfrm_singleshipping_shippingAddress_useAsBillingAddress': True,
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
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.method()

        print(shipping.status_code)
        if shipping.status_code == 200:
            logger.warning(SITE,self.taskID,'Successfully submitted shipping')
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
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
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

        logger.prepare(SITE,self.taskID,'Submitting payment...')
        try:
            payment = self.session.post(f'https://{self.awlabRegion}/on/demandware.store/Sites-awlab-en-Site/en_{self.dwRegion}/COBilling-Billing', data=payload, headers={
                'accept-language': 'en-US,en;q=0.9',
                'origin': f'https://{self.awlabRegion}',
                'referer':f'https://{self.awlabRegion}/billing',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'x-requested-with': 'XMLHttpRequest',
                'accept':'*/*',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.method()

        if payment.status_code == 200:
            logger.warning(SITE,self.taskID,'Payment submitted')
            self.end = time.time() - self.start
            try:
                data = payment.json()
            except:
                logger.error(SITE,self.taskID,'Failed to get token. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.paypal()

            logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')
            ppURL = 'https://www.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token={}&useraction=commit'.format(data["token"])

            url = storeCookies(ppURL,self.session, self.productTitle, self.productImage, self.productPrice)
            updateConsoleTitle(False,True,SITE)
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
            self.method()


    def cad(self):
        logger.info(SITE,self.taskID,'Starting [CAD] checkout...')
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()

        # token = captcha.v2()
    
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
        logger.prepare(SITE,self.taskID,'Submitting payment...')
        try:
            payment = self.session.post(f'https://{self.awlabRegion}/on/demandware.store/Sites-awlab-en-Site/en_{self.dwRegion}/COBilling-Billing', data=payload, headers={
                'accept-language': 'en-US,en;q=0.9',
                'origin': f'https://{self.awlabRegion}',
                'referer':f'https://{self.awlabRegion}/billing',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'x-requested-with': 'XMLHttpRequest',
                'accept':'*/*',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.card()

        if payment.status_code in [200,302]:
            logger.warning(SITE,self.taskID,'Payment submitted')
            self.end = time.time() - self.start
            logger.alert(SITE,self.taskID,'Checkout complete!')
            updateConsoleTitle(False,True,SITE)
            
            try:
                discord.success(
                    webhook=loadSettings()["webhook"],
                    site=SITE,
                    image=self.productImage,
                    title=self.productTitle,
                    size=self.size,
                    price=self.productPrice,
                    paymentMethod="CAD",
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
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        number = profile["card"]["cardNumber"]
        if str(number[0]) == "3":
            cType = 'amex'
        if str(number[0]) == "4":
            cType = 'visa'
        if str(number[0]) == "5":
            cType = 'mc'


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
            'noPaymentNeeded': True,
            'dwfrm_billing_paymentMethods_creditCard_selectedCardID': '',
            'dwfrm_billing_paymentMethods_selectedPaymentMethodID': 'CREDIT_CARD',
            'dwfrm_billing_billingAddress_personalData': True,
            'dwfrm_billing_billingAddress_tersmsOfSale': True,
            'csrf_token': self.csrf
        }
        logger.prepare(SITE,self.taskID,'Submitting payment...')
        try:
            payment = self.session.post(f'https://{self.awlabRegion}/on/demandware.store/Sites-awlab-en-Site/en_{self.dwRegion}/COBilling-Billing', data=payload, headers={
                'accept-language': 'en-US,en;q=0.9',
                'origin': f'https://{self.awlabRegion}',
                'referer':f'https://{self.awlabRegion}/billing',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'x-requested-with': 'XMLHttpRequest',
                'accept':'*/*',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.card()


        if payment.status_code in [200,302] and "orderNo" in payment.url:
            logger.warning(SITE,self.taskID,'Payment submitted')
            logger.info(SITE,self.taskID,'Initiating 3DS checkout')
            soup = BeautifulSoup(payment.text, 'html.parser')
            self.termURL = soup.find('input',{'name':'TermUrl'})['value'] 
            self.PaReq = soup.find('input',{'name':'PaReq'})['value'] 
            self.MD = soup.find('input',{'name':'MD'})['value'] 

            self.Dpayload = {
               "TermUrl":self.termURL,
               "PaReq":self.PaReq,
               "MD":self.MD 
            }
            self.threeDs()

        elif payment.status_code in [200,302] and "revieworder" in payment.url:
            logger.prepare(SITE,self.taskID,'Card declined. Retrying....')

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
            self.card()

        else:
            logger.error(SITE,self.taskID,'Failed to get 3DS. Retrying')
            time.sleep(int(self.task["DELAY"]))
            self.card()


    def threeDs(self):
        try:
            payerAuth = self.session.post('https://idcheck.acs.touchtechpayments.com/v1/payerAuthentication', data=self.Dpayload, headers={
                'referer':f'https://{self.awlabRegion}',
                'content-type': 'application/x-www-form-urlencoded',
                'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.threeDs()

        if payerAuth.status_code == 200:
            try:
                transToken = payerAuth.text.split('token: "')[1].split('"')[0]
                payload = {"transToken":transToken}
                poll = self.session.post('https://poll.touchtechpayments.com/poll', json=payload, headers={
                    'authority': 'verifiedbyvisa.acs.touchtechpayments.com',
                    'accept-language': 'en-US,en;q=0.9',
                    'referer': 'https://verifiedbyvisa.acs.touchtechpayments.com/v1/payerAuthentication',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                    'accept':'*/*',
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.threeDs()


            if poll.json()["status"] == "blocked":
                logger.error(SITE,self.taskID,'Card Blocked. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.threeDs()
            if poll.json()["status"] == "pending":
                discord.threeDS(
                    webhook=loadSettings()["webhook"],
                    site=SITE,
                    image=self.productImage,
                    title=self.productTitle,
                    size=self.size,
                    price=self.productPrice,
                    paymentMethod="Card",
                    profile=self.task["PROFILE"],
                    product=self.task["PRODUCT"],
                    proxy=self.session.proxies
                )
                while True:
                    pass
                logger.warning(SITE,self.taskID,'Polling 3DS...')
                while poll.json()["status"] == "pending":
                    poll = self.session.post('https://poll.touchtechpayments.com/poll',headers={
                        'authority': 'verifiedbyvisa.acs.touchtechpayments.com',
                        'accept-language': 'en-US,en;q=0.9',
                        'referer': 'https://verifiedbyvisa.acs.touchtechpayments.com/v1/payerAuthentication',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                        'accept':'*/*',}, json=payload)
            
            try:
                aaa = poll.json()
            except:
                logger.error(SITE,self.taskID,'Failed to retrieve auth token for 3DS. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.threeDs()
            if poll.json()["status"] == "success":
                authToken = poll.json()['authToken']
            else:
                logger.error(SITE,self.taskID,'Failed to retrieve auth token for 3DS. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.threeDs()

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
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.threeDs()

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
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.threeDs()
            
            if r.status_code in [200,302]:
                try:
                    closeFrame = self.session.post(f'https://{self.awlabRegion}/on/demandware.store/Sites-awlab-en-Site/en_{self.dwRegion}/Adyen-CloseIFrame',headers={
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                        'content-type': 'application/x-www-form-urlencoded',
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'origin': 'https://verifiedbyvisa.acs.touchtechpayments.com',
                        'referer':'https://verifiedbyvisa.acs.touchtechpayments.com/v1/payerAuthentication',
                    }, data={"dwfrm_redirecttotop_redirecttop":"Submit","MD":self.MD,"PaRes":pares,"csrf_token":self.csrf})
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    log.info(e)
                    logger.error(SITE,self.taskID,'Error: {}'.format(e))
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    self.threeDs()

                logger.prepare(SITE,self.taskID,'Confirming Order...')
                try:
                    confirm = self.session.post(f'https://{self.awlabRegion}/orderconfirmed',headers={
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                        'content-type': 'application/x-www-form-urlencoded',
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'referer':f'https://{self.awlabRegion}/on/demandware.store/Sites-awlab-en-Site/en_{self.dwRegion}/Adyen-CloseIFrame',
                    }, data={"MD":None,"PaReq":None})
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    log.info(e)
                    logger.error(SITE,self.taskID,'Error: {}'.format(e))
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    self.threeDs()

                if confirm.status_code == 200 and "orderconfirmed" in confirm.url or "riepilogoordine" in confirm.url:
                    logger.warning(SITE,self.taskID,'Order confirmed')
                    self.end = time.time() - self.start
                    logger.alert(SITE,self.taskID,'Checkout complete!')
                    updateConsoleTitle(False,True,SITE)
        
                    try:
                        discord.success(
                            webhook=loadSettings()["webhook"],
                            site=SITE,
                            url=self.task["PRODUCT"],
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
                        while True:
                            pass
                
                else:
                    logger.error(SITE,self.taskID,'Checkout failed. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.threeDs()

        else:
            logger.error(SITE,self.taskID,'Failed to get 3DS. Retrying')
            time.sleep(int(self.task["DELAY"]))
            self.threeDs()



                