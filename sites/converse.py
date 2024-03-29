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
from utils.akamai import AKAMAI
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
    footlocker_snare
)
import utils.config as CONFIG

_SITE_ = 'CONVERSE'
SITE = 'Converse'
class CONVERSE:
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

        self.profile = loadProfile(self.task["PROFILE"])
        if self.profile == None:
            self.error("Profile Not found. Exiting...")
            time.sleep(10)
            sys.exit()

        self.sizesplit = ''
        if   self.profile['countryCode'].upper() == 'GB':
            self.sizesplit = 'uk '
            self.baseUrl = 'https://www.converse.com/uk/en'
            self.base = 'https://www.converse.com/on/demandware.store/Sites-converse-gb-Site/en_GB/'
        elif self.profile['countryCode'].upper() == 'BE':
            self.baseUrl = 'https://www.converse.com/be/en'
            self.base = 'https://www.converse.com/on/demandware.store/Sites-converse-be-Site/en_BE/'
        elif self.profile['countryCode'].upper() == 'DK':
            self.baseUrl = 'https://www.converse.com/dk/en'
            self.base = 'https://www.converse.com/on/demandware.store/Sites-converse-eu-Site/en_DK/'
        elif self.profile['countryCode'].upper() == 'DE':
            self.baseUrl = 'https://www.converse.com/de/en'
            self.base = 'https://www.converse.com/on/demandware.store/Sites-converse-de-Site/de_DE/'
        elif self.profile['countryCode'].upper() == 'ES':
            self.baseUrl = 'https://www.converse.com/es/en'
            self.base = 'https://www.converse.com/on/demandware.store/Sites-converse-es-Site/es_ES/'
        elif self.profile['countryCode'].upper() == 'FI':
            self.baseUrl = 'https://www.converse.com/fi/en'
            self.base = 'https://www.converse.com/on/demandware.store/Sites-converse-eu-Site/en_FI/'
        elif self.profile['countryCode'].upper() == 'FR':
            self.baseUrl = 'https://www.converse.com/fr/en'
            self.base = 'https://www.converse.com/on/demandware.store/Sites-converse-fr-Site/fr_FR/'
        elif self.profile['countryCode'].upper() == 'IE':
            self.baseUrl = 'https://www.converse.com/ie/en'
            self.base = 'https://www.converse.com/on/demandware.store/Sites-converse-eu-Site/en_IE/'
        elif self.profile['countryCode'].upper() == 'IT':
            self.baseUrl = 'https://www.converse.com/it/en'
            self.base = 'https://www.converse.com/on/demandware.store/Sites-converse-it-Site/it_IT/'
        elif self.profile['countryCode'].upper() == 'LU':
            self.baseUrl = 'https://www.converse.com/lu/en'
            self.base = 'https://www.converse.com/on/demandware.store/Sites-converse-fr-Site/en_LU/'
        elif self.profile['countryCode'].upper() == 'NL':
            self.baseUrl = 'https://www.converse.com/nl/en'
            self.base = 'https://www.converse.com/on/demandware.store/Sites-converse-nl-Site/nl_NL/'
        elif self.profile['countryCode'].upper() == 'AT':
            self.baseUrl = 'https://www.converse.com/at/en'
            self.base = 'https://www.converse.com/on/demandware.store/Sites-converse-de-Site/de_AT/'
        elif self.profile['countryCode'].upper() == 'PT':
            self.baseUrl = 'https://www.converse.com/pt/en'
            self.base = 'https://www.converse.com/on/demandware.store/Sites-converse-es-Site/en_PT/'
        else:
            self.error('Region not supported. Exiting...')
            time.sleep(10)
            sys.exit()

        if 'https' not in self.task['PRODUCT']:
            self.prodUrl = '{}/regular/{}.html'.format(self.baseUrl,self.task['PRODUCT'])
        else:
            self.prodUrl = self.task['PRODUCT']


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
            "product_url":self.prodUrl
        }

        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)

        self.tasks()
    
    def tasks(self):
        self.cookie = AKAMAI.converse(self.session,self.taskID)
        while self.cookie['_abck'] == 'error':
            self.cookie = AKAMAI.converse(self.session,self.taskID)
            time.sleep(2)

        self.cookie = self.cookie['_abck']

        cookie_obj = requests.cookies.create_cookie(domain='.converse.com',name='_abck',value=self.cookie)
        self.session.cookies.set_cookie(cookie_obj)

        self.monitor()
        self.addToCart()
        self.shippingPage()
        self.shipping()
        self.billing()
        self.submit()
        self.paypal()


        self.sendToDiscord()

    def monitor(self):
        while True:
            self.prepare("Getting Product...")


            try:
                response = self.session.get(self.prodUrl,headers={
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue
            
            self.referer = response.url
            if response.status_code == 200:
                self.start = time.time()

                self.warning("Retrieved Product")

                try:
                    soup = BeautifulSoup(response.text, "html.parser")

                    self.webhookData['product'] = str(soup.find("span",{"class":"productName"}).text)
                    self.webhookData['image'] = str(soup.find("span",{"class":"productImageUrl"}).text)
                    self.webhookData['price'] = str(soup.find("span",{"class":"price-sales"}).text)
                    self.sku = str(soup.find("span",{"class":"productSKU"}).text)

                    foundSizes = soup.find('select',{'id':'variationDropdown-size'})

                    allSizes = []
                    sizes = []
                    for s in foundSizes:
                        try:
                            try:
                                size = s.text.split(' ')[1].strip()
                            except:
                                size = s.text.strip()

                            allSizes.append('{}:{}'.format(
                                size,
                                s['value'].split('_size=')[1].split('&')[0]
                            ))
                            
                            sizes.append(size)
                        except Exception as e:
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
                                    self.sizePID = '{}_{}'.format(self.sku,size.split(":")[1])
                                    
                                    self.warning(f"Found Size => {self.size}")
        
                    else:
                        selected = random.choice(allSizes)
                        self.size = selected.split(":")[0]
                        self.sizePID = '{}_{}'.format(self.sku,selected.split(":")[1])
                        
                        self.warning(f"Found Size => {self.size}")

                except Exception as e:
                    log.info(e)
                    self.error("Failed to parse product data (maybe OOS)")
                    time.sleep(int(self.task['DELAY']))
                    continue
                
                self.webhookData['size'] = self.size
                return

            elif response.status_code == 403:
                self.cookie = AKAMAI.converse(self.session,self.taskID)
                while self.cookie['_abck'] == 'error':
                    self.cookie = AKAMAI.converse(self.session,self.taskID)
                    time.sleep(2)
                    
                self.cookie = self.cookie['_abck']
                continue
                            
            else:
                self.error(f"Failed to get product [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def addToCart(self):
        while True:
            self.prepare("Adding to cart...")
            
            payload = {
                'Quantity': '1',
                'cartAction': 'add',
                'pid': self.sizePID
            }
            
            try:
                response = self.session.post('{}Cart-AddProduct?format=ajax'.format(self.base), data=payload, headers={
                    'accept-language': 'en-US,en;q=0.9',
                    'origin': 'https://www.converse.com',
                    'referer': self.referer,
                    'accept':'text/html, */*; q=0.01',
                    'x-requested-with': 'XMLHttpRequest',
                    'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue
            
            if response.status_code == 200 and 'subtotal' in response.text.lower():
                self.success("Added to cart!")
                updateConsoleTitle(True,False,SITE)
                return
                
            elif response.status_code == 403:
                self.cookie = AKAMAI.converse(self.session,self.taskID)
                while self.cookie['_abck'] == 'error':
                    self.cookie = AKAMAI.converse(self.session,self.taskID)
                    time.sleep(2)
                    
                self.cookie = self.cookie['_abck']
                continue
            
            else:
                self.error(f"Failed to cart [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def shippingPage(self):
        while True:
            self.prepare("Getting shipping...")

            try:
                response = self.session.get(f'{self.baseUrl}/checkout-shipping', headers={
                    'accept-language': 'en-US,en;q=0.9',
                    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
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

                    self.csrf = soup.find('input',{'name':'csrf_token'})['value']
                    self.shippingKey = soup.find('input',{'name':'dwfrm_singleshipping_securekey'})['value']
                    self.shippingMethod = soup.findAll('select',{'name':'regular-shipping-methods'})[0].find_all('option')[0]['value']
                    self.dwCont = response.text.split('checkout-shipping?dwcont=')[1].split('"')[0]
                except Exception:
                    self.error("Failed to get shipping [failed to parse response]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue
                

                self.warning('Got shipping')
                return

            elif response.status_code == 403:
                self.cookie = AKAMAI.converse(self.session,self.taskID)
                while self.cookie['_abck'] == 'error':
                    self.cookie = AKAMAI.converse(self.session,self.taskID)
                    time.sleep(2)
                    
                self.cookie = self.cookie['_abck']
                continue

            else:
                self.error(f"Failed to get shipping [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
            
    def shipping(self):
        while True:
            self.prepare("Submitting shipping...")
            
            try:
                payload = {
                    'dwfrm_singleshipping_shippingAddress_addressFields_common_firstName':self.profile['firstName'],
                    'dwfrm_singleshipping_shippingAddress_addressFields_common_lastName':self.profile['lastName'],
                    'dwfrm_singleshipping_shippingAddress_addressFields_common_address1':'{} {}'.format(self.profile['house'],self.profile['addressOne']),
                    'dwfrm_singleshipping_shippingAddress_addressFields_common_address2':self.profile['addressTwo'],
                    'dwfrm_singleshipping_shippingAddress_addressFields_common_city':self.profile['city'],
                    'dwfrm_singleshipping_shippingAddress_addressFields_regional_zip':self.profile['zip'],
                    'dwfrm_singleshipping_shippingAddress_addressFields_regional_phoneOpt':self.profile['phone'],
                    'areaCode':self.profile['phonePrefix'],
                    'regular-shipping-methods':self.shippingMethod,
                    'dwfrm_singleshipping_shippingAddress_giftmessageFields_giftMessage':'',
                    'dwfrm_singleshipping_shippingAddress_save':'Go to Payment',
                    'csrf_token':self.csrf,
                    'dwfrm_singleshipping_securekey':self.shippingKey
                }
            except Exception:
                self.error('Failed to submit shipping. [failed to construct form]. Retrying...')
                time.sleep(int(self.task['DELAY']))
                continue

            try:
                response = self.session.post(f'{self.baseUrl}/checkout-shipping?dwcont=' +self.dwCont, data=payload, headers={
                    'accept-language': 'en-US,en;q=0.9',
                    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'content-type':'application/x-www-form-urlencoded',
                    'referer': f'{self.baseUrl}/checkout-shipping',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
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
                    self.billingSecureKey = soup.find('input',{'name':'dwfrm_billing_securekey'})['value']
                except Exception:
                    self.error("Failed to submit shipping [failed to parse response]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue

                self.warning("Submitted shipping")
                return

            elif response.status_code == 403:
                self.cookie = AKAMAI.converse(self.session,self.taskID)
                while self.cookie['_abck'] == 'error':
                    self.cookie = AKAMAI.converse(self.session,self.taskID)
                    time.sleep(2)
                    
                self.cookie = self.cookie['_abck']
                continue
            
            else:
                self.error(f"Failed to submit shipping [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def billing(self):
        while True:
            self.prepare("Submitting billing...")
            try:
                payload = {
                    'dwfrm_billing_securekey': self.billingSecureKey,
                    'dwfrm_billing_paymentMethods_selectedPaymentMethodID': 'PAY_PAL',
                    'dwfrm_billing_paymentMethods_regionalpaymentfields_idealBankName': '',
                    'dwfrm_billing_paymentMethods_creditCard_type': 'Visa',
                    'dwfrm_billing_paymentMethods_creditCard_number': '',
                    'dwfrm_billing_paymentMethods_creditCard_month': '',
                    'dwfrm_billing_paymentMethods_creditCard_year': '',
                    'dwfrm_billing_paymentMethods_creditCard_cvn': '',
                    'dwfrm_billing_paymentMethods_bml_year': '',
                    'dwfrm_billing_paymentMethods_bml_month': '',
                    'dwfrm_billing_paymentMethods_bml_day': '',
                    'dwfrm_billing_paymentMethods_bml_ssn': '',
                    'dwfrm_billing_billingAddress_billingSameAsShipping': True,
                    'dwfrm_billing_billingAddress_addressFields_common_firstName': '',
                    'dwfrm_billing_billingAddress_addressFields_common_lastName': '',
                    'dwfrm_billing_billingAddress_addressFields_common_address1': '',
                    'dwfrm_billing_billingAddress_addressFields_common_address2': '',
                    'dwfrm_billing_billingAddress_addressFields_common_city': '',
                    'dwfrm_billing_billingAddress_addressFields_regional_zip': '',
                    'dwfrm_billing_billingAddress_addressFields_regional_phoneOpt': '',
                    'areaCode': self.profile['phonePrefix'],
                    'dwfrm_billing_billingAddress_email_emailAddress': self.profile['email'],
                    'dwfrm_billing_billingAddress_email_confirmationEmailAddress': self.profile['email'],
                    'csrf_token': self.csrf,
                    'dwfrm_billing_save': 'Review Order'
                }
            except Exception:
                self.error('Failed to submit billing. [failed to construct form]. Retrying...')
                time.sleep(int(self.task['DELAY']))
                continue
            
            try:
                response = self.session.post(f'{self.baseUrl}/checkout-shipping?dwcont=' +self.dwCont, data=payload, headers={
                    'accept-language': 'en-US,en;q=0.9',
                    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'content-type':'application/x-www-form-urlencoded',
                    'referer': f'{self.baseUrl}/checkout-shipping?dwcont='+self.dwCont,
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue
            
            if response.status_code in [200,302]:
                self.pp_referer = response.url
                self.warning("Submitted billing")
                return

            elif response.status_code == 403:
                self.cookie = AKAMAI.converse(self.session,self.taskID)
                while self.cookie['_abck'] == 'error':
                    self.cookie = AKAMAI.converse(self.session,self.taskID)
                    time.sleep(2)
                    
                self.cookie = self.cookie['_abck']
                continue

            else:
                self.error(f"Failed to submit billing [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def submit(self):
        while True:
            self.prepare('Submitting order...')
            try:
                payload = {
                    'csrf_token': self.csrf,
                    'sessionId': '',
                    'submit': 'Order Now'
                }
            except Exception:
                self.error('Failed to submit order. [failed to construct form]. Retrying...')
                time.sleep(int(self.task['DELAY']))
                continue

            try:
                response = self.session.post(f'{self.baseUrl}/checkout-confirmation',data=payload,headers={
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type':'application/x-www-form-urlencoded',
                    'referer': f'{self.baseUrl}/checkout-shipping?dwcont='+self.dwCont,
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue
            
            if response.status_code in [200,302]:
                self.warning('Submitted order')
                self.pp_referer = response.url
                return
            
            elif response.status_code == 403:
                self.cookie = AKAMAI.converse(self.session,self.taskID)
                while self.cookie['_abck'] == 'error':
                    self.cookie = AKAMAI.converse(self.session,self.taskID)
                    time.sleep(2)
                    
                self.cookie = self.cookie['_abck']
                continue
            
            else:
                self.error(f"Failed to submit order [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def paypal(self):
        while True:
            self.prepare('Getting paypal checkout...')

            try:
                response = self.session.get(self.pp_referer, headers={
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue
            
            if response.status_code == 200:
                self.end = time.time() - self.start
                self.webhookData['speed'] = self.end

                self.success("Got paypal checkout!")
                updateConsoleTitle(False,True,SITE)

                self.webhookData['url'] = storeCookies(
                    response.url,self.session,
                    self.webhookData['product'],
                    self.webhookData['image'],
                    self.webhookData['price'],
                    False
                )
                return
            
            elif response.status_code == 403:
                self.cookie = AKAMAI.converse(self.session,self.taskID)
                while self.cookie['_abck'] == 'error':
                    self.cookie = AKAMAI.converse(self.session,self.taskID)
                    time.sleep(2)
                    
                self.cookie = self.cookie['_abck']
                continue
            
            else:
                self.error(f"Failed to get paypal checkout [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
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
                    region=self.profile['countryCode'].lower(),
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