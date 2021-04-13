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
import tls as client
from requests_toolbelt import MultipartEncoder

from utils.captcha import captcha
from utils.logger import logger
from utils.webhook import Webhook
from utils.log import log
from utils.adyen import ClientSideEncrypter
from utils.threeDS import threeDSecure

from utils.functions import (
    loadSettings,
    loadProfile,
    loadProxy,
    createId,
    loadCookie,
    loadToken,
    sendNotification,
    injection,
    storeCookies,
    updateConsoleTitle,
    scraper,
    footlocker_snare,
    birthday
)
import utils.config as CONFIG

_SITE_ = 'AWLAB'
SITE = 'Aw-Lab'
class AWLAB:
    def success(self,message):
        logger.success(SITE,self.taskID,message)
    def error(self,message):
        logger.error(SITE,self.taskID,message)
    def prepare(self,message):
        logger.prepare(SITE,self.taskID,message)
    def warning(self,message):
        logger.warning(SITE,self.taskID,message)
    def info(self,message):
        logger.info(SITE,self.taskID,message)
    def secondary(self,message):
        logger.secondary(SITE,self.taskID,message)
    def alert(self,message):
        logger.alert(SITE,self.taskID,message)


    def task_checker(self):
        originalTask = self.task
        while True:
            with open('./{}/tasks.csv'.format(_SITE_.lower()),'r') as csvFile:
                csv_reader = csv.DictReader(csvFile)
                row = [row for idx, row in enumerate(csv_reader) if idx in (self.rowNumber,self.rowNumber)]
                self.task = row[0]
                try:
                    self.task['ACCOUNT EMAIL'] = originalTask['ACCOUNT EMAIL']
                    self.task['ACCOUNT PASSWORD'] = originalTask['ACCOUNT PASSWORD']
                except:
                    pass
                csvFile.close()

            time.sleep(2)

    def __init__(self, task, taskName, rowNumber):
        self.task = task
        self.taskID = taskName
        self.rowNumber = rowNumber

        if self.rowNumber != 'qt': 
            threading.Thread(target=self.task_checker,daemon=True).start()

        try:
            # self.session = client.Session(browser=client.Fingerprint.CHROME_83)
            self.session = scraper()
        except Exception as e:
            self.error(f'error => {e}')
            self.__init__(task,taskName,rowNumber)


        self.webhookData = {
            "site":SITE,
            "product":"n/a",
            "size":"n/a",
            "image":"https://i.imgur.com/VqWvzDN.png",
            "price":"0",
            "profile":self.task['PROFILE'],
            "speed":0,
            "url":"https://venetiacli.io",
            "paymentMethod":"n/a",
            "proxy":"n/a",
            "product_url":self.task['PRODUCT']
        }

        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)

        self.profile = loadProfile(self.task["PROFILE"])
        if self.profile == None:
            self.error("Profile Not found. Exiting...")
            time.sleep(10)
            sys.exit()

        if self.profile['countryCode'].upper() == 'IT':
            self.baseUrl = 'https://www.aw-lab.com'
            self.demandWareBase = 'https://www.aw-lab.com/on/demandware.store/Sites-awlab-it-Site/it_IT/'
        if self.profile['countryCode'].upper() == 'ES':
            self.baseUrl = 'https://es.aw-lab.com'
            self.demandWareBase = 'https://es.aw-lab.com/on/demandware.store/Sites-awlab-es-Site/es_ES/'
        else:
            self.baseUrl = 'https://en.aw-lab.com'
            self.demandWareBase = 'https://en.aw-lab.com/on/demandware.store/Sites-awlab-en-Site/en_GB/'

        self.tasks()
    
    def tasks(self):

        self.monitor()
        self.addToCart()
        self.method()
        self.shipping()

        if self.task['PAYMENT'].strip().lower() == "paypal":
            self.paypal()
        elif self.task['PAYMENT'].strip().lower() == "cad":
            self.cad() #cash on devliery
        else:
            self.card()

        self.sendToDiscord()

    def monitor(self):
        while True:
            self.prepare("Getting Product...")
            try:
                
                response = self.session.get(self.task['PRODUCT'])
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue

            try:
                n_a = self.session.get('{}Product-Variation?format=ajax&pid={}'.format(self.demandWareBase,self.task['PRODUCT']),headers={
                    'x-requested-with': 'XMLHttpRequest',
                    'accept': 'application/json, text/javascript, */*; q=0.01',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/json',
                    'referer':self.baseUrl
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue
            

            if response.status_code == 200:
                self.start = time.time()

                self.warning("Retrieved Product")

                try:
                    soup = BeautifulSoup(response.text, "html.parser")

                    self.webhookData['product'] = str(soup.find('title').text.split('-')[0])
                    self.webhookData['image'] = str(soup.find('link',{'rel':'image_src'})["href"])
                    self.webhookData['price'] = str(soup.find_all('span',{'class':'b-price__sale'})[0].text)

                    self.productId = soup.find('div',{'id':'pdpMain'})["data-product-id"]
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
                        self.error("No sizes available")
                        time.sleep(int(self.task["DELAY"]))
                        continue

                    if self.task["SIZE"].strip().lower() != "random":
                        if self.task["SIZE"] not in sizes:
                            self.error("Size not available")
                            time.sleep(int(self.task["DELAY"]))
                            continue
                        else:
                            for size in allSizes:
                                if size.split(':')[0].strip().lower() == self.task["SIZE"].strip().lower():
                                    self.size = size.split(':')[0]
                                    self.pid = size.split(":")[1]
                                    
                                    self.warning(f"Found Size => {self.size}")
        
                    else:
                        selected = random.choice(allSizes)
                        self.size = selected.split(":")[0]
                        self.pid = selected.split(":")[1]
                        
                        self.warning(f"Found Size => {self.size}")

                        

                except Exception as e:
                    log.info(e)
                    self.error("Failed to parse product data (maybe OOS)")
                    time.sleep(int(self.task['DELAY']))
                    continue

                return
                    
            else:
                self.error(f"Failed to get product [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def addToCart(self):
        while True:
            self.prepare("Adding to cart...")
            
            payload = {
                'Quantity': 1,
                'sizeTable': '',
                'cartAction': 'add',
                'pid': self.pid
            }

            try:
                response = self.session.post('{}Cart-AddProduct?format=ajax'.format(self.demandWareBase),data=payload, headers={
                    'accept-language': 'en-US,en;q=0.9',
                    'origin': self.baseUrl,
                    'referer': self.task["PRODUCT"],
                    'accept':'text/html, */*; q=0.01',
                    'x-requested-with': 'XMLHttpRequest'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            try:
                response2 = self.session.post('{}Cart-SubmitForm?format=ajax'.format(self.demandWareBase), data={'dwfrm_cart_checkoutCart': 'true'}, headers={
                    'accept-language': 'en-US,en;q=0.9',
                    'origin': self.baseUrl,
                    'referer': self.task["PRODUCT"],
                    'accept':'text/html, */*; q=0.01',
                    'x-requested-with': 'XMLHttpRequest'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue



            if response.status_code == 200 and response2.status_code == 200:
                try:
                    stat = response2.json()["success"]
                except:
                    self.error(f"Failed to cart [Failed to parse response]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue
                
                if stat == True:
                    self.success("Added to cart!")
                    updateConsoleTitle(True,False,SITE)
                    return
                else:
                    self.error(f"Failed to cart [{str(response.status_code)}]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue
            
            else:
                self.error(f"Failed to cart [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def method(self):
        while True:
            self.prepare("Setting checkout method...")
            
            try:
                response = self.session.get(f'{self.baseUrl}/checkout',headers={
                    'accept-language': 'en-US,en;q=0.9',
                    'origin': self.baseUrl,
                    'referer': self.task["PRODUCT"],
                    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                })

            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if response.status_code == 200:
                try:
                    soup = BeautifulSoup(response.text,"html.parser")
                    self.csrf = soup.find('input',{'name':'csrf_token'})['value']
                except:
                    self.error(f"Failed to set checkout method [Failed to parse response]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue

                self.warning("Set checkout method")
                return
            else:
                self.error(f"Failed to set checkout method [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def validate(self):
        while True:
            self.prepare("Validating address...")
            try:
                states = self.session.post('{}Address-UpdateAddressFormStates?format=ajax'.format(self.demandWareBase), data={'selectedCountryCode': self.profile['countryCode'].upper(), 'formId': 'singleshipping.shippingAddress.addressFields.states.state'}, headers={
                    'accept-language': 'en-US,en;q=0.9',
                    'origin': self.baseUrl,
                    'referer':f'{self.baseUrl}/shipping',
                    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                })

            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if states.status_code == 200:
                try:
                    soup = BeautifulSoup(states.text,"html.parser")
                    states = soup.find("select",{"name":"dwfrm_singleshipping_shippingAddress_addressFields_states_state"})
                    for s in states:
                        try:

                            if self.profile["region"].lower() in s.text.strip().lower():
                                self.stateID = s["value"]
                        except:
                            pass
                except:
                    self.error(f"Failed to set shipping [failed to get states]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue
            else:
                self.error(f"Failed to set shipping [{str(states.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
            
            

            try:
                payload = {
                    "addressLine1":'{} {}'.format(self.profile["house"], self.profile["addressOne"]),
                    "zipCode":self.profile['zip'],
                    "city":self.profile['CITY'],
                    "mainDivision":self.stateID,
                    "countryCode":self.profile['countryCode'].upper()
                }
                
            except Exception as e:
                self.error(f"Failed to construct shipping form. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
                
            try:
                response = self.session.post('{}Address-Validate?format=ajax'.format(self.demandWareBase), data=payload, headers={
                    'accept-language': 'en-US,en;q=0.9',
                    'origin': self.baseUrl,
                    'referer':f'{self.baseUrl}/shipping',
                    'content-type': 'application/x-www-form-urlencoded',
                    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'x-requested-with': 'XMLHttpRequest'

                })

            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

        
            if response.status_code == 200:

                try:
                    soup = BeautifulSoup(response.text, "html.parser")
                    options = soup.find_all('span',{'class':'b-checkout-delivery__address-text'})[0].text
                    self.addressLine1 = options.split(',')[0].strip()
                    self.zip = options.split(',')[1].split(',')[0].strip()
                    self.city = options.split(',')[2].strip()
                except Exception:
                    self.error("Failed to validate address [failed to parse response]. Retrying...")
                    continue

                self.warning("Successfully validated address")
                return

            else:
                self.error(f"Failed to validate address [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def shipping(self):
        while True:
            self.prepare("Submitting shipping...")
            try:
                states = self.session.post('{}Address-UpdateAddressFormStates?format=ajax'.format(self.demandWareBase), data={'selectedCountryCode': self.profile['countryCode'].upper(), 'formId': 'singleshipping.shippingAddress.addressFields.states.state'}, headers={
                    'accept-language': 'en-US,en;q=0.9',
                    'origin': self.baseUrl,
                    'referer':f'{self.baseUrl}/shipping',
                    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                })

            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if states.status_code == 200:
                try:
                    soup = BeautifulSoup(states.text,"html.parser")
                    states = soup.find("select",{"name":"dwfrm_singleshipping_shippingAddress_addressFields_states_state"})
                    for s in states:
                        try:

                            if self.profile["region"].lower() in s.text.strip().lower():
                                self.stateID = s["value"]
                        except:
                            pass
                except:
                    self.error(f"Failed to set shipping [failed to get states]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue
            else:
                self.error(f"Failed to set shipping [{str(states.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
            
            

            try:
                bday = birthday()
                payload = {
                    'dwfrm_billing_billingAddress_email_emailAddress': self.profile["email"],
                    'dwfrm_singleshipping_shippingAddress_addressFields_phonecountrycode_codes': self.profile["phonePrefix"],
                    'dwfrm_singleshipping_shippingAddress_addressFields_phonewithoutcode': self.profile["phone"],
                    'dwfrm_singleshipping_shippingAddress_addressFields_phone': '{}{}'.format(self.profile["phonePrefix"], self.profile["phone"]),
                    'dwfrm_singleshipping_shippingAddress_addressFields_isValidated': True,
                    'dwfrm_singleshipping_shippingAddress_addressFields_firstName': self.profile["firstName"],
                    'dwfrm_singleshipping_shippingAddress_addressFields_lastName': self.profile["lastName"],
                    'dwfrm_singleshipping_shippingAddress_addressFields_title': 'Mr',
                    'dwfrm_singleshipping_shippingAddress_addressFields_birthdayfields_day': bday["day"],
                    'dwfrm_singleshipping_shippingAddress_addressFields_birthdayfields_month': bday["month"],
                    'dwfrm_singleshipping_shippingAddress_addressFields_birthdayfields_year': bday["year"],
                    'dwfrm_singleshipping_shippingAddress_addressFields_birthday': '{}-{}-{}'.format(bday["year"],bday["month"],bday["day"]),
                    'dwfrm_singleshipping_shippingAddress_addressFields_address1': '{} {}, {}'.format(self.profile["house"], self.profile["addressOne"], self.profile["addressTwo"]),
                    'dwfrm_singleshipping_shippingAddress_addressFields_postal': self.profile["zip"],
                    'dwfrm_singleshipping_shippingAddress_addressFields_city': self.profile["city"],
                    'dwfrm_singleshipping_shippingAddress_addressFields_states_state': self.stateID,
                    'dwfrm_singleshipping_shippingAddress_addressFields_country': self.profile["countryCode"],
                    'dwfrm_singleshipping_shippingAddress_useAsBillingAddress': True,
                    'dwfrm_singleshipping_shippingAddress_shippingMethodID': 'ANY_STD',
                    'dwfrm_singleshipping_shippingAddress_save': 'Proceed to Checkout',
                    'csrf_token': self.csrf
                }
                
            except Exception as e:
                self.error(f"Failed to construct shipping form. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
                
            try:
                response = self.session.post('{}COShipping-SingleShipping'.format(self.demandWareBase), data=payload, headers={
                    'accept-language': 'en-US,en;q=0.9',
                    'origin': self.baseUrl,
                    'referer':f'{self.baseUrl}/shipping',
                    'content-type': 'application/x-www-form-urlencoded',
                    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                })

            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

        
            if response.status_code == 200:

                self.warning("Successfully set shipping")
                return

            else:
                self.error(f"Failed to set shipping [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

   
    
    def paypal(self):
        while True:
            self.prepare("Getting paypal checkout...")

            if CONFIG.captcha_configs[_SITE_]['type'].lower() == 'v3':
                capToken = captcha.v3(CONFIG.captcha_configs[_SITE_]['siteKey'],self.baseUrl,self.task['PROXIES'],SITE,self.taskID)
            elif CONFIG.captcha_configs[_SITE_]['type'].lower() == 'v2':
                capToken = captcha.v2(CONFIG.captcha_configs[_SITE_]['siteKey'],self.baseUrl,self.task['PROXIES'],SITE,self.taskID)

            try:
                payload = {
                    'dwfrm_billing_save': True,
                    'dwfrm_billing_billingAddress_addressId': 'guest-shipping',
                    'dwfrm_billing_billingAddress_addressFields_isValidated': '',
                    'dwfrm_billing_billingAddress_addressFields_firstName': self.profile["firstName"],
                    'dwfrm_billing_billingAddress_addressFields_lastName': self.profile["lastName"],
                    'dwfrm_billing_billingAddress_addressFields_address1': '{} {}, {}'.format(self.profile["house"], self.profile["addressOne"], self.profile["addressTwo"]),
                    'dwfrm_billing_billingAddress_addressFields_postal': self.profile["zip"],
                    'dwfrm_billing_billingAddress_addressFields_city': self.profile["city"],
                    'dwfrm_billing_billingAddress_addressFields_states_state': self.stateID,
                    'dwfrm_billing_billingAddress_addressFields_country': self.profile["countryCode"],
                    'dwfrm_billing_couponCode': '',
                    'dwfrm_billing_paymentMethods_creditCard_encrypteddata': '',
                    'dwfrm_billing_paymentMethods_creditCard_type': '',
                    'dwfrm_adyPaydata_brandCode': '',
                    'noPaymentNeeded': True,
                    'dwfrm_billing_paymentMethods_creditCard_selectedCardID': '',
                    'dwfrm_billing_paymentMethods_selectedPaymentMethodID': 'PayPal',
                    'dwfrm_billing_billingAddress_personalData': True,
                    'dwfrm_billing_billingAddress_tersmsOfSale': True,
                    'csrf_token': self.csrf,
                    'g-recaptcha-response':capToken
                }
            except Exception as e:
                self.error(f"Failed to construct paypal form ({e}). Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

            

            try:
                response = self.session.post('{}COBilling-Billing'.format(self.demandWareBase), data=payload, headers={
                    'accept-language': 'en-US,en;q=0.9',
                    'origin': self.baseUrl,
                    'referer':f'{self.baseUrl}/billing',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'x-requested-with': 'XMLHttpRequest',
                    'accept':'*/*',
                })

            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if response.status_code == 200:

                try:
                    data = response.json()
                    token = data['token']
                except:
                    self.error(f"Failed to get paypal checkout [failed to parse response]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue
                
                self.end = time.time() - self.start
                self.webhookData['speed'] = self.end

                self.success("Got paypal checkout!")
                updateConsoleTitle(False,True,SITE)

                self.webhookData['url'] = storeCookies(
                    'https://www.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token={}&useraction=commit'.format(token),
                    self.session,
                    self.webhookData['product'],
                    self.webhookData['image'],
                    self.webhookData['price'],
                    False
                )
                return


                
            else:
                self.error(f"Failed to get paypal checkout [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def cad(self):
        while True:
            self.prepare("Getting CAD checkout...")

            if CONFIG.captcha_configs[_SITE_]['type'].lower() == 'v3':
                capToken = captcha.v3(CONFIG.captcha_configs[_SITE_]['siteKey'],self.baseUrl,self.task['PROXIES'],SITE,self.taskID)
            elif CONFIG.captcha_configs[_SITE_]['type'].lower() == 'v2':
                capToken = captcha.v2(CONFIG.captcha_configs[_SITE_]['siteKey'],self.baseUrl,self.task['PROXIES'],SITE,self.taskID)

            try:
                payload = {
                    'dwfrm_billing_save': True,
                    'dwfrm_billing_billingAddress_addressId': 'guest-shipping',
                    'dwfrm_billing_billingAddress_addressFields_isValidated': '',
                    'dwfrm_billing_billingAddress_addressFields_firstName': self.profile["firstName"],
                    'dwfrm_billing_billingAddress_addressFields_lastName': self.profile["lastName"],
                    'dwfrm_billing_billingAddress_addressFields_address1': '{} {}, {}'.format(self.profile["house"], self.profile["addressOne"], self.profile["addressTwo"]),
                    'dwfrm_billing_billingAddress_addressFields_postal': self.profile["zip"],
                    'dwfrm_billing_billingAddress_addressFields_city': self.profile["city"],
                    'dwfrm_billing_billingAddress_addressFields_states_state': self.stateID,
                    'dwfrm_billing_billingAddress_addressFields_country': self.profile["countryCode"],
                    'dwfrm_billing_couponCode': '',
                    'dwfrm_billing_paymentMethods_creditCard_encrypteddata': '',
                    'dwfrm_billing_paymentMethods_creditCard_type': '',
                    'dwfrm_adyPaydata_brandCode': '',
                    'noPaymentNeeded': True,
                    'dwfrm_billing_paymentMethods_creditCard_selectedCardID': '',
                    'dwfrm_billing_paymentMethods_selectedPaymentMethodID': 'CASH_ON_DELIVERY',
                    'dwfrm_billing_billingAddress_personalData': True,
                    'dwfrm_billing_billingAddress_tersmsOfSale': True,
                    'csrf_token': self.csrf,
                    'g-recaptcha-response':capToken
                }
            except Exception as e:
                self.error(f"Failed to construct CAD form ({e}). Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue


            try:
                response = self.session.post('{}COBilling-Billing'.format(self.demandWareBase), data=payload, headers={
                    'accept-language': 'en-US,en;q=0.9',
                    'origin': self.baseUrl,
                    'referer':f'{self.baseUrl}/billing',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'x-requested-with': 'XMLHttpRequest',
                    'accept':'*/*',
                })

            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if response.status_code == 200:

                try:
                    data = response.json()
                    token = data['token']
                except:
                    self.error(f"Failed to get CAD checkout [failed to parse response]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue
                
                self.end = time.time() - self.start
                self.webhookData['speed'] = self.end

                self.success("Checkout Successful")
                updateConsoleTitle(False,True,SITE)

                return


                
            else:
                self.error(f"Failed to get CAD checkout [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    
    def card(self):
        while True:
            self.prepare("Completing card checkout...")
            number = self.profile["card"]["cardNumber"]
            if str(number[0]) == "3":
               cType = 'amex'
            if str(number[0]) == "4":
                cType = 'visa'
            if str(number[0]) == "5":
                cType = 'mc'

            if CONFIG.captcha_configs[_SITE_]['type'].lower() == 'v3':
                capToken = captcha.v3(CONFIG.captcha_configs[_SITE_]['siteKey'],self.baseUrl,self.task['PROXIES'],SITE,self.taskID)
            elif CONFIG.captcha_configs[_SITE_]['type'].lower() == 'v2':
                capToken = captcha.v2(CONFIG.captcha_configs[_SITE_]['siteKey'],self.baseUrl,self.task['PROXIES'],SITE,self.taskID)


            try:
                encryptedInfo = ClientSideEncrypter("10001|A58F2F0D8A4A08232DD1903F00A3F99E99BB89D5DEDF7A9612A3C0DC9FA9D8BDB2A20A233B663B0A48D47A0A1DDF164B3206985EFF19686E3EF75ADECF77BA10013B349C9F95CEBB5A66C48E3AD564410DB77A5E0798923E849E48A6274A80CBE1ACAA886FF3F91C40C6F2038D90FABC9AEE395D4872E24183E8B2ACB28025964C5EAE8058CB06288CDA80D44F69A7DFD3392F5899886094DB23F703DAD458586338BF21CF84288C22020CD2AB539A35BF1D98582BE5F79184C84BE877DB30C3C2DE81E394012511BFE9749E35C3E40D28EE3338DE7CBB1EDD253951A7B66A85E9CC920CA2A40CAD48ACD8BD1AE681997D1655E59005F1887B872A7A873EDBD1", "_0_1_18")
                adyenEncrypted = str(encryptedInfo.generate_adyen_nonce(
                    self.profile["firstName"] + " " + self.profile["lastName"],
                    self.profile["card"]["cardNumber"],
                    self.profile["card"]["cardCVV"],
                    self.profile["card"]["cardMonth"], 
                    self.profile["card"]["cardYear"]
                ).replace("b'", "").replace("'", ""))
                payload = {
                    'dwfrm_billing_save': True,
                    'dwfrm_billing_billingAddress_addressId': 'guest-shipping',
                    'dwfrm_billing_billingAddress_addressFields_isValidated': True,
                    'dwfrm_billing_billingAddress_addressFields_firstName': self.profile["firstName"],
                    'dwfrm_billing_billingAddress_addressFields_lastName': self.profile["lastName"],
                    'dwfrm_billing_billingAddress_addressFields_address1': '{} {}, {}'.format(self.profile["house"], self.profile["addressOne"], self.profile["addressTwo"]),
                    'dwfrm_billing_billingAddress_addressFields_postal': self.profile["zip"],
                    'dwfrm_billing_billingAddress_addressFields_city': self.profile["city"],
                    'dwfrm_billing_billingAddress_addressFields_states_state': self.stateID,
                    'dwfrm_billing_billingAddress_addressFields_country': self.profile["countryCode"],
                    'dwfrm_billing_couponCode': '',
                    'dwfrm_billing_paymentMethods_creditCard_encrypteddata': adyenEncrypted,
                    'dwfrm_billing_paymentMethods_creditCard_type': cType,
                    'dwfrm_adyPaydata_brandCode': '',
                    'noPaymentNeeded': True,
                    'dwfrm_billing_paymentMethods_creditCard_selectedCardID': '',
                    'dwfrm_billing_paymentMethods_selectedPaymentMethodID': 'CREDIT_CARD',
                    'dwfrm_billing_billingAddress_personalData': True,
                    'dwfrm_billing_billingAddress_tersmsOfSale': True,
                    'csrf_token': self.csrf,
                    'g-recaptcha-response':capToken
                }
            except Exception as e:
                self.error(f"Failed to construct card form ({e}). Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

            try:
                response = self.session.post('{}COBilling-Billing'.format(self.demandWareBase), data=payload, headers={
                    'accept-language': 'en-US,en;q=0.9',
                    'origin': self.baseUrl,
                    'referer':f'{self.baseUrl}/billing',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'x-requested-with': 'XMLHttpRequest',
                    'accept':'*/*',
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue
            
            if response.status_code in [200,302] and "orderNo" in str(response.url):
                try:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    self.termURL = soup.find('input',{'name':'TermUrl'})['value'] 
                    self.PaReq = soup.find('input',{'name':'PaReq'})['value'] 
                    self.MD = soup.find('input',{'name':'MD'})['value'] 

                    self.Dpayload = {
                        "TermUrl":self.termURL,
                        "PaReq":self.PaReq,
                        "MD":self.MD 
                    }

                except:
                    self.error("Failed to complete card checkout [failed to parse response]. Retrying...")
                    time.sleep(int(self.task["DELAY"]))
                    continue
                
                self.webhookData['size'] = self.size


                three_d_data = threeDSecure.solve(
                    self.session,
                    self.profile,
                    self.Dpayload,
                    self.webhookData,
                    self.taskID,
                    self.baseUrl
                )
                if three_d_data == False:
                    self.error("Checkout Failed (3DS Declined or Failed). Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue

                try:
                    response2 = self.session.post('{}Adyen-RedirectToTop?type=treedscontinue'.format(self.demandWareBase),headers={
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                        'content-type': 'application/x-www-form-urlencoded',
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'origin': 'https://verifiedbyvisa.acs.touchtechpayments.com',
                        'referer':'https://verifiedbyvisa.acs.touchtechpayments.com/v1/payerAuthentication',
                    }, data=three_d_data)
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    log.info(e)
                    self.error(f"error: {str(e)}")
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    continue

                if response2.status_code in [200,302]:
                    try:
                        response3 = self.session.post('{}Adyen-CloseIFrame'.format(self.demandWareBase),headers={
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                            'content-type': 'application/x-www-form-urlencoded',
                            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                            'origin': 'https://verifiedbyvisa.acs.touchtechpayments.com',
                            'referer':'https://verifiedbyvisa.acs.touchtechpayments.com/v1/payerAuthentication',
                        }, data={"dwfrm_redirecttotop_redirecttop":"Submit","MD":self.MD,"PaRes":three_d_data['PaRes'],"csrf_token":self.csrf})
                    except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                        log.info(e)
                        self.error(f"error: {str(e)}")
                        time.sleep(int(self.task["DELAY"]))
                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                        continue

                    
                    try:
                        response4 = self.session.post('{}orderconfirmed'.format(self.baseUrl),headers={
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                            'content-type': 'application/x-www-form-urlencoded',
                            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                            'referer':'{}Adyen-CloseIFrame'.format(self.demandWareBase),
                        }, data={"MD":None,"PaReq":None})
                    except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                        log.info(e)
                        self.error(f"error: {str(e)}")
                        time.sleep(int(self.task["DELAY"]))
                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                        continue
                    
                    if response4.status_code == 200 and "orderconfirmed" in response4.url or "riepilogoordine" in response4.url:
                        self.end = time.time() - self.start
                        self.webhookData['speed'] = self.end

                        self.success("Checkout Successful")
                        updateConsoleTitle(False,True,SITE)
                        return
                    
                    else:
                        self.error("Checkout Failed. Retrying...")
                        time.sleep(int(self.task['DELAY']))
                        continue
               
            
            else:
                self.error("Failed to complete card checkout. Retrying...")
                time.sleep(int(self.task["DELAY"]))
                continue
    
    def sendToDiscord(self):
        while True:
            
            self.webhookData['proxy'] = self.session.proxies

            sendNotification(SITE,self.webhookData['product'])

            try:
                Webhook.success(
                    webhook=loadSettings()["webhook"],
                    site=SITE,
                    url=self.webhookData['url'],
                    image=self.webhookData['image'],
                    title=self.webhookData['product'],
                    size=self.webhookData['size'],
                    price=self.webhookData['price'],
                    paymentMethod=self.task['PAYMENT'].strip().title(),
                    product=self.webhookData['product_url'],
                    profile=self.task["PROFILE"],
                    proxy=self.webhookData['proxy'],
                    speed=self.webhookData['speed']
                )
                self.secondary("Sent to discord!")
                while True:
                    pass
            except:
                self.alert("Failed to send webhook. Checkout here ==> {}".format(self.webhookData['url']))
                while True:
                    pass