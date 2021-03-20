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
import uuid

from utils.captcha import captcha
from utils.logger import logger
from utils.webhook import Webhook
from utils.log import log
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
    randomString
)
import utils.config as config

SITE = 'SVD'
class SVD:
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

        self.tasks()
    
    def tasks(self):

        self.monitor()
        self.addToCart()
        self.jwt()
        self.checkoutData()
        self.shippingRates()
        self.shipping()

        if self.task['PAYMENT'].strip().lower() == "paypal":
            self.paypal()
        else:
            self.card()

        self.sendToDiscord()

    def monitor(self):
        while True:
            self.prepare("Getting Product...")

            try:
                url = '{}{}'.format(self.task["PRODUCT"],f"#%253F_={randomString(20)}")
                response = self.session.get(url)
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

                    self.webhookData['product'] = str(soup.find("span", {"class": "product-data__model"}).text)
                    self.webhookData['image'] = str(soup.find_all("img", {"class": "lazyload"})[0]["src"])
                    self.webhookData['price'] = str(soup.find("span", {"class": "price"}).text)

                    self.cartURL = soup.find("form", {"id": "product_addtocart_form"})["action"]
                    self.productID = soup.find("input", {"name": "item"})["value"]
                    self.formKey = soup.find("input", {"name": "form_key"})["value"]

                    cookie_obj = requests.cookies.create_cookie(domain='.www.sivasdescalzo.com', name='form_key', value=self.formKey)
                    self.session.cookies.set_cookie(cookie_obj)

                    regexSwatch = r'"jsonSwatchConfig":(.+)"}}'
                    regexAttributes = r'{"attributes":(.+)}}'
                    regexOption = r'"optionConfig":(.+)}}'

                    matches =  re.search(regexSwatch, response.text, re.MULTILINE)
                    matches2 = re.search(regexAttributes, response.text, re.MULTILINE)
                    matches3 = re.search(regexOption, response.text, re.MULTILINE)
                    if matches and matches2 and matches3:
                        jsonSwatch = json.loads('{' + matches.group() + '}')["jsonSwatchConfig"]
                        dict = list(jsonSwatch.keys())
                        self.SuperAttribute = dict[0]
                        jsonAttributes = json.loads(matches2.group())["attributes"]
        
                        option = json.loads('{' + matches3.group() + '}')["optionConfig"]
                        dict = list(option.keys())
                        self.option = dict[0]

                        allSizes = []
                        sizes = []
                        for s in jsonAttributes[self.SuperAttribute]["options"]:
                            try:
                                allSizes.append('{}:{}:{}'.format(
                                    s["label"], s["products"][0], s["id"]))
                                sizes.append(s["label"])
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
                                        self.option = size.split(":")[1]
                                        self.sizeID = size.split(':')[2]
                                        
                                        self.warning(f"Found Size => {self.size}")
            
                        else:
                            selected = random.choice(allSizes)
                            self.size = selected.split(":")[0]
                            self.option = selected.split(":")[1]
                            self.sizeID = selected.split(":")[2]
                            
                            self.warning(f"Found Size => {self.size}")

                        

                    else:
                        raise Exception
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
            
            try:
                form = {
                    "product": self.productID,
                    "selected_configurable_option": "",
                    "related_product": "",
                    "item": self.productID,
                    "form_key": self.formKey,
                    "global_size": "us",
                    f"super_attribute[{self.SuperAttribute}]": self.sizeID,
                    f"options[{self.option}]": f"{self.size} US",
                    "qty": 1
                }
            except:
                self.error("Failed to cart [error constructing cart form]")
                time.sleep(int(self.task["DELAY"]))
                continue

            

            try:
                response = self.session.post(self.cartURL, data=form, headers={
                    'accept': 'application/json, text/javascript, */*; q=0.01',
                    # 'cookie': f'form_key={self.formKey}',
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
                    data = response.json()
                except Exception as e:
                    log.info(e)
                    self.error("Failed to cart [failed to parse response]. Retrying...")
                    time.sleep(int(self.task["DELAY"]))
                    continue

                if data == []:
                    self.success("Added to cart!")
                    updateConsoleTitle(True,False,SITE)
                    return
                else:
                    self.error(f"Failed to cart. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue
            
            else:
                self.error(f"Failed to cart [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def jwt(self):
        while True:
            self.prepare("Getting fingerprint...")

            self.sessionId = str(uuid.uuid4())
            
            try:
                response = self.session.get(f'https://www.sivasdescalzo.com/en/customer/section/load/?sections=cart%2Cdirectory-data%2Cmessages&force_new_section_timestamp=true&_={int(time.time())}', headers={
                    'x-requested-with': 'XMLHttpRequest',
                    'accept': 'application/json, text/javascript, */*; q=0.01',
                })

            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if response.status_code == 200:

                try:
                    self.ClientToken = response.text.split("button.init('")[1].split("'")[0]
                    result = base64.b64decode(self.ClientToken)
                    self.bearerToken = json.loads(result.decode('Utf-8'))["authorizationFingerprint"]
                except Exception as e:
                    log.info(e)
                    self.error("Failed to get fingerprint [failed to parse response]. Retrying...")
                    time.sleep(int(self.task["DELAY"]))
                    continue

                try:
                    response2 = self.session.post('https://payments.braintree-api.com/graphql',json={
                        "clientSdkMetadata":
                        {
                            "source": "client",
                            "integration": "custom",
                            "sessionId": self.sessionId
                        },
                        "query": "query ClientConfiguration {   clientConfiguration {     analyticsUrl     environment     merchantId     assetsUrl     clientApiUrl     creditCard {       supportedCardBrands       challenges       threeDSecureEnabled       threeDSecure {         cardinalAuthenticationJWT       }     }     applePayWeb {       countryCode       currencyCode       merchantIdentifier       supportedCardBrands     }     googlePay {       displayName       supportedCardBrands       environment       googleAuthorization     }     ideal {       routeId       assetsUrl     }     kount {       merchantId     }     masterpass {       merchantCheckoutId       supportedCardBrands     }     paypal {       displayName       clientId       privacyUrl       userAgreementUrl       assetsUrl       environment       environmentNoNetwork       unvettedMerchant       braintreeClientId       billingAgreementsEnabled       merchantAccountId       currencyCode       payeeEmail     }     unionPay {       merchantAccountId     }     usBankAccount {       routeId       plaidPublicKey     }     venmo {       merchantId       accessToken       environment     }     visaCheckout {       apiKey       externalClientId       supportedCardBrands     }     braintreeApi {       accessToken       url     }     supportedFeatures   } }",
                        "operationName": "ClientConfiguration"
                    },headers={
                        'authorization': 'Bearer {}'.format(self.bearerToken),
                        'braintree-version': '2018-05-10',
                        'content-type': 'application/json',
                        'accept': '*/*',
                        'origin': 'https://www.sivasdescalzo.com',
                    })

                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    log.info(e)
                    self.error(f"error: {str(e)}")
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    continue

                if response2.status_code == 200:

                    try:
                        self.config = response2.json()["data"]["clientConfiguration"]["creditCard"]["threeDSecure"]
                    except Exception as e:
                        log.info(e)
                        self.error("Failed to get fingerprint [failed to parse response]. Retrying...")
                        time.sleep(int(self.task["DELAY"]))
                        continue


                    self.warning("Got fingerprint")
                    return

                else:
                    self.error(f"Failed to get fingerprint [{str(response.status_code)}]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue

            else:
                self.error(f"Failed to get fingerprint [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def checkoutData(self):
        while True:
            self.prepare("Getting checkout data...")

            try:
                response = self.session.get('https://www.sivasdescalzo.com/en/checkout/', headers={
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Language': 'en,en-GB;q=0.9',
                    'Cache-Control': 'no-cache',
                    'DNT': '1',
                    'Pragma': 'no-cache',
                    'Referer': self.task["PRODUCT"],
                })

            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if response.status_code == 200:
                
                try:
                    regex = r'{"entity_id":(.+"quoteItemData")'
                    regex2 = r'"region_id":(.{.+"types")'
                    matches = re.search(regex, response.text, re.MULTILINE)
                    matches2 = re.search(regex2, response.text, re.MULTILINE)

                    jsResponse = json.loads(matches.group()[:-16])
                    self.cartID = jsResponse["entity_id"]

                    regions = json.loads('{' + matches2.group()[:-10])["region_id"]

                    try:
                        for r in regions:
                            if r["title"].lower() == self.profile["region"].lower():
                                self.region = r["title"]
                                self.regionID = r["value"]
                            elif r["title"].lower() != self.profile["region"].lower():
                                self.regionID = ''
                                self.region = self.profile["region"]
                    except Exception as e:
                        log.info(e)
                        pass

                except Exception as e:
                    log.info(e)
                    self.error("Failed to get checkout data [failed to parse response]. Retrying...")
                    time.sleep(int(self.task["DELAY"]))
                    continue

                self.warning("Got checkout data")
                return
            else:
                self.error(f"Failed to get checkout data [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def shippingRates(self):
        while True:
            self.prepare("Getting shipping rates...")

            try:
                form = {
                    "address": {
                        "street": [self.profile["house"] + " " + self.profile["addressOne"], self.profile["addressTwo"]],
                        "city": self.profile["city"],
                        "region": self.profile["region"],
                        "country_id": self.profile["countryCode"],
                        "postcode": self.profile["zip"],
                        "firstname": self.profile["firstName"],
                        "lastname": self.profile["lastName"],
                        "telephone": self.profile["phone"],
                        "custom_attributes": [{"attribute_code": "taxvat", "value": ""}]
                    }
                }

                try:
                    if self.regionID and self.region:
                        form["region_id"] = self.regionID
                        form["region"] = self.region
                except:
                    pass
            except Exception as e:
                log.info(e)
                self.error("Failed to get shipping rates [failed to construct form]. Retrying...")
                time.sleep(int(self.task["DELAY"]))
                continue



            try:
                response = self.session.post(f'https://www.sivasdescalzo.com/en/rest/en/V1/guest-carts/{self.cartID}/estimate-shipping-methods',
                json=form,headers={
                    'accept': '*/*',
                    # 'cookie': f'form_key={self.formKey}'
                })

            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if response.status_code == 200:
                
                try:
                    self.rate = response.json()[0]["method_code"]
                    self.carrier_code = response.json()[0]["carrier_code"]
                except Exception as e:
                    log.info(e)
                    self.error("Failed to get shipping rates [failed to parse response]. Retrying...")
                    time.sleep(int(self.task["DELAY"]))
                    continue

                self.warning("Got shipping rates")
                return
            else:
                self.error(f"Failed to get shipping rates [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue


    def shipping(self):
        while True:
            self.prepare("Submitting shipping...")

            try:
                form = {
                        "addressInformation":
                        {
                            "shipping_address":
                            {
                                "countryId": self.profile["countryCode"],
                                "region": self.profile["region"],
                                "street": [self.profile["house"] + " " + self.profile["addressOne"], self.profile["addressTwo"]],
                                "telephone": self.profile["phone"],
                                "postcode": self.profile["zip"],
                                "city": self.profile["city"],
                                "firstname": self.profile["firstName"],
                                "lastname": self.profile["lastName"],
                                "customAttributes": [{"attribute_code": "taxvat", "value": ""}]
                            },
                            "billing_address":
                            {
                                "countryId": self.profile["countryCode"],
                                "region": self.profile["region"],
                                "street": [self.profile["house"] + " " + self.profile["addressOne"], self.profile["addressTwo"]],
                                "telephone": self.profile["phone"],
                                "postcode": self.profile["zip"],
                                "city": self.profile["city"],
                                "firstname": self.profile["firstName"],
                                "lastname": self.profile["lastName"],
                                "customAttributes": [{"attribute_code": "taxvat", "value": ""}],
                                "saveInAddressBook": None
                            },
                            "shipping_method_code": self.rate,
                            "shipping_carrier_code": self.carrier_code,
                            "extension_attributes": {}
                        }
                    }

                try:
                    if self.regionID and self.region:
                        form["addressInformation"]["shipping_address"]["regionId"] = self.regionID
                        form["addressInformation"]["shipping_address"]["regionCode"] = self.region
                except:
                    pass
            except Exception as e:
                log.info(e)
                self.error("Failed to submit shipping [failed to construct form]. Retrying...")
                time.sleep(int(self.task["DELAY"]))
                continue
            
        
                
            try:
                response = self.session.post(f'https://www.sivasdescalzo.com/en/rest/en/V1/guest-carts/{self.cartID}/shipping-information',
                json=form, headers={
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/json',
                    'origin': 'https://www.sivasdescalzo.com',
                    'referer': 'https://www.sivasdescalzo.com/en/checkout/',
                    'x-requested-with': 'XMLHttpRequest',
                    # 'cookie': f'form_key={self.formKey}'
                })

            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

        
            if response.status_code == 200:
                try:
                    self.price = response.json()["totals"]["grand_total"]
                except Exception as e:
                    log.info(e)
                    self.error(f"Failed to set shipping [failed to parse response]. Retrying...")
                    time.sleep(int(self.task["DELAY"]))
                    continue

                self.warning("Successfully set shipping")
                return

            else:
                self.error(f"Failed to set shipping [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    
    def paypal(self):
        while True:
            self.prepare("Getting paypal checkout...")
            sessionId = str(uuid.uuid4())

            try:
                form = {
                    "returnUrl": "https://www.paypal.com/checkoutnow/error",
                    "cancelUrl": "https://www.paypal.com/checkoutnow/error",
                    "offerPaypalCredit": False,
                    "experienceProfile": {"brandName": "SVD - sivasdescalzo", "localeCode": "en_US", "noShipping": "false", "addressOverride": True},
                    "amount": self.price,
                    "currencyIsoCode": "EUR",
                    "line1": self.profile["house"] + " " + self.profile["addressOne"],
                    "line2":self.profile["addressTwo"],
                    "city": self.profile["city"],
                    "state": self.profile["region"],
                    "postalCode": self.profile["zip"],
                    "countryCode": self.profile["countryCode"],
                    "phone": self.profile["phone"],
                    "recipientName": "{} {}".format(self.profile["firstName"], self.profile["lastName"]),
                    "braintreeLibraryVersion": "braintree/web/3.48.0",
                    "_meta": {"merchantAppId": "www.sivasdescalzo.com", "platform": "web", "sdkVersion": "3.48.0", "source": "client", "integration": "custom", "integrationType": "custom", "sessionId": sessionId},
                    "authorizationFingerprint": self.bearerToken
                }
            except Exception as e:
                log.info(e)
                self.error("Failed to submit shipping [failed to construct form]. Retrying...")
                time.sleep(int(self.task["DELAY"]))
                continue
            
            try:
                response = self.session.post('https://api.braintreegateway.com/merchants/7rgb8j8vb5f4hdwg/client_api/v1/paypal_hermes/create_payment_resource',
                json=form,headers={
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/json',
                    'Accept': '*/*',
                    'Origin': 'https://www.sivasdescalzo.com',
                })

            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if response.status_code in [200,201]:
                
                try:
                    paymentToken = response.json()['paymentResource']['paymentToken']
                    paypal = response.json()['paymentResource']['redirectUrl']
                    token = paypal.split("token=")[1]
                    checkoutUrl = "https://www.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token={}".format(token)
                except Exception as e:
                    log.info(e)
                    self.error(f"Failed to get paypal checkout [failed to parse response]. Retrying...")
                    time.sleep(int(self.task["DELAY"]))
                    continue

                self.end = time.time() - self.start
                self.webhookData['speed'] = self.end
                

                self.success("Got paypal checkout! (complete paypal checkout before closing venetiaCLI)")
                updateConsoleTitle(False,True,SITE)
                self.webhookData['url'] = storeCookies(
                    checkoutUrl,self.session,
                    self.webhookData['product'],
                    self.webhookData['image'],
                    self.webhookData['price']
                )
                self.sendToDiscord2()

                nonce = ''
                while nonce == '':
                    try:
                        data = {
                            "paypalAccount": {
                                "correlationId": token,
                                "options": { "validate": False },
                                "paymentToken": paymentToken,
                                "payerId": "",
                                "unilateral": False,
                                "intent": "authorize"
                            },
                            "braintreeLibraryVersion": "braintree/web/3.48.0",
                            "_meta": {
                                "merchantAppId": "www.sivasdescalzo.com",
                                "platform": "web",
                                "sdkVersion": "3.48.0",
                                "source": "client",
                                "integration": "custom",
                                "integrationType": "custom",
                                "sessionId": sessionId
                            },
                            "authorizationFingerprint": self.bearerToken
                        }

                        r1 = self.session.post("https://api.braintreegateway.com/merchants/7rgb8j8vb5f4hdwg/client_api/v1/payment_methods/paypal_accounts",headers={
                            "Host": "api.braintreegateway.com",
                            "Origin": "https://www.sivasdescalzo.com",
                            "Referer": "https://www.sivasdescalzo.com/en/checkout/",
                        }, json=data)

                        # r.json()['paypalAccounts'][0]['details']['payerInfo']['email']
                        
                        print(r1.json())
                        payerId = r1.json()['paypalAccounts'][0]['details']['payerInfo']['payerId']
                        data["payerId"] = payerId

                        r2 = self.session.post("https://api.braintreegateway.com/merchants/7rgb8j8vb5f4hdwg/client_api/v1/payment_methods/paypal_accounts",headers={
                            "Host": "api.braintreegateway.com",
                            "Origin": "https://www.sivasdescalzo.com",
                            "Referer": "https://www.sivasdescalzo.com/en/checkout/",
                        }, json=data)
                        nonce = r2.json()['paypalAccounts'][0]['nonce']
                    except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                        log.info(e)
                        self.error(f"error: {str(e)}")
                        time.sleep(int(self.task["DELAY"]))
                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                        continue

                try:
                    data = {
                        "cartId": self.cartID,
                        "billingAddress": {
                            "countryId": self.profile["countryCode"],
                            "regionCode": "",
                            "region": self.region,
                            "street": [self.profile["house"] + " " + self.profile["addressOne"] + " " + self.profile["addressTwo"]],
                            "telephone": self.profile["phone"],
                            "postcode": self.profile["zip"],
                            "city": self.profile["city"],
                            "firstname": self.profile["firstName"],
                            "lastname": self.profile["lastName"],
                            "customAttributes": [{ "attribute_code": "taxvat", "value": "" }],
                            "saveInAddressBook": None
                        },
                        "paymentMethod": {
                            "method": "braintree_paypal",
                            "additional_data": {
                            "payment_method_nonce": nonce,
                            "device_data": "{\"device_session_id\":\"\",\"fraud_merchant_id\":null}"
                            }
                        },
                        "email": self.profile["email"]
                    }

                    try:
                        if self.regionID:
                            data["regionId"] = self.regionID
                    except:
                        pass
                except Exception as e:
                    self.error("Failed to construct payload. Retrying...")
                    time.sleep(int(self.task["DELAY"]))
                    continue

                
                try:
                    response = self.session.post('https://www.sivasdescalzo.com/en/rest/en/V1/guest-carts/{}/payment-information'.format(self.cartID),
                    json=data,headers={
                        'Connection': 'keep-alive',
                        'Content-Type': 'application/json',
                        'Accept': '*/*',
                        'Origin': 'https://www.sivasdescalzo.com',
                    })

                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    log.info(e)
                    self.error(f"error: {str(e)}")
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    continue
                
                self.alert("Completed payal checkout")
                while True:
                    pass


                
            else:
                self.error(f"Failed to get paypal checkout [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    
    def card(self):
        while True:
            self.prepare("Completing card checkout...")
            return
    
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
                    size=self.size,
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

    def sendToDiscord2(self):
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
                    size=self.size,
                    price=self.webhookData['price'],
                    paymentMethod=self.task['PAYMENT'].strip().title(),
                    product=self.webhookData['product_url'],
                    profile=self.task["PROFILE"],
                    proxy=self.webhookData['proxy'],
                    speed=self.webhookData['speed']
                )
                self.secondary("Sent to discord!")
            except:
                self.alert("Failed to send webhook. Checkout here ==> {}".format(self.webhookData['url']))

            return
