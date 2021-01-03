import requests
from bs4 import BeautifulSoup
import datetime
import threading
import random
import sys
import time
import re
import json
import uuid
import os
import base64
import cloudscraper
import string
from urllib3.exceptions import HTTPError


from utils.logger import logger
from utils.webhook import discord
from utils.log import log
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies, updateConsoleTitle, scraper)

SITE = 'GROSBASKET'

class GROSBASKET:
    def __init__(self, task,taskName):
        self.taskID = taskName
        self.task = task
        self.sess = requests.session()

        twoCap = loadSettings()["2Captcha"]
        self.session = scraper()

        self.userAgent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1'

        self.session.headers.update({
            'User-Agent':self.userAgent
        })
        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
        self.collect()



    def collect(self):
        logger.prepare(SITE,self.taskID,'Getting product page...')
        try:
            retrieve = self.session.get(self.task["PRODUCT"], headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.collect()

        split = self.task["PRODUCT"].split("grosbasket.com/")[1]
        self.region = split.split('/')[0]
        if retrieve.status_code == 200:
            self.start = time.time()
            logger.success(SITE,self.taskID,'Got product page')
            try:
                soup = BeautifulSoup(retrieve.text, "html.parser")
                self.productTitle = soup.find("h1", {"itemprop": "name"}).text.replace('\n','')
                self.productImage = soup.find("img", {"class": "lazy"})["src"]
                self.attributeId = soup.find("select", {
                    "class": "required-entry super-attribute-select"})["id"].split("attribute")[1]
    
                regex = r"{\"attributes\":(.*?)}}\)"
                regex2 = r"{\"send_url\":(.*?)}\)"
                matches = re.search(regex, retrieve.text, re.MULTILINE)
                matches2 = re.search(regex2, retrieve.text, re.MULTILINE)
                if matches:
                    productData = json.loads(
                        matches.group()[:-1])["attributes"][self.attributeId]
    
                    productData2 = json.loads(matches2.group()[:-1])
                    self.currentCategory = productData2["current_category"]
                    self.formKey = productData2["form_key"]
                    self.productId = productData2["product_id"]
                    self.atcUrl = productData2["send_url"]
    
                    allSizes = []
                    sizes = []
                    for s in productData["options"]:
                        allSizes.append('{}:{}:{}'.format(
                            s["label"], s["products"][0], s["id"]))
                        sizes.append(s["label"])
    

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
                            for size in allSizes:
                                if size.split(':')[0] == self.task["SIZE"]:
                                    self.size = size.split(':')[0]
                                    self.sizeID = size.split(':')[2]
                                    self.option = size.split(":")[1]
                                    logger.success(SITE,self.taskID,f'Found Size => {self.size}')
    
                    elif self.task["SIZE"].lower() == "random":
                        selected = random.choice(allSizes)
                        self.size = selected.split(":")[0]
                        self.sizeID = selected.split(":")[2]
                        self.option = selected.split(":")[1]
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
            'product_id': self.productId,
            'form_key': self.formKey,
            'product': self.productId,
            'related_product': '',
            f'super_attribute[{self.attributeId}]': self.sizeID,
            'qty': 1,
            'IsProductView': 1,
            'current_category': self.currentCategory
        }
        try:
            postCart = self.session.post(self.atcUrl, data=payload,headers={
                'authority': 'www.grosbasket.com',
                'accept-language': 'en-US,en;q=0.9',
                'origin': 'https://www.grosbasket.com',
                'referer': self.task["PRODUCT"],
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()

        if postCart.status_code == 200 and postCart.json()["is_add_to_cart"] == "1":
            updateConsoleTitle(True,False,SITE)
            logger.success(SITE,self.taskID,'Successfully carted')
            self.clientToken()
        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

    def clientToken(self):
        self.sessionId = str(uuid.uuid4())
        try:
            tokenRequest = self.session.get(f'https://www.grosbasket.com/{self.region}/braintree/checkout/clientToken/',headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.clientToken()

        if tokenRequest.status_code == 200 and tokenRequest.json()["success"] == True:
            logger.success(SITE,self.taskID,'Successfully retrieved token')
            result = base64.b64decode(tokenRequest.json()["client_token"])
            self.fingerprint = json.loads(result.decode(
                'Utf-8'))["authorizationFingerprint"]


            braintreeHeaders = {
                'authority': 'payments.braintree-api.com',
                'authorization': 'Bearer {}'.format(self.fingerprint),
                'sec-fetch-dest': 'empty',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                'braintree-version': '2018-05-10',
                'content-type': 'application/json',
                'accept': '*/*',
                'origin': 'https://www.grosbasket.com',
                'sec-fetch-site': 'cross-site',
                'sec-fetch-mode': 'cors',
            }
    
            braintreeData = {
                "clientSdkMetadata":
                {
                    "source": "client",
                    "integration": "custom",
                    "sessionId": self.sessionId
                },
                "query": "query ClientConfiguration {   clientConfiguration {     analyticsUrl     environment     merchantId     assetsUrl     clientApiUrl     creditCard {       supportedCardBrands       challenges       threeDSecureEnabled       threeDSecure {         cardinalAuthenticationJWT       }     }     applePayWeb {       countryCode       currencyCode       merchantIdentifier       supportedCardBrands     }     googlePay {       displayName       supportedCardBrands       environment       googleAuthorization     }     ideal {       routeId       assetsUrl     }     kount {       merchantId     }     masterpass {       merchantCheckoutId       supportedCardBrands     }     paypal {       displayName       clientId       privacyUrl       userAgreementUrl       assetsUrl       environment       environmentNoNetwork       unvettedMerchant       braintreeClientId       billingAgreementsEnabled       merchantAccountId       currencyCode       payeeEmail     }     unionPay {       merchantAccountId     }     usBankAccount {       routeId       plaidPublicKey     }     venmo {       merchantId       accessToken       environment     }     visaCheckout {       apiKey       externalClientId       supportedCardBrands     }     braintreeApi {       accessToken       url     }     supportedFeatures   } }",
                "operationName": "ClientConfiguration"
            }
    
            try:
                r = self.session.post('https://payments.braintree-api.com/graphql',
                                    headers=braintreeHeaders, json=braintreeData)
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.clientToken()

            self.jwt = r.json()["data"]["clientConfiguration"]["creditCard"]["threeDSecure"]["cardinalAuthenticationJWT"]

            self.billing()
        else:
            logger.error(SITE,self.taskID,'Failed to retrieve token. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.clientToken()

    def billing(self):
        self.profile = loadProfile(self.task["PROFILE"])
        if self.profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        self.countryCode = self.profile["countryCode"]

        try:
            fireCheckout = self.session.get(f'https://www.grosbasket.com/{self.region}/firecheckout/',headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'accept': 'text/javascript, text/html, application/xml, text/xml, */*'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.billing()

        if fireCheckout.status_code == 200:
            soup = BeautifulSoup(fireCheckout.text, "html.parser")
            try:
                self.addressId = soup.find(
                    "input", {"name": "billing[address_id]"})["value"]
                self.shippingId = soup.find(
                    "input", {"name": "shipping[address_id]"})["value"]
                self.cartQty = soup.find("select", {"id": "fc_qty_change"})["name"]
                self.cartSafe = self.cartQty.replace('cart', 'cart_safe')
    
                self.shippingMethodValue = soup.find("input",{"name":"shipping_method"})["value"]
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to scrape shipping details. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.billing()


            self.saveOrder()


    def saveOrder(self):
        if self.task["PAYMENT"] == "paypal":
            self.paymentMethod = "paypal_express"

            payload = {
                'form_key': self.formKey,
                'qty_h': 1,
                'product_id2': self.productId,
                self.cartSafe: 1,
                self.cartQty: 1,
                'coupon[remove]': 0,
                'coupon[code]': '',
                'billing[address_id]': self.shippingId,
                'billing[firstname]': self.profile["firstName"],
                'billing[lastname]': self.profile["lastName"],
                'billing[email]': self.profile["email"],
                'billing[telephone]': self.profile["phone"],
                'billing[street][]': '{} {}'.format(self.profile["house"], self.profile["addressOne"]),
                'billing[postcode]': self.profile["zip"],
                'billing[city]': self.profile["city"],
                'billing[country_id]': self.countryCode,
                'billing[region_id]': '',
                'billing[region]': self.region,
                'shipping[same_as_billing]': 'on',
                'billing[company]': '',
                'billing[vat_id]': '',
                'billing[customer_password]': '',
                'billing[confirm_password]': '',
                'billing[save_in_address_book]': 1,
                'billing[use_for_shipping]': 1,
                'shipping[address_id]': self.addressId,
                'shipping[firstname]': '',
                'shipping[lastname]': '',
                'shipping[telephone]': '',
                'shipping[street][]': '',
                'shipping[postcode]': '',
                'shipping[city]': '',
                'shipping[country_id]': self.countryCode,
                'shipping[region_id]': '',
                'shipping[region]': '',
                'shipping[company]': '',
                'shipping[vat_id]': '',
                'shipping[save_in_address_book]': 1,
                'shipping[save_in_address_book]': 1,
                'shipping_method': self.shippingMethodValue,
                'payment[method]': self.paymentMethod,
                'agreement[3]': 1,
                'payment[device_data]': {"device_session_id":""},
            }
    
            try:
                postSaveOrder = self.session.post(f'https://www.grosbasket.com/{self.region}/firecheckout/index/saveOrder/form_key/{self.formKey}',data=payload,headers={
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                    'accept': 'text/javascript, text/html, application/xml, text/xml, */*'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.saveOrder()
    
            if postSaveOrder.status_code == 200:
                logger.success(SITE,self.taskID,'Successfully set shipping method')
                self.startPaypal()
            elif postSaveOrder.status_code != 200:
                logger.error(SITE,self.taskID,'Failed to set shipping method')
                time.sleep(int(self.task["DELAY"]))
                self.saveOrder()

        elif self.task["PAYMENT"] == "card":
            self.braintreeCard()

    def startPaypal(self):
        logger.info(SITE,self.taskID,'Starting [PAYPAL] checkout...')
        try:
            startExpress = self.session.get('https://www.grosbasket.com/en/paypal/express/start/',headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.startPaypal()

        if "paypal" in startExpress.url:
            self.end = time.time() - self.start
            logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')
            updateConsoleTitle(False,True,SITE)

            url = storeCookies(startExpress.url,self.session, self.productTitle, self.productImage, self.productPrice)

            try:
                quote = self.session.post('https://www.grosbasket.com/en/braintree/checkout/quoteTotal/',headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                    'Accept': 'text/javascript, text/html, application/xml, text/xml, */*'
                })
                self.price = quote.json()["grandTotal"]
                self.currency = quote.json()["currencyCode"]
                self.productPrice = '{} {}'.format(self.price, self.currency)
            except Exception as e:
                log.info(e)
                pass
        

        
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
                sendNotification(SITE,self.productTitle)
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
            self.startPaypal()



    def braintreeCard(self):
        logger.info(SITE,self.taskID,'Starting [CREDIT CARD] checkout...')
        try:
            quote = self.session.post('https://www.grosbasket.com/en/braintree/checkout/quoteTotal/',headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'Accept': 'text/javascript, text/html, application/xml, text/xml, */*'
            })
        except:
            logger.error(SITE,self.taskID,'Connection Error. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.braintreeCard()
        
        self.price = quote.json()["grandTotal"]
        self.currency = quote.json()["currencyCode"]
        self.productPrice = '{} {}'.format(self.price, self.currency)

        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        countryCode = profile["countryCode"]

        choice = "0123456789abcdefghijklmnopqrstuvwxyz"
        self.referenceId = "0_" + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + "-" + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + "-" + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(
            choice) - 1)] + "-" + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + "-" + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)]

        configUrl = 'https://api.braintreegateway.com/merchants/yxqdsd59q3vv367y/client_api/v1/configuration?authorizationFingerprint={}&_meta[merchantAppId]={}&_meta[platform]={}&_meta[sdkVersion]={}&_meta[source]={}&_meta[integration]={}&_meta[integrationType]={}&_meta[sessionId]={}&braintreeLibraryVersion={}&configVersion={}'.format(self.fingerprint,'www.grosbasket.com','web','3.16.0','client','custom','custom',self.sessionId,'braintree/web/3.16.0','3')
        config = self.session.get(configUrl,headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
            'Accept': '*/*'
        })
        if config.status_code == 200:
            self.cardinalJWT = config.json()["cardinalAuthenticationJWT"]
        else:
            time.sleep(int(self.task["DELAY"]))
            self.braintreeCard()



        headers = {
            'authority': 'payments.braintree-api.com',
            'authorization': 'Bearer {}'.format(self.fingerprint),
            'sec-fetch-dest': 'empty',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'braintree-version': '2018-05-10',
            'content-type': 'application/json',
            'accept': '*/*',
            'origin': 'https://assets.braintreegateway.com',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'referer': 'https://assets.braintreegateway.com/web/3.16.0/html/hosted-fields-frame.min.html',
            'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6',
        }
        data = {
            "clientSdkMetadata": {
                "source": "client",
                "integration": "custom",
                "sessionId": self.sessionId
            },
            "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }",
            "variables": {
                "input": {
                    "creditCard": {
                        "number": profile["card"]["cardNumber"],
                        "expirationMonth": profile["card"]["cardMonth"],
                        "expirationYear": profile["card"]["cardYear"],
                        "cvv": profile["card"]["cardCVV"]
                    },
                    "options": {"validate": False}}
            },
            "operationName": "TokenizeCreditCard"
        }

        r = self.session.post('https://payments.braintree-api.com/graphql',
                              headers=headers, json=data, )
        ccToken = r.json()['data']['tokenizeCreditCard']['token']


        cardinalHeaders = {
            'authority': 'centinelapi.cardinalcommerce.com',
            'sec-fetch-dest': 'empty',
            'x-cardinal-tid': '',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'content-type': 'application/json;charset=UTF-8',
            'accept': '*/*',
            'origin': 'https://www.grosbasket.com',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'referer': f'https://www.grosbasket.com/{self.region}/firecheckout/',
            'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6',
        }
        data = {
            "BrowserPayload": {
                "Order": {
                    "OrderDetails": {},
                    "Consumer": {
                        "BillingAddress": {},
                        "ShippingAddress": {},
                        "Account": {}
                    },
                    "Cart": [],
                    "Token": {},
                    "Authorization": {},
                    "Options": {},
                    "CCAExtension": {}
                },
                "SupportsAlternativePayments": {
                    "cca": True,
                    "hostedFields": False,
                    "applepay": False,
                    "discoverwallet": False,
                    "wallet": False,
                    "paypal": False,
                    "visacheckout": False
                }
            },
            "Client": {
                "Agent": "SongbirdJS",
                "Version": "1.30.2"
            },
            "ConsumerSessionId": self.referenceId,
            "ServerJWT": self.jwt
        }
        r = self.session.post('https://centinelapi.cardinalcommerce.com/V1/Order/JWT/Init',
                              headers=cardinalHeaders, json=data, )
        self.CardinalJWT = r.json()['CardinalJWT'].split(".")[1]
        payload = str(base64.b64decode(
            str(self.CardinalJWT.replace('-', '+').replace('_', '/') + "==")))
        self.consumerId = payload.split('ConsumerSessionId":"')[
            1].split('"')[0]





        headers = {
            'Accept':'*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Host': 'api.braintreegateway.com',
            'Origin': 'https://www.grosbasket.com',
            'Referer': f'https://www.grosbasket.com/{self.region}/firecheckout/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }

        payload = {
            "amount":self.price,
            "braintreeLibraryVersion":"braintree/web/3.16.0",
            "_meta":{
                "merchantAppId":"www.grosbasket.com",
                "platform":"web",
                "sdkVersion":"3.16.0",
                "source":"client",
                "integration":"custom",
                "integrationType":"custom",
                "sessionId":self.sessionId,
            },
            "authorizationFingerprint": self.fingerprint
        }

        r = self.session.post('https://api.braintreegateway.com/merchants/yxqdsd59q3vv367y/client_api/v1/payment_methods/{}/three_d_secure/lookup'.format(
            ccToken), headers=headers, json=payload, )
        self.nonce = r.json()['paymentMethod']['nonce']
        self.pareq = r.json()['lookup']['pareq']
        self.md = r.json()['lookup']['md']
        self.transactionId = r.json()['lookup']['transactionId']
        self.termURL = r.json()['lookup']['termUrl']



        r = self.session.post('https://0eaf.cardinalcommerce.com/EAFService/jsp/v1/redirect',data={'PaReq':self.pareq,'MD':self.md,'TermUrl':self.termURL},headers={
            'Host': '0eaf.cardinalcommerce.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Origin': 'https://assets.braintreegateway.com',
            'Referer': 'https://assets.braintreegateway.com/web/3.16.0/html/three-d-secure-bank-frame.min.html',
            'Sec-Fetch-Dest': 'iframe',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        })
        soup = BeautifulSoup(r.text, 'lxml')
        self.pareq = str(soup.find("input", attrs={"name": "PaReq"})['value'])
        self.md = soup.find("input", attrs={"name": "MD"})['value']


        headers = {
            'authority': 'verifiedbyvisa.acs.touchtechpayments.com',
            'cache-control': 'max-age=0',
            'origin': 'https://0eaf.cardinalcommerce.com',
            'upgrade-insecure-requests': '1',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'sec-fetch-dest': 'iframe',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'navigate',
        }
        data = {'PaReq': self.pareq,'TermUrl': 'https://0eaf.cardinalcommerce.com/EAFService/jsp/v1/term', 'MD': self.md}
        r = self.session.post('https://verifiedbyvisa.acs.touchtechpayments.com/v1/payerAuthentication',
                              headers=headers, data=data)
        
        print(r.text)
        soup = BeautifulSoup(r.text, 'lxml')
        self.transToken = str(soup.find_all("script")[0]).split('"')[1]
        print(self.transToken)

        self.ThreeDS()
        # if len(self.transToken) > 70:
            # self.nonThreeDS()
        # else:
            # self.ThreeDS()

    def nonThreeDS(self):
        logger.info(SITE,self.taskID,'Initiating non 3DS checkout')
        
        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://verifiedbyvisa.acs.touchtechpayments.com',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Sec-Fetch-Dest': 'iframe',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'navigate',
        }
        data = {'MD': self.md, 'PaRes': self.transToken}
        r = self.session.post('https://0eaf.cardinalcommerce.com/EAFService/jsp/v1/term',
                              headers=headers, data=data)


        payload = {
            'billing[address_id]': self.addressId,
            'billing[firstname]': self.profile["firstName"],
            'billing[lastname]': self.profile["lastName"],
            'billing[email]': self.profile["email"],
            'billing[telephone]': self.profile["phone"],
            'billing[street][]': '{} {}'.format(self.profile["house"], self.profile["addressOne"]),
            'billing[postcode]': self.profile["zip"],
            'billing[city]': self.profile["city"],
            'billing[country_id]': self.countryCode,
            'billing[region_id]': '',
            'billing[region]': self.profile["region"],
            'shipping[same_as_billing]': 1,
            'billing[company]': '',
            'billing[vat_id]': '',
            'billing[customer_password]': '',
            'billing[confirm_password]': '',
            'billing[save_in_address_book]': 1,
            'billing[use_for_shipping]': 1,
            'shipping[address_id]': self.shippingId,
            'shipping[firstname]': self.profile["firstName"],
            'shipping[lastname]':  self.profile["lastName"],
            'shipping[telephone]': self.profile["phone"],
            'shipping[street][]': '{} {}'.format(self.profile["house"], self.profile["addressOne"]),
            'shipping[postcode]': self.profile["zip"],
            'shipping[city]': self.profile["city"],
            'shipping[country_id]': self.countryCode,
            'shipping[region_id]': '',
            'shipping[region]': '',
            'shipping[company]': '',
            'shipping[vat_id]': '',
            'shipping[save_in_address_book]': 1,
            'shipping_method': self.shippingMethodValue,
            'coupon[remove]': 0,
            'coupon[code]': '',
            'order-comment': '',
            'payment[method]': 'gene_braintree_creditcard',
            'payment[payment_method_nonce]':self.nonce,
            self.cartSafe: 1,
            self.cartQty: 1,
            'payment[device_data]': {"device_session_id": ""},
            'agreement[3]': 1
        }
    
        try:
            postSaveOrder = self.session.post(f'https://www.grosbasket.com/{self.region}/firecheckout/index/saveOrder/form_key/{self.formKey}',data=payload,headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'accept': 'text/javascript, text/html, application/xml, text/xml, */*'
            })
        except:
            logger.error(SITE,self.taskID,'Connection Error. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.nonThreeDS()


    def ThreeDS(self):
        logger.info(SITE,self.taskID,'Initiating 3DS checkout')

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/json',
            'Host': '0eaf.cardinalcommerce.com',
            'Origin': 'https://0eaf.cardinalcommerce.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }

        payload = {
            "Request":{
                "Headers":"sec-fetch-mode:navigate, referer:https://0eaf.cardinalcommerce.com/EAFService/jsp/v1/redirect, sec-fetch-site:same-origin, accept-language:en-US,en;q=0.9, cookie:BIGipServerCentinel-Prod-Web-EnhancedAltFlow.app~Centinel-Prod-Web-EnhancedAltFlow_pool=402776842.55335.0000; _gcl_au=1.1.364579413.1591790712; _ga=GA1.2.1225583943.1591790712, host:0eaf.cardinalcommerce.com, upgrade-insecure-requests:1, connection:keep-alive, user-agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36, accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9, sec-fetch-dest:iframe",
                "Ip":"",
                "Referer":"https://0eaf.cardinalcommerce.com/EAFService/jsp/v1/redirect"
            },
            "Browser":{
                "Language":"en-US",
                "Useragent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
                "Cookies":{
                    "Legacy":True,
                    "SessionStorage":True,
                    "LocalStorage":True
                },
                "Fingerprint":self.fingerprint,
                "FingerprintJson":"[{\"key\":\"user_agent\",\"value\":\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36\"},{\"key\":\"language\",\"value\":\"en-US\"},{\"key\":\"color_depth\",\"value\":24},{\"key\":\"resolution\",\"value\":[2560,1440]},{\"key\":\"available_resolution\",\"value\":[2560,1400]},{\"key\":\"timezone_offset\",\"value\":-60},{\"key\":\"session_storage\",\"value\":1},{\"key\":\"local_storage\",\"value\":1},{\"key\":\"indexed_db\",\"value\":1},{\"key\":\"open_database\",\"value\":1},{\"key\":\"cpu_class\",\"value\":\"unknown\"},{\"key\":\"navigator_platform\",\"value\":\"Win32\"},{\"key\":\"do_not_track\",\"value\":\"unknown\"},{\"key\":\"regular_plugins\",\"value\":[\"Chrome PDF Plugin::Portable Document Format::application/x-google-chrome-pdf~pdf\",\"Chrome PDF Viewer::::application/pdf~pdf\",\"Native Client::::application/x-nacl~,application/x-pnacl~\"]},{\"key\":\"adblock\",\"value\":false},{\"key\":\"has_lied_languages\",\"value\":false},{\"key\":\"has_lied_resolution\",\"value\":false},{\"key\":\"has_lied_os\",\"value\":false},{\"key\":\"has_lied_browser\",\"value\":false},{\"key\":\"touch_support\",\"value\":[0,false,false]},{\"key\":\"js_fonts\",\"value\":[\"Arial\",\"Arial Black\",\"Arial Narrow\",\"Book Antiqua\",\"Bookman Old Style\",\"Calibri\",\"Cambria\",\"Cambria Math\",\"Century\",\"Century Gothic\",\"Century Schoolbook\",\"Comic Sans MS\",\"Consolas\",\"Courier\",\"Courier New\",\"Garamond\",\"Georgia\",\"Helvetica\",\"Impact\",\"Lucida Bright\",\"Lucida Calligraphy\",\"Lucida Console\",\"Lucida Fax\",\"Lucida Handwriting\",\"Lucida Sans\",\"Lucida Sans Typewriter\",\"Lucida Sans Unicode\",\"Microsoft Sans Serif\",\"Monotype Corsiva\",\"MS Gothic\",\"MS Outlook\",\"MS PGothic\",\"MS Reference Sans Serif\",\"MS Sans Serif\",\"MS Serif\",\"Palatino Linotype\",\"Segoe Print\",\"Segoe Script\",\"Segoe UI\",\"Segoe UI Light\",\"Segoe UI Semibold\",\"Segoe UI Symbol\",\"Tahoma\",\"Times\",\"Times New Roman\",\"Trebuchet MS\",\"Verdana\",\"Wingdings\",\"Wingdings 2\",\"Wingdings 3\"]}]",
                "Screen":{
                    "Resolution":"1440x2560",
                    "Ratio":1.7777777777777777
                },
                "TimeoffSet":-1,
                "Plugins":"{\"key\":\"regular_plugins\",\"value\":[\"Chrome PDF Plugin::Portable Document Format::application/x-google-chrome-pdf~pdf\",\"Chrome PDF Viewer::::application/pdf~pdf\",\"Native Client::::application/x-nacl~,application/x-pnacl~\"]}"
            },
            "CardinalPayload":self.pareq
        }
        r = self.session.post('https://0eaf.cardinalcommerce.com/EAFService/v1/saveProfilingData',json=payload,headers=headers)

        headers = {
            'authority': 'poll.touchtechpayments.com',
            'sec-fetch-dest': 'empty',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'content-type': 'application/json',
            'accept': '*/*',
            'origin': 'https://verifiedbyvisa.acs.touchtechpayments.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
        }

        data = '{"transToken": "%s"}' % self.transToken

        r = self.session.post('https://poll.touchtechpayments.com/poll',
                              headers=headers, data=data, )
        

        if r.json()["status"] == "blocked":
            logger.cardError('', True, SITE, 'Card Blocked',self.taskID)
        if r.json()["status"] == "pending":
            logger.warning(SITE,self.taskID,'Polling 3DS...')
            while r.json()["status"] == "pending":
                r = self.session.post('https://poll.touchtechpayments.com/poll',
                                      headers=headers, data=data, )

        authToken = r.json()['authToken']
        logger.alert(SITE,self.taskID,'3DS Authorised')


        data = '{"transToken":"%s","authToken":"%s"}' % (
            self.transToken, authToken)
        r = self.session.post("https://macs.touchtechpayments.com/v1/confirmTransaction",
                              headers=headers, data=data, )



        pares = r.json()['Response']


        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://verifiedbyvisa.acs.touchtechpayments.com',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Sec-Fetch-Dest': 'iframe',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'navigate',
        }
        data = {'MD': self.md, 'PaRes': pares}
        r = self.session.post('https://0eaf.cardinalcommerce.com/EAFService/jsp/v1/term',
                              headers=headers, data=data, )
        


        headers = {
            'authority': 'centinelapi.cardinalcommerce.com',
            'cache-control': 'max-age=0',
            'origin': 'https://0eaf.cardinalcommerce.com',
            'upgrade-insecure-requests': '1',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'sec-fetch-dest': 'iframe',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'navigate',
        }
        data = {'PaRes': pares, 'MD': self.consumerId}
        r = self.session.post('https://centinelapi.cardinalcommerce.com/V1/TermURL/Overlay/CCA',
                              headers=headers, data=data, )


        soup = BeautifulSoup(r.text, 'lxml')
        jwtCheckout = str(soup.find_all("script")[0]).split('"')[1]


        headers = {
            'authority': 'centinelapi.cardinalcommerce.com',
            'cache-control': 'max-age=0',
            'origin': 'https://0eaf.cardinalcommerce.com',
            'Referer':'https://0eaf.cardinalcommerce.com/EAFService/jsp/v1/term',
            'upgrade-insecure-requests': '1',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'sec-fetch-dest': 'iframe',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'navigate',
        }

        #payload = {
        #    "amount":self.price,
        #    "jwt":jwtCheckout,
        #    "paymentMethodNonce":self.nonce,
        #    "braintreeLibraryVersion":"braintree/web/3.16.0",
        #    "_meta":{
        #        "merchantAppId":"www.grosbasket.com",
        #        "platform":"web",
        #        "sdkVersion":"3.16.0",
        #        "source":"client",
        #        "integration":"custom",
        #        "integrationType":"custom",
        #        "sessionId":self.sessionId,
        #    },
        #    "authorizationFingerprint": self.fingerprint
        #}
#
        #r = self.session.post('https://api.braintreegateway.com/merchants/yxqdsd59q3vv367y/client_api/v1/payment_methods/{}/three_d_secure/lookup'.format(
        #   self.nonce ), headers=headers, json=payload, )
#
        #with open('request3DS-7.txt','w') as output:
        #    output.write(f'{r} - {r.text}')


        print(self.termURL)
        r = self.session.post(self.termURL,headers=headers,data={'MD': self.md, 'PaRes': pares})


        #r = self.session.get('https://assets.braintreegateway.com/web/3.16.0/html/three-d-secure-authentication-complete-frame.html')


        payload = {
                'billing[address_id]': self.addressId,
                'billing[firstname]': self.profile["firstName"],
                'billing[lastname]': self.profile["lastName"],
                'billing[email]': self.profile["email"],
                'billing[telephone]': self.profile["phone"],
                'billing[street][]': '{} {}'.format(self.profile["house"], self.profile["addressOne"]),
                'billing[postcode]': self.profile["zip"],
                'billing[city]': self.profile["city"],
                'billing[country_id]': self.countryCode,
                'billing[region_id]': '',
                'billing[region]': self.profile["region"],
                'shipping[same_as_billing]': 1,
                'billing[company]': '',
                'billing[vat_id]': '',
                'billing[customer_password]': '',
                'billing[confirm_password]': '',
                'billing[save_in_address_book]': 1,
                'billing[use_for_shipping]': 1,
                'shipping[address_id]': self.shippingId,
                'shipping[firstname]': self.profile["firstName"],
                'shipping[lastname]':  self.profile["lastName"],
                'shipping[telephone]': self.profile["phone"],
                'shipping[street][]': '{} {}'.format(self.profile["house"], self.profile["addressOne"]),
                'shipping[postcode]': self.profile["zip"],
                'shipping[city]': self.profile["city"],
                'shipping[country_id]': self.countryCode,
                'shipping[region_id]': '',
                'shipping[region]': '',
                'shipping[company]': '',
                'shipping[vat_id]': '',
                'shipping[save_in_address_book]': 1,
                'shipping_method': self.shippingMethodValue,
                'coupon[remove]': 0,
                'coupon[code]': '',
                'order-comment': '',
                'payment[method]': 'gene_braintree_creditcard',
                'payment[payment_method_nonce]':self.nonce,
                self.cartSafe: 1,
                self.cartQty: 1,
                'payment[device_data]': {"device_session_id": ""},
                'agreement[3]': 1
            }
    
        try:
            postSaveOrder = self.session.post(f'https://www.grosbasket.com/{self.region}/firecheckout/index/saveOrder/form_key/{self.formKey}',data=payload,headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'accept': 'text/javascript, text/html, application/xml, text/xml, */*'
            })
        except:
            logger.error(SITE,self.taskID,'Connection Error. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.saveOrder()



        
        print(postSaveOrder.json())
        if postSaveOrder.json()["success"] == True:
            logger.secondary(SITE,self.taskID,'Checkout Complete!')
            updateConsoleTitle(False,True,SITE)
            discord.success(
                webhook=loadSettings()["webhook"],
                site=SITE,
                url=self.task["PRODUCT"],
                image=self.productImage,
                title=self.productTitle,
                size=self.size,
                price=self.productPrice,
                paymentMethod='Card',
                profile=self.task["PROFILE"],
            )
            while True:
                pass

        elif postSaveOrder.json()["success"] == False:
            logger.error(SITE,self.taskID,'Checkout Failed')
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
            )
            while True:
                pass


        
