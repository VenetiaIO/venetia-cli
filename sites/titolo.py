import requests
from bs4 import BeautifulSoup
import datetime
import threading
import random
import sys
import time
import re
import json
import base64
import string
import cloudscraper
from urllib3.exceptions import HTTPError
import csv
from requests_toolbelt import MultipartEncoder
SITE = 'TITOLO'

from utils.logger import logger
from utils.captcha import captcha
from utils.webhook import discord
from utils.log import log
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies, updateConsoleTitle, scraper)

class TITOLO:
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
                csvFile.close()
            time.sleep(2)

    def __init__(self,task,taskName,rowNumber):
        self.task = task
        self.taskID = taskName

        twoCap = loadSettings()["2Captcha"]
        self.session = scraper()
        self.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
        self.session.proxies = self.proxies
        self.rowNumber = rowNumber

        threading.Thread(target=self.task_checker,daemon=True).start()
        self.collect()

    def collect(self):
        while True:
            logger.prepare(SITE,self.taskID,'Getting product page...')
            try:
                retrieve = self.session.get(self.task["PRODUCT"],headers={
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if retrieve.status_code == 200:
                self.start = time.time()
                logger.warning(SITE,self.taskID,'Got product page')
                self.baseSite = 'https://www.titoloshop.com'

                try:
                    split = self.task["PRODUCT"].split("titoloshop.")[1]
                    self.reg = 'eu_en'
                except:
                    self.reg = 'ch_en'


                try:
                    logger.prepare(SITE,self.taskID,'Getting product data...')

                    soup = BeautifulSoup(retrieve.text,"html.parser")
                    self.productTitle = soup.find("meta",{"property":"og:image:alt"})["content"]
                    self.productImage = soup.find("meta",{"property":"og:image"})["content"]
                    self.productPrice = soup.find("span",{"class":"price"}).text
                    self.atcUrl = soup.find("form", {"id": "product_addtocart_form"})["action"].replace(',',',,')
                    self.formKey = soup.find("input", {"name": "form_key"})["value"]
                    self.productId = soup.find("input", {"name": "product_id"})["value"]
                    # self.attributeIdColor = soup.find_all("select", {"class": "required-entry super-attribute-select"})[0]["id"].split("attribute")[1]
                    self.attributeId = retrieve.text.split('{"attributes":{"')[1].split('"')[0]
                    sizeSelect = soup.find("div",{"id":"tab-size_eu"})

                    cookie_obj = requests.cookies.create_cookie(domain='.www.titoloshop.com', name='form_key', value=self.formKey)
                    self.session.cookies.set_cookie(cookie_obj)
        
                    # regex = r"{\"attributes\":(.*?)}}\)"
                    # matches = re.search(regex, retrieve.text, re.MULTILINE)
                    # if matches:
                    #     productData = json.loads(
                    #         matches.group()[:-1])["attributes"][self.attributeIdColor]
                    #     self.color = productData["options"][0]["id"]
        
                    allSizes = []
                    sizes = []
                    for s in sizeSelect:
                        try:
                            allSizes.append('{}:{}:{}'.format(s['option-label'],s["data-option-label"], s['data-option-id']))
                            sizes.append(s['option-label'])
                        except:
                            pass
                    
                    if len(sizes) == 0:
                        logger.error(SITE,self.taskID,'Size Not Found')
                        time.sleep(int(self.task["DELAY"]))
                        continue
        
                    if self.task["SIZE"].lower() == "random":
                        chosen = random.choice(allSizes)
                        self.size = chosen.split(':')[0]
                        self.sizeValue = chosen.split(':')[1]
                        self.optionId = chosen.split(':')[2]
                        logger.warning(SITE,self.taskID,f'Found Size => {self.size}')
                    
            
                    else:
                        if self.task["SIZE"] not in sizes:
                            logger.error(SITE,self.taskID,'Size Not Found')
                            time.sleep(int(self.task["DELAY"]))
                            continue
                        for size in allSizes:
                            if self.task["SIZE"] == size.split(':')[0]:
                                self.size = size.split(':')[0]
                                self.sizeValue = size.split(':')[1]
                                self.optionId = size.split(':')[2]
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
        # captchaResponse = loadToken(SITE)
        # if captchaResponse == "empty":
        #     captchaResponse = captcha.v2('6Ldpi-gUAAAAANpo2mKVvIR6u8nUGrInKKik8MME',self.task["PRODUCT"],self.proxies,SITE,self.taskID)
    
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
            postCart = self.session.post(self.atcUrl,data=payload_encoded.to_string(),headers={
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-language": "en-US,en;q=0.9",
                "content-type": f"multipart/form-data; boundary=----WebKitFormBoundary{boundary}",
                "sec-ch-ua": "\"Google Chrome\";v=\"89\", \"Chromium\";v=\"89\", \";Not A Brand\";v=\"99\"",
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-requested-with": "XMLHttpRequest",
                "referrer":self.task['PRODUCT']
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()
        

        try:
            response = postCart.json()
        except:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()



        if postCart.status_code == 200 and response == []:
            updateConsoleTitle(True,False,SITE)
            logger.warning(SITE,self.taskID,'Successfully carted')
            self.method()
        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            if self.task['SIZE'].lower() == "random":
                self.collect()
            else:
                time.sleep(int(self.task["DELAY"]))
                self.addToCart()

    def method(self):
        logger.prepare(SITE,self.taskID,'Getting session...')
        try:
            setMethod = self.session.get(f'{self.baseSite}/{self.reg}/checkout/',headers={
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'referer': self.task['PRODUCT'],
            })

        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.method()

        try:
            self.sessionId = setMethod.text.split('"quoteData":{"entity_id":"')[1].split('"')[0]
        except Exception as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Failed to initiate session. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.method()


        if setMethod.status_code == 200:
            logger.warning(SITE,self.taskID,'Got session')
            self.estimate()
        else:
            logger.error(SITE,self.taskID,'Failed to initiate session. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.method()


    def estimate(self):
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()

        logger.prepare(SITE,self.taskID,'Getting shipping methods...')

        payload = {
            "address": {
                "street": ["{} {}".format(profile["addressOne"], profile["addressTwo"]), profile["house"]],
                "city": profile["city"],
                "country_id": profile["countryCode"],
                "postcode": profile["zip"],
                "firstname": profile["firstName"],
                "lastname": profile["lastName"],
                "telephone": profile["phone"]
            }
        }

        try:
            response = self.session.post(f'{self.baseSite}/{self.reg}/rest/{self.reg}/V1/guest-carts/{self.sessionId}/estimate-shipping-methods',json=payload,headers={
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "content-type": "application/json",
                "referrer": f"{self.baseSite}/{self.reg}",
                "x-requested-with": "XMLHttpRequest"
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.estimate()

        try:
            responseJson = response.json()
        except:
            logger.error(SITE,self.taskID,'Failed to get shipping method. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.estimate()

        if response.status_code == 200 and len(responseJson) > 0:
            self.shippingMethod = responseJson[0]
            logger.warning(SITE,self.taskID,'Got shipping method')
            self.billing()

        else:
            logger.error(SITE,self.taskID,'Failed to get shipping method. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.estimate()

    def billing(self):
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        logger.prepare(SITE,self.taskID,'Submitting billing...')

        payload = {
            "addressInformation": {
                "shipping_address": {
                "countryId": profile["countryCode"],
                "street": ["{} {}".format(profile["addressOne"], profile["addressTwo"]), profile["house"]],
                "telephone": profile["phone"],
                "postcode": profile["zip"],
                "city": profile["city"],
                "firstname": profile["firstName"],
                "lastname": profile["lastName"]
                },
                "billing_address": {
                "countryId": profile["countryCode"],
                "street": ["{} {}".format(profile["addressOne"], profile["addressTwo"]), profile["house"]],
                "telephone": profile["phone"],
                "postcode": profile["zip"],
                "city": profile["city"],
                "firstname": profile["firstName"],
                "lastname": profile["lastName"],
                "saveInAddressBook": None
                },
                "shipping_method_code": self.shippingMethod['method_code'],
                "shipping_carrier_code": self.shippingMethod['carrier_code'],
                "extension_attributes": {}
            }
        }

        try:
            postBilling = self.session.post(f'{self.baseSite}/{self.reg}/rest/{self.reg}/V1/guest-carts/{self.sessionId}/shipping-information',json=payload,headers={
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "content-type": "application/json",
                "referrer": f"{self.baseSite}/{self.reg}",
                "x-requested-with": "XMLHttpRequest"
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.billing()


        if postBilling.status_code == 200:
            logger.warning(SITE,self.taskID,'Successfully set shipping')
            self.payment_method()

        elif postBilling.status_code != 200:
            logger.error(SITE,self.taskID,'Failed to set shipping. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.billing()


    def payment_method(self):
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()

        logger.prepare(SITE,self.taskID,'Setting payment method...')

        paymentM = "datatranscw_paypal"
        if self.task['PAYMENT'].lower() == "visa" or self.task['PAYMENT'].lower() == "mastercard": paymentM = "datatranscw_creditcard"
        
        payload = {
            "cartId": self.sessionId,
            "billingAddress": {
                "countryId": profile["countryCode"],
                "street": ["{} {}".format(profile["addressOne"], profile["addressTwo"]), profile["house"]],
                "telephone": profile["phone"],
                "postcode": profile["zip"],
                "city": profile["city"],
                "firstname": profile["firstName"],
                "lastname": profile["lastName"],
                "saveInAddressBook": None
            },
            "paymentMethod": {
                "method": paymentM,
                "po_number": None,
                "additional_data": {}
            },
            "email": profile['email']
        }

        
        try:
            postPayment = self.session.post(f'{self.baseSite}/{self.reg}/rest/{self.reg}/V1/guest-carts/{self.sessionId}/payment-information',json=payload,headers={
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "content-type": "application/json",
                "referrer": f"{self.baseSite}/{self.reg}",
                "x-requested-with": "XMLHttpRequest"
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.payment_method()


        if postPayment.status_code == 200:
            try:
                self.orderId = postPayment.json()
            except Exception:
                logger.error(SITE,self.taskID,f'Failed to set payment Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.payment_method()

            logger.warning(SITE,self.taskID,'Successfully set payment method')
            if self.task['PAYMENT'].lower() == "visa" or self.task['PAYMENT'].lower() == "mastercard": self.placeOrder_cc()
            else: self.placeOrder_pp()

            
        else:
            try:
                responseJson = postPayment.json()
                message = responseJson['message']
            except:
                message = "n/a"
            logger.error(SITE,self.taskID,f'Failed to set payment [{message}]. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.payment_method()


    def placeOrder_pp(self):
        logger.info(SITE,self.taskID,'Starting [PAYPAL] checkout...')
        logger.prepare(SITE,self.taskID,'Getting paypal link...')
            
        payload = {
            'orderId': self.orderId
        }

        try:
            place = self.session.post(f'{self.baseSite}/{self.reg}/rest/{self.reg}/V1/guest-carts/{self.sessionId}/datatranscw/checkout/authorize',json=payload,headers={
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "content-type": "application/json",
                "referrer": f"{self.baseSite}/{self.reg}",
                "x-requested-with": "XMLHttpRequest"
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.placeOrder_pp()


        try:
            responseJson = place.json()
        except:
            logger.error(SITE,self.taskID,'Failed to get paypal link. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.placeOrder_pp()

        if place.status_code == 200:
            # trx = responseJson['java_script_callback_function'].split('\"data-sign\", \"')[1].split('\")')[0]
            try:
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
                logger.error(SITE,self.taskID,'Failed to get paypal redirect. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.placeOrder_pp()


    

            try:
                pp_ = self.session.get('https://pay.datatrans.com/upp/jsp/upStart.jsp',params=params,headers={
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Content-Type": "application/x-www-form-urlencoded",
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.placeOrder_pp()
            
            try:
                trx = pp_.text.split('name="datatransTrxId" value="')[1].split('"')[0]
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
                logger.error(SITE,self.taskID,'Failed to get paypal redirect. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.placeOrder_pp()

            try:
                pp = self.session.post('https://pay.datatrans.com/upp/jsp/upStart_1.jsp',data=payload,headers={
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Referer":pp_.url,
                    "Host": "pay.datatrans.com",
                    "Origin": "https://pay.datatrans.com"
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.placeOrder_pp()

            if pp.status_code == 200:
                self.end = time.time() - self.start
                try:
                    ec = pp.text.split("name='token' value='")[1].split("'")[0]
                except Exception:
                    logger.error(SITE,self.taskID,'Failed to get paypal redirect. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.placeOrder_pp()


                ppurl = f'https://www.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token={ec}&useraction=commit'

                logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')
                url = storeCookies(ppurl,self.session, self.productTitle, self.productImage, self.productPrice)
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
            logger.error(SITE,self.taskID,'Failed to get paypal redirect. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.placeOrder_pp()


    def placeOrder_cc(self):
        logger.info(SITE,self.taskID,'Starting [CARD] checkout...')
        logger.prepare(SITE,self.taskID,'Getting checkout link...')
            
        val = ""
        if self.task['PAYMENT'].lower() == "visa": val = "VIS"
        else: val = "ECA"

        payload = {
            "orderId": self.orderId,
            "formValues":[{"key":"pmethod","value":"VIS"}]
        }

        try:
            place = self.session.post(f'{self.baseSite}/{self.reg}/rest/{self.reg}/V1/guest-carts/{self.sessionId}/datatranscw/checkout/authorize',json=payload,headers={
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "content-type": "application/json",
                "referrer": f"{self.baseSite}/{self.reg}",
                "x-requested-with": "XMLHttpRequest"
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.placeOrder_cc()


        try:
            responseJson = place.json()
        except:
            logger.error(SITE,self.taskID,'Failed to get checkout link. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.placeOrder_cc()

        if place.status_code == 200:

            try:
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
            except Exception as e:
                logger.error(SITE,self.taskID,'Failed to get checkout link. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.placeOrder_cc()


    

            try:
                cc_ = self.session.get('https://pay.datatrans.com/upp/jsp/upStart.jsp',params=params,headers={
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Content-Type": "application/x-www-form-urlencoded",
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.placeOrder_cc()
            
            try:
                trx = cc_.text.split('name="datatransTrxId" value="')[1].split('"')[0]
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
            except Exception as e:
                logger.error(SITE,self.taskID,'Failed to get checkout link. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.placeOrder_cc()

            if cc_.status_code == 200:
                self.end = time.time() - self.start

                url_ = cc_.url

                logger.alert(SITE,self.taskID,'Sending Card checkout to Discord!')
                url = storeCookies(url_,self.session, self.productTitle, self.productImage, self.productPrice)
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
                        paymentMethod='Card',
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
            logger.error(SITE,self.taskID,'Failed to get checkout link. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.placeOrder_cc()



    
        

