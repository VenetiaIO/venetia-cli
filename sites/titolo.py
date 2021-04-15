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
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies, updateConsoleTitle, scraper)
import utils.config as config

_SITE_ = 'TITOLO'
SITE = 'Titolo'
class TITOLO:
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

        self.baseSite = 'https://www.titoloshop.com'

        try:
            split = self.task["PRODUCT"].split("titoloshop.")[1]
            self.reg = 'eu_en'
        except:
            self.reg = 'ch_en'


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

        self.tasks()
    
    def tasks(self):

        self.monitor()
        self.addToCart()
        self.method()
        self.getShippingMethod()
        self.shipping()
        self.paymentMethod()

        if self.task['PAYMENT'].strip().lower() == "visa" or self.task['PAYMENT'].strip().lower() == "mastercard" or self.task['PAYMENT'].strip().lower() == "card":
            self.placeOrder_cc()
        else:
            self.placeOrder_pp()

        self.sendToDiscord()

    def monitor(self):
        while True:
            self.prepare("Getting Product...")

            try:
                response = self.session.get(self.task["PRODUCT"])
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

                    self.webhookData['product'] = str(soup.find("meta",{"property":"og:image:alt"})["content"])
                    self.webhookData['image'] = str(soup.find("meta",{"property":"og:image"})["content"])
                    self.webhookData['price'] = str(soup.find("span",{"class":"price"}).text)

                    self.atcUrl = soup.find("form", {"id": "product_addtocart_form"})["action"].replace(',',',,')
                    self.formKey = soup.find("input", {"name": "form_key"})["value"]
                    self.productId = soup.find("input", {"name": "product_id"})["value"]
                    self.attributeId = response.text.split('{"attributes":{"')[1].split('"')[0]
                    sizeSelect = soup.find("div",{"id":"tab-size_eu"})

                    cookie_obj = requests.cookies.create_cookie(domain='.www.titoloshop.com', name='form_key', value=self.formKey)
                    self.session.cookies.set_cookie(cookie_obj)

                    allSizes = []
                    sizes = []
                    for s in sizeSelect:
                        try:
                            allSizes.append('{}:{}:{}'.format(s['option-label'],s["data-option-label"], s['data-option-id']))
                            sizes.append(s['option-label'])
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
                                    self.sizeValue = size.split(":")[1]
                                    self.optionId = size.split(':')[2]
                                    
                                    self.warning(f"Found Size => {self.size}")
        
                    else:
                        selected = random.choice(allSizes)
                        self.size = selected.split(":")[0]
                        self.sizeValue = selected.split(":")[1]
                        self.optionId = selected.split(":")[2]
                        
                        self.warning(f"Found Size => {self.size}")


                except Exception as e:
                    log.info(e)
                    self.error("Failed to parse product data (maybe OOS)")
                    time.sleep(int(self.task['DELAY']))
                    continue
                
                self.webhookData['size'] = self.size
                return
                    
            else:
                self.error(f"Failed to get product [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def addToCart(self):
        while True:
            self.prepare("Adding to cart...")
            
            boundary = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=16))
            payload = {
                'product': self.productId,
                'selected_configurable_option': '',
                'related_product': '',
                'item': self.productId,
                'form_key': self.formKey,
                f'super_attribute[{self.attributeId}]': self.optionId,
                'qty': '1',
                f'formatted_size_value[{self.attributeId}]': self.sizeValue
            }
            payload_encoded = MultipartEncoder(payload, boundary=f'----WebKitFormBoundary{boundary}')
            

            try:
                response = self.session.post(self.atcUrl, data=payload_encoded.to_string(), headers={
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': f'multipart/form-data; boundary=----WebKitFormBoundary{boundary}',
                    'referer': self.task["PRODUCT"],
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'x-requested-with': 'XMLHttpRequest',
                    'accept':'application/json, text/javascript, */*; q=0.01'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue


            try:
                response_data = response.json()
            except Exception as e:
                log.info(e)
                self.error("Failed to cart [failed to parse response]. Retrying...")
                time.sleep(int(self.task["DELAY"]))
                continue

            if response.status_code == 200 and response_data == []:
                self.success("Added to cart!")
                updateConsoleTitle(True,False,SITE)
                return
            
            else:
                self.error(f"Failed to cart [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def method(self):
        while True:
            self.prepare("Getting basket ID")
            
            try:
                response = self.session.get(f'{self.baseSite}/{self.reg}/checkout/',headers={
                    'referer': self.task['PRODUCT'],
                    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
                })

            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if response.status_code == 200:

                try:
                    self.sessionId = response.text.split('"quoteData":{"entity_id":"')[1].split('"')[0]
                except Exception as e:
                    log.info(e)
                    self.error("Failed to get basket ID [failed to parse response]. Retrying...")
                    time.sleep(int(self.task["DELAY"]))
                    continue

                self.warning("Got basket ID")
                return
            else:
                self.error(f"Failed to get basket ID [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def getShippingMethod(self):
        while True:
            self.prepare("Getting shipping method")

            try:
                payload = {
                    "address": {
                        "street": ["{} {}".format(self.profile["addressOne"], self.profile["addressTwo"]), self.profile["house"]],
                        "city": self.profile["city"],
                        "country_id": self.profile["countryCode"],
                        "postcode": self.profile["zip"],
                        "firstname": self.profile["firstName"],
                        "lastname": self.profile["lastName"],
                        "telephone": self.profile["phone"]
                    }
                }
            except Exception:
                self.error(f"Failed to get shipping method [Failed to construct payload]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
            
            try:
                response = self.session.post(f'{self.baseSite}/{self.reg}/rest/{self.reg}/V1/guest-carts/{self.sessionId}/estimate-shipping-methods',
                json=payload,headers={
                    "accept": "*/*",
                    "accept-language": "en-US,en;q=0.9",
                    "accept-encoding": "gzip, deflate, br",
                    "content-type": "application/json",
                    "referrer": f"{self.baseSite}/{self.reg}",
                    "x-requested-with": "XMLHttpRequest"
                })

            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if response.status_code == 200:
                try:
                    responseJson = response.json()
                except Exception as e:
                    log.info(e)
                    self.error("Failed to get shipping method [failed to parse response]. Retrying...")
                    time.sleep(int(self.task["DELAY"]))
                    continue

                if len(responseJson) > 0:
                    self.shippingMethod = responseJson[0]
                    self.warning("Got shipping method")
                    return
                else:
                    self.error(f"Failed to get shipping method [empty response]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue
            else:
                self.error(f"Failed to get shipping method [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def shipping(self):
        while True:
            self.prepare("Submitting shipping...")

            try:
                payload = {
                    "addressInformation": {
                        "shipping_address": {
                        "countryId": self.profile["countryCode"],
                        "street": ["{} {}".format(self.profile["addressOne"], self.profile["addressTwo"]), self.profile["house"]],
                        "telephone": self.profile["phone"],
                        "postcode": self.profile["zip"],
                        "city": self.profile["city"],
                        "firstname": self.profile["firstName"],
                        "lastname": self.profile["lastName"]
                        },
                        "billing_address": {
                        "countryId": self.profile["countryCode"],
                        "street": ["{} {}".format(self.profile["addressOne"], self.profile["addressTwo"]), self.profile["house"]],
                        "telephone": self.profile["phone"],
                        "postcode": self.profile["zip"],
                        "city": self.profile["city"],
                        "firstname": self.profile["firstName"],
                        "lastname": self.profile["lastName"],
                        "saveInAddressBook": None
                        },
                        "shipping_method_code": self.shippingMethod['method_code'],
                        "shipping_carrier_code": self.shippingMethod['carrier_code'],
                        "extension_attributes": {}
                    }
                }
            except Exception as e:
                self.error(f"Failed to construct shipping form ({e}). Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
                
            try:
                response = self.session.post(f'{self.baseSite}/{self.reg}/rest/{self.reg}/V1/guest-carts/{self.sessionId}/shipping-information',
                json=payload, headers={
                    "accept": "*/*",
                    "accept-language": "en-US,en;q=0.9",
                    "accept-encoding": "gzip, deflate, br",
                    "content-type": "application/json",
                    "referrer": f"{self.baseSite}/{self.reg}",
                    "x-requested-with": "XMLHttpRequest"
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

    def paymentMethod(self):
        while True:
            self.prepare("Setting payment method...")



            try:
                paymentM = "datatranscw_paypal"
                if self.task['PAYMENT'].strip().lower() == "visa" or self.task['PAYMENT'].strip().lower() == "mastercard" or self.task['PAYMENT'].strip().lower() == "card": paymentM = "datatranscw_creditcard"

                payload = {
                    "cartId": self.sessionId,
                    "billingAddress": {
                        "countryId": self.profile["countryCode"],
                        "street": ["{} {}".format(self.profile["addressOne"], self.profile["addressTwo"]), self.profile["house"]],
                        "telephone": self.profile["phone"],
                        "postcode": self.profile["zip"],
                        "city": self.profile["city"],
                        "firstname": self.profile["firstName"],
                        "lastname": self.profile["lastName"],
                        "saveInAddressBook": None
                    },
                    "paymentMethod": {
                        "method": paymentM,
                        "po_number": None,
                        "additional_data": {}
                    },
                    "email": self.profile['email']
                }
            except Exception as e:
                self.error(f"Failed to construct payment form ({e}). Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
            
            try:
                response = self.session.post(f'{self.baseSite}/{self.reg}/rest/{self.reg}/V1/guest-carts/{self.sessionId}/payment-information',
                json=payload, headers={
                    "accept": "*/*",
                    "accept-language": "en-US,en;q=0.9",
                    "accept-encoding": "gzip, deflate, br",
                    "content-type": "application/json",
                    "referrer": f"{self.baseSite}/{self.reg}",
                    "x-requested-with": "XMLHttpRequest"
                })

            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if response.status_code == 200:

                try:
                    self.orderId = response.json()
                except Exception:
                    self.error(f'Failed to set payment method [failed to parse response]. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.payment_method()

                self.warning("Set payment method")
    
                return
            else:
                self.error(f"Failed to set payment method [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def placeOrder_pp(self):
        while True:
            self.prepare("Getting paypal checkout...")

            try:
                payload = {
                    'orderId': self.orderId
                }
            except Exception:
                self.error(f"Failed to construct checkout form. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
            
            try:
                response = self.session.post(f'{self.baseSite}/{self.reg}/rest/{self.reg}/V1/guest-carts/{self.sessionId}/datatranscw/checkout/authorize',
                json=payload,headers={
                    "accept": "*/*",
                    "accept-language": "en-US,en;q=0.9",
                    "accept-encoding": "gzip, deflate, br",
                    "content-type": "application/json",
                    "referrer": f"{self.baseSite}/{self.reg}",
                    "x-requested-with": "XMLHttpRequest"
                })

            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if response.status_code == 200:
                try:
                    responseJson = response.json()
                    params = {
                        "uppModuleName": "Customweb Magento",
                        "uppModuleVersion": responseJson['java_script_callback_function'].split('\"data-upp-module-version\", \"')[1].split('\")')[0],
                        "merchantId": responseJson['java_script_callback_function'].split('\"data-merchant-id\", \"')[1].split('\")')[0],
                        "amount": responseJson['java_script_callback_function'].split('\"data-amount\", \"')[1].split('\")')[0],
                        "currency": responseJson['java_script_callback_function'].split('\"data-currency\", \"')[1].split('\")')[0],
                        "refno": responseJson['java_script_callback_function'].split('\"data-refno\", \"')[1].split('\")')[0],
                        "successUrl": responseJson['java_script_callback_function'].split('\"data-success-url\", \"')[1].split('\")')[0],
                        "errorUrl": responseJson['java_script_callback_function'].split('\"data-error-url\", \"')[1].split('\")')[0],
                        "cancelUrl": responseJson['java_script_callback_function'].split('\"data-cancel-url\", \"')[1].split('\")')[0],
                        "uppReturnMaskedCC": responseJson['java_script_callback_function'].split('\"data-upp-return-masked-c-c\", \"')[1].split('\")')[0],
                        "language": responseJson['java_script_callback_function'].split('\"data-language\", \"')[1].split('\")')[0],
                        "reqtype": responseJson['java_script_callback_function'].split('\"data-reqtype\", \"')[1].split('\")')[0],
                        "uppCustomerName": responseJson['java_script_callback_function'].split('\"data-upp-customer-name\", \"')[1].split('\")')[0],
                        "uppCustomerFirstName": responseJson['java_script_callback_function'].split('\"data-upp-customer-first-name\", \"')[1].split('\")')[0],
                        "uppCustomerLastName": responseJson['java_script_callback_function'].split('\"data-upp-customer-last-name\", \"')[1].split('\")')[0],
                        "uppCustomerStreet": responseJson['java_script_callback_function'].split('\"data-upp-customer-street\", \"')[1].split('\")')[0],
                        "uppCustomerCity": responseJson['java_script_callback_function'].split('\"data-upp-customer-city\", \"')[1].split('\")')[0],
                        "uppCustomerCountry": responseJson['java_script_callback_function'].split('\"data-upp-customer-country\", \"')[1].split('\")')[0],
                        "uppCustomerZipCode": responseJson['java_script_callback_function'].split('\"data-upp-customer-zip-code\", \"')[1].split('\")')[0],
                        "uppCustomerEmail": responseJson['java_script_callback_function'].split('\"data-upp-customer-email\", \"')[1].split('\")')[0],
                        "uppCustomerDetails": responseJson['java_script_callback_function'].split('\"data-upp-customer-details\", \"')[1].split('\")')[0],
                        "paymentmethod": responseJson['java_script_callback_function'].split('\"data-paymentmethod\", \"')[1].split('\")')[0],
                        "L_AMT0": responseJson['java_script_callback_function'].split('\"data--l_-a-m-t0\", \"')[1].split('\")')[0],
                        "L_TAXAMT0": responseJson['java_script_callback_function'].split('\"data--l_-t-a-x-a-m-t0\", \"')[1].split('\")')[0],
                        "L_NAME0": responseJson['java_script_callback_function'].split('\"data--l_-n-a-m-e0\", \"')[1].split('\")')[0],
                        "L_Number0": responseJson['java_script_callback_function'].split('\"data--l_-number0\", \"')[1].split('\")')[0],
                        "L_Desc0": responseJson['java_script_callback_function'].split('\"data--l_-desc0\", \"')[1].split('\")')[0],
                        "SHIPPINGAMT": responseJson['java_script_callback_function'].split('\"data--s-h-i-p-p-i-n-g-a-m-t\", \"')[1].split('\")')[0],
                        "ITEMAMT": responseJson['java_script_callback_function'].split('\"data--i-t-e-m-a-m-t\", \"')[1].split('\")')[0],
                        "TAXAMT": responseJson['java_script_callback_function'].split('\"data--t-a-x-a-m-t\", \"')[1].split('\")')[0],
                        "cwDataTransId": responseJson['java_script_callback_function'].split('\"data-cw-data-trans-id\", \"')[1].split('\")')[0],
                        "theme": responseJson['java_script_callback_function'].split('\"data-theme\", \"')[1].split('\")')[0],
                        "sign": responseJson['java_script_callback_function'].split('\"data-sign\", \"')[1].split('\")')[0],
                        "version": "2.0.0"
                    }
                except Exception:
                    self.error(f"Failed to get paypal checkout [failed to parse response]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue
                
                try:
                    response2 = self.session.get('https://pay.datatrans.com/upp/jsp/upStart.jsp',params=params,headers={
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "en-US,en;q=0.9",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "Content-Type": "application/x-www-form-urlencoded",
                    })

                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    log.info(e)
                    self.error(f"error: {str(e)}")
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    continue

                if response2.status_code == 200:
                    try:
                        trx = response2.text.split('name="datatransTrxId" value="')[1].split('"')[0]
                        payload = {
                            "datatransTrxId": trx,
                            "hiddenFrame": False,
                            "uppScreenWidth": 999,
                            "iframed": "",
                            "browserUserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
                            "browserJavaEnabled": False,
                            "browserLanguage": "en-US",
                            "browserColorDepth": 24,
                            "browserScreenHeight": 1440,
                            "browserScreenWidth": 2560,
                            "browserTZ": 0
                        }
                    except Exception:
                        self.error(f"Failed to get paypal checkout [failed to parse response]. Retrying...")
                        time.sleep(int(self.task['DELAY']))
                        continue

                    try:
                        response3 = self.session.post('https://pay.datatrans.com/upp/jsp/upStart_1.jsp',data=payload,headers={
                            "Accept-Encoding": "gzip, deflate, br",
                            "Accept-Language": "en-US,en;q=0.9",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                            "Content-Type": "application/x-www-form-urlencoded",
                            "Referer":response2.url,
                            "Host": "pay.datatrans.com",
                            "Origin": "https://pay.datatrans.com"
                        })

                    except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                        log.info(e)
                        self.error(f"error: {str(e)}")
                        time.sleep(int(self.task["DELAY"]))
                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                        continue

                    if response3.status_code == 200:

                        try:
                            ec = response3.text.split("name='token' value='")[1].split("'")[0]
                            ppurl = f'https://www.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token={ec}&useraction=commit'
                        except Exception:
                            self.error(f"Failed to get paypal checkout [failed to parse response]. Retrying...")
                            time.sleep(int(self.task['DELAY']))
                            continue

                        self.end = time.time() - self.start
                        self.webhookData['speed'] = self.end

                        self.success("Got paypal checkout!")
                        updateConsoleTitle(False,True,SITE)

                        self.webhookData['url'] = storeCookies(
                            ppurl,self.session,
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

                
            else:
                self.error(f"Failed to get paypal checkout [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    
    def placeOrder_cc(self):
        while True:
            self.prepare("Getting card checkout...")

            try:
                val = ""
                if self.task['PAYMENT'].strip().lower() == "visa": val = "VIS"
                else: val = "ECA"

                payload = {
                    'orderId': self.orderId,
                    "formValues":[{"key":"pmethod","value":val}]
                }
            except Exception:
                self.error(f"Failed to construct checkout form. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
            
            try:
                response = self.session.post(f'{self.baseSite}/{self.reg}/rest/{self.reg}/V1/guest-carts/{self.sessionId}/datatranscw/checkout/authorize',
                json=payload,headers={
                    "accept": "*/*",
                    "accept-language": "en-US,en;q=0.9",
                    "accept-encoding": "gzip, deflate, br",
                    "content-type": "application/json",
                    "referrer": f"{self.baseSite}/{self.reg}",
                    "x-requested-with": "XMLHttpRequest"
                })

            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if response.status_code == 200:

                try:
                    responseJson = response.json()
                    params = {
                        "uppModuleName": responseJson['hidden_form_fields'][0]['value'],
                        "uppModuleVersion": responseJson['hidden_form_fields'][1]['value'],
                        "merchantId": responseJson['hidden_form_fields'][2]['value'],
                        "amount": responseJson['hidden_form_fields'][3]['value'],
                        "currency": responseJson['hidden_form_fields'][4]['value'],
                        "refno": responseJson['hidden_form_fields'][5]['value'],
                        "successUrl": responseJson['hidden_form_fields'][6]['value'],
                        "errorUrl": responseJson['hidden_form_fields'][7]['value'],
                        "cancelUrl": responseJson['hidden_form_fields'][8]['value'],
                        "uppReturnMaskedCC": responseJson['hidden_form_fields'][9]['value'],
                        "language": responseJson['hidden_form_fields'][10]['value'],
                        "reqtype": responseJson['hidden_form_fields'][11]['value'],
                        "uppCustomerName": responseJson['hidden_form_fields'][12]['value'],
                        "uppCustomerFirstName": responseJson['hidden_form_fields'][13]['value'],
                        "uppCustomerLastName": responseJson['hidden_form_fields'][14]['value'],
                        "uppCustomerStreet": responseJson['hidden_form_fields'][15]['value'],
                        "uppCustomerCity": responseJson['hidden_form_fields'][16]['value'],
                        "uppCustomerCountry": responseJson['hidden_form_fields'][17]['value'],
                        "uppCustomerZipCode": responseJson['hidden_form_fields'][18]['value'],
                        "uppCustomerEmail": responseJson['hidden_form_fields'][19]['value'],
                        "uppCustomerDetails": responseJson['hidden_form_fields'][20]['value'],
                        "paymentmethod": responseJson['hidden_form_fields'][21]['value'],
                        "cwDataTransId": responseJson['hidden_form_fields'][22]['value'],
                        "theme":responseJson['hidden_form_fields'][23]['value'],
                        "sign": responseJson['hidden_form_fields'][24]['value'],
                        "version": "2.0.0"
                    }
                except Exception:
                    self.error(f"Failed to get card checkout [failed to parse response]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue
                
                try:
                    response2 = self.session.get('https://pay.datatrans.com/upp/jsp/upStart.jsp',params=params,headers={
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "en-US,en;q=0.9",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "Content-Type": "application/x-www-form-urlencoded",
                    })

                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    log.info(e)
                    self.error(f"error: {str(e)}")
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    continue

                if response2.status_code == 200:

                    self.end = time.time() - self.start
                    self.webhookData['speed'] = self.end

                    self.success("Got card checkout!")
                    updateConsoleTitle(False,True,SITE)

                    self.webhookData['url'] = storeCookies(
                        response2.url,self.session,
                        self.webhookData['product'],
                        self.webhookData['image'],
                        self.webhookData['price'],
                        False
                    )
                    return
                
                else:
                    self.error(f"Failed to get card checkout [{str(response.status_code)}]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue

                
            else:
                self.error(f"Failed to get card checkout [{str(response.status_code)}]. Retrying...")
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