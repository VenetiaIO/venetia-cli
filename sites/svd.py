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
import uuid
from urllib3.exceptions import HTTPError

from utils.logger import logger
from utils.webhook import discord
from utils.log import log
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, randomString, sendNotification,storeCookies, updateConsoleTitle)
SITE = 'SVD'


class SVD:
    def __init__(self, task, taskName):
        self.task = task
        self.session = requests.session()
        self.taskID = taskName

        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)

        self.collect()

    def collect(self):
        logger.prepare(SITE,self.taskID,'Getting product page...')
        try:
            url = '{}{}'.format(self.task["PRODUCT"],f"#%253F_={randomString(20)}")
            retrieve = self.session.get(url,headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            #log.info(e)
            logger.error(SITE,self.taskID,'Error retrieving product page')
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.collect()

        if retrieve.status_code == 200:
            self.start = time.time()
            logger.success(SITE,self.taskID,'Got product page')
            try:
                soup = BeautifulSoup(retrieve.text, "html.parser")
                self.formKey = soup.find(
                    "input", {"name": "form_key"})["value"]
                cookie_obj = requests.cookies.create_cookie(
                    domain='.www.sivasdescalzo.com', name='form_key', value=self.formKey)
                self.session.cookies.set_cookie(cookie_obj)
    
                self.productTitle = soup.find(
                    "span", {"class": "product-data__model"}).text
                self.productPrice = soup.find("span", {"class": "price"}).text
                self.productImage = soup.find_all("img", {"class": "lazyload"})[0]["src"]
                self.cartURL = soup.find(
                    "form", {"id": "product_addtocart_form"})["action"]
                self.productID = soup.find("input", {"name": "item"})["value"]
    
                regexSwatch = r'"jsonSwatchConfig":(.+)"}}'
                regexAttributes = r'{"attributes":(.+)}}'
                regexOption = r'"optionConfig":(.+)}}'
                matches = re.search(regexSwatch, retrieve.text, re.MULTILINE)
                matches2 = re.search(
                    regexAttributes, retrieve.text, re.MULTILINE)
                matches3 = re.search(regexOption, retrieve.text, re.MULTILINE)
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to scrape page (Most likely out of stock). Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.collect()
            if matches:
                try:
                    jsonSwatch = json.loads(
                        '{' + matches.group() + '}')["jsonSwatchConfig"]
                    dict = list(jsonSwatch.keys())
                    self.SuperAttribute = dict[0]
                    jsonAttributes = json.loads(matches2.group())["attributes"]
    
                    option = json.loads(
                        '{' + matches3.group() + '}')["optionConfig"]
                    dict = list(option.keys())
                    self.option = dict[0]
                except Exception as e:
                    log.info(e)

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
                                self.addToCart()

                elif self.task["SIZE"].lower() == "random":
                    selected = random.choice(allSizes)
                    self.size = selected.split(":")[0]
                    self.sizeID = selected.split(":")[2]
                    self.option = selected.split(":")[1]
                    logger.success(SITE,self.taskID,f'Found Size => {self.size}')
                    self.addToCart()
            else:
                logger.error(SITE,self.taskID,'Failed to scrape page (Most likely out of stock). Retrying...')

        else:
            try:
                status = retrieve.status_code
            except:
                status = 'Unknown'
            logger.error(SITE,self.taskID,f'Failed to get product page => {status}. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.collect()

    def addToCart(self):

        cartForm = {
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
        try:
            cart = self.session.post(self.cartURL, data=cartForm,headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'cookie': f'form_key={self.formKey}',
                'x-requested-with': 'XMLHttpRequest'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()

        if cart.status_code == 200 and cart.json() == []:
            updateConsoleTitle(True,False,SITE)
            logger.success(SITE,self.taskID,'Successfully carted')
            self.jwt()
        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

    def jwt(self):
        self.sessionId = str(uuid.uuid4())

        try:
            section = self.session.get('https://www.sivasdescalzo.com/en/customer/section/load/?sections=cart%2Cdirectory-data%2Cmessages&force_new_section_timestamp=true&_=',headers={
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
                'accept': 'application/json, text/javascript, */*; q=0.01'

            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.jwt()

        try:
            html = section.json()["cart"]["extra_actions"]
            soup = BeautifulSoup(html, "html.parser")
            div = soup.find("div", {"class": ["paypal", "checkout", "paypal-logo",
                                            "braintree-paypal-logobraintree-paypal-mini-cart-container"]})["data-mage-init"]
            jsonDiv = json.loads(div)["Magento_Braintree/js/paypal/button"]
            self.ClientToken = jsonDiv["clientToken"]
    
            result = base64.b64decode(self.ClientToken)
            self.bearerToken = json.loads(result.decode(
                'Utf-8'))["authorizationFingerprint"]
        except Exception as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Failed to retrieve token. Retrying...')
            self.jwt()

        braintreeHeaders = {
            'authority': 'payments.braintree-api.com',
            'authorization': 'Bearer {}'.format(self.bearerToken),
            'sec-fetch-dest': 'empty',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'braintree-version': '2018-05-10',
            'content-type': 'application/json',
            'accept': '*/*',
            'origin': 'https://www.sivasdescalzo.com',
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
            self.jwt()

        try:
            self.config = r.json()["data"]["clientConfiguration"]["creditCard"]["threeDSecure"]
        except:
            logger.error(SITE,self.taskID,'Failed to retrieve token. Retrying...')
            self.jwt()

        if self.config:
            logger.success(SITE,self.taskID,'Successfully retrieved token')
            self.shipping()
        else:
            logger.error(SITE,self.taskID,'Failed to retrieve token. Retrying...')
            self.jwt()

    def shipping(self):

        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        countryCode = profile["countryCode"]

        try:
            shippingPage = self.session.get('https://www.sivasdescalzo.com/en/checkout/',headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'en,en-GB;q=0.9',
                'Cache-Control': 'no-cache',
                'DNT': '1',
                'Pragma': 'no-cache',
                'Referer': self.task["PRODUCT"],
                'Sec-fetch-dest': 'document',
                'Sec-fetch-mode': 'navigate',
                'Sec-fetch-site': 'same-origin',
                'Sec-fetch-user': '?1',
                'Upgrade-insecure-requests': '1',
                'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.shipping()

        if shippingPage.status_code == 200:
            regex = r'{"entity_id":(.+"quoteItemData")'
            #regex2 = r'{"isActive":(.+"ccTypesMapper")'
            regex3 = r'"region_id":(.{.+"types")'
            matches = re.search(regex, shippingPage.text, re.MULTILINE)
            #matches2 = re.search(regex2, shippingPage.text, re.MULTILINE)
            matches3 = re.search(regex3, shippingPage.text, re.MULTILINE)
            if matches:
                try:
                    jsResponse = json.loads(matches.group()[:-16])
                    self.cartID = jsResponse["entity_id"]
    
                    #jsResponse2 = json.loads(matches2.group()[:-16] + '}')
                    #self.clientToken = jsResponse2["clientToken"]
    
                    regions = json.loads('{' + matches3.group()[:-10])["region_id"]
                    try:
                        for r in regions:
                            if r["title"].lower() == profile["region"].lower():
                                self.region = r["title"]
                                self.regionID = r["value"]
                            elif r["title"].lower() != profile["region"].lower():
                                self.regionID = ''
                                self.region = profile["region"]
                    except Exception as e:
                        log.info(e)
                        pass
    
                    logger.success(SITE,self.taskID,'Retrieved cart ID')
                except Exception as e:
                    log.info(e)
                    logger.error(SITE,self.taskID,'Failed to retrieve cart ID. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.shipping()

            else:
                logger.error(SITE,self.taskID,'Failed to retrieve cart ID. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.shipping()

            if self.regionID:
                ratesForm = {
                    "address": {
                        "street": [profile["house"] + " " + profile["addressOne"], profile["addressTwo"]],
                        "city": profile["city"],
                        "region_id": self.regionID,
                        "region": self.region,
                        "country_id": countryCode,
                        "postcode": profile["zip"],
                        "firstname": profile["firstName"],
                        "lastname": profile["lastName"],
                        "telephone": "",
                        "custom_attributes": [{"attribute_code": "taxvat", "value": ""}]
                    }
                }
            else:
                ratesForm = {
                    "address": {
                        "street": [profile["house"] + " " + profile["addressOne"], profile["addressTwo"]],
                        "city": profile["city"],
                        "region": profile["region"],
                        "country_id": countryCode,
                        "postcode": profile["zip"],
                        "firstname": profile["firstName"],
                        "lastname": profile["lastName"],
                        "telephone": profile["phone"],
                        "custom_attributes": [{"attribute_code": "taxvat", "value": ""}]
                    }
                }

            try:
                rates = self.session.post(f'https://www.sivasdescalzo.com/en/rest/en/V1/guest-carts/{self.cartID}/estimate-shipping-methods', json=ratesForm,headers={
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                    'accept': '*/*',
                    'cookie': f'form_key={self.formKey}'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.shipping()

            if rates.status_code == 200:
                try:
                    rate = rates.json()[0]["method_code"]
                    carrier_code = rates.json()[0]["carrier_code"]
                except Exception as e:
                    log.info(e)
                    logger.error(SITE,self.taskID,'Failed to set shipping. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.shipping()


                if self.regionID:
                    shippingForm = {
                        "addressInformation":
                        {
                            "shipping_address":
                            {"countryId": countryCode,
                             "regionId": self.regionID,
                             "regionCode": self.region,
                             "region": self.region,
                             "street": [profile["house"] + " " + profile["addressOne"], profile["addressTwo"]],
                             "telephone": profile["phone"],
                             "postcode": profile["zip"],
                             "city": profile["city"],
                             "firstname": profile["firstName"],
                             "lastname": profile["lastName"],
                             "customAttributes": [{"attribute_code": "taxvat", "value": ""}]},
                            "billing_address":
                            {"countryId": countryCode,
                             "region": profile["region"],
                             "street": [profile["house"] + " " + profile["addressOne"], profile["addressTwo"]],
                             "telephone": profile["phone"],
                             "postcode": profile["zip"],
                             "city": profile["city"],
                             "firstname": profile["firstName"],
                             "lastname": profile["lastName"],
                             "customAttributes": [{"attribute_code": "taxvat", "value": ""}],
                             "saveInAddressBook": None},
                            "shipping_method_code": rate, "shipping_carrier_code": carrier_code, "extension_attributes": {}
                        }
                    }
                else:
                    shippingForm = {
                        "addressInformation":
                        {
                            "shipping_address":
                            {"countryId": countryCode,
                             "region": profile["region"],
                             "street": [profile["house"] + " " + profile["addressOne"], profile["addressTwo"]],
                             "telephone": profile["phone"],
                             "postcode": profile["zip"],
                             "city": profile["city"],
                             "firstname": profile["firstName"],
                             "lastname": profile["lastName"],
                             "customAttributes": [{"attribute_code": "taxvat", "value": ""}]},
                            "billing_address":
                            {"countryId": countryCode,
                             "region": profile["region"],
                             "street": [profile["house"] + " " + profile["addressOne"], profile["addressTwo"]],
                             "telephone": profile["phone"],
                             "postcode": profile["zip"],
                             "city": profile["city"],
                             "firstname": profile["firstName"],
                             "lastname": profile["lastName"],
                             "customAttributes": [{"attribute_code": "taxvat", "value": ""}],
                             "saveInAddressBook": None},
                            "shipping_method_code": rate, "shipping_carrier_code": carrier_code, "extension_attributes": {}
                        }
                    }

                logger.success(SITE,self.taskID,'Successfully retrieved shipping rates')
                try:
                    sendShipping = self.session.post(f'https://www.sivasdescalzo.com/en/rest/en/V1/guest-carts/{self.cartID}/shipping-information',json=shippingForm, headers={
                        'authority': 'www.sivasdescalzo.com',
                        'path': f'/en/rest/en/V1/guest-carts/{self.cartID}/shipping-information',
                        'scheme': 'https',
                        'accept': '*/*',
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'en-US,en;q=0.9',
                        'content-type': 'application/json',
                        'origin': 'https://www.sivasdescalzo.com',
                        'referer': 'https://www.sivasdescalzo.com/en/checkout/',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-origin',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                        'x-requested-with': 'XMLHttpRequest',
                        'cookie': f'form_key={self.formKey}'
                    })
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    log.info(e)
                    logger.error(SITE,self.taskID,'Error: {}'.format(e))
                    logger.error(SITE,self.taskID,'Connection Error. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    self.shipping()

                if sendShipping.status_code == 200:
                    self.price = sendShipping.json()["totals"]["grand_total"]
                    logger.success(SITE,self.taskID,'Successfully set shipping')

                    if self.task["PAYMENT"].lower() == "paypal":
                        self.braintreePaypal()
                    if self.task["PAYMENT"].lower() == "card":
                        self.braintreeCard()
                else:
                    logger.error(SITE,self.taskID,'Failed to set shipping. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.shipping()

            else:
                logger.error(SITE,self.taskID,'Failed to get shipping rates. Retrying...')
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                self.shipping()


        else:
            logger.error(SITE,self.taskID,'Failed to get shipping. Retrying...')
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.shipping()

    def braintreePaypal(self):

        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        countryCode = profile["countryCode"]

        headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Origin': 'https://www.sivasdescalzo.com',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
        }
        sessionId = str(uuid.uuid4())

        try:
            data = {
                "returnUrl": "https://www.paypal.com/checkoutnow/error",
                "cancelUrl": "https://www.paypal.com/checkoutnow/error",
                "offerPaypalCredit": False,
                "experienceProfile": {"brandName": "SVD - sivasdescalzo", "localeCode": "en_US", "noShipping": "false", "addressOverride": True},
                "amount": self.price,
                "currencyIsoCode": "EUR",
                "line1": profile["house"] + " " + profile["addressOne"],
                "city": profile["city"],
                "state": "",
                "postalCode": profile["zip"],
                "countryCode": countryCode,
                "phone": profile["phone"],
                "recipientName": "{} {}".format(profile["firstName"], profile["lastName"]),
                "braintreeLibraryVersion": "braintree/web/3.48.0",
                "_meta": {"merchantAppId": "www.sivasdescalzo.com", "platform": "web", "sdkVersion": "3.48.0", "source": "client", "integration": "custom", "integrationType": "custom", "sessionId": sessionId},
                "authorizationFingerprint": self.bearerToken
            }
            try:
                r = self.session.post('https://api.braintreegateway.com/merchants/7rgb8j8vb5f4hdwg/client_api/v1/paypal_hermes/create_payment_resource',
                                        headers=headers, json=data)
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.braintreePaypal()
    
            paymentToken = r.json()['paymentResource']['paymentToken']
            paypal = r.json()['paymentResource']['redirectUrl']
            token = paypal.split("token=")[1]
            checkoutUrl = "https://www.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token={}".format(
                token)
            logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord! (DONT CLOSE APPLICATION UNTIL YOU HAVE COMPLETED CHECKOUT)')
            logger.secondary(SITE,self.taskID,'Polling PayPal Checkout...')
        except:
            logger.error(SITE,self.taskID,'Failed to get PayPal checkout. Retrying...')
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.braintreePaypal()

        updateConsoleTitle(False,True,SITE)
        url = storeCookies(checkoutUrl,self.session)
        self.end = time.time() - self.start
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
        except:
            logger.secondary(SITE,self.taskID,'Failed to send webhook. Checkout here ==> {}'.format(url))

        headers = {
            "Host": "api.braintreegateway.com",
            "Origin": "https://www.sivasdescalzo.com",
            "Referer": "https://www.sivasdescalzo.com/en/checkout/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }

        nonce = ''
        while nonce == '':
            try:
                data = {"paypalAccount": {"correlationId": token, "options": {"validate": False}, "paymentToken": paymentToken, "payerId": "", "unilateral": False, "intent": "authorize"}, "braintreeLibraryVersion": "braintree/web/3.48.0", "_meta": {
                    "merchantAppId": "www.sivasdescalzo.com", "platform": "web", "sdkVersion": "3.48.0", "source": "client", "integration": "custom", "integrationType": "custom", "sessionId": sessionId}, "authorizationFingerprint": self.bearerToken}

                r = self.session.post("https://api.braintreegateway.com/merchants/7rgb8j8vb5f4hdwg/client_api/v1/payment_methods/paypal_accounts",
                                      headers=headers, json=data)

                r.json()['paypalAccounts'][0]['details']['payerInfo']['email']
                payerId = r.json()[
                    'paypalAccounts'][0]['details']['payerInfo']['payerId']

                data = {"paypalAccount": {"correlationId": token, "options": {"validate": False}, "paymentToken": paymentToken, "payerId": payerId, "unilateral": False, "intent": "authorize"}, "braintreeLibraryVersion": "braintree/web/3.48.0",
                        "_meta": {"merchantAppId": "www.sivasdescalzo.com", "platform": "web", "sdkVersion": "3.48.0", "source": "client", "integration": "custom", "integrationType": "custom", "sessionId": sessionId}, "authorizationFingerprint": self.bearerToken}

                r = self.session.post("https://api.braintreegateway.com/merchants/7rgb8j8vb5f4hdwg/client_api/v1/payment_methods/paypal_accounts",
                                      headers=headers, json=data)
                nonce = r.json()['paypalAccounts'][0]['nonce']

            except Exception:
                time.sleep(2)

        headers = {
            'authority': 'www.sivasdescalzo.com',
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'content-type': 'application/json',
            'origin': 'https://www.sivasdescalzo.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
        }

        if self.regionID:
            data = {"cartId": self.cartID, "billingAddress": {"countryId": countryCode, "regionId": self.regionID, "regionCode": "", "region": self.region, "street": [profile["house"] + " " + profile["addressOne"]], "telephone": profile["phone"], "postcode": profile["zip"], "city": profile["city"], "firstname": profile["firstName"], "lastname": profile["lastName"], "customAttributes": [
                {"attribute_code": "taxvat", "value": ""}], "saveInAddressBook": None}, "paymentMethod": {"method": "braintree_paypal", "additional_data": {"payment_method_nonce": nonce, "device_data": "{\"device_session_id\":\"\",\"fraud_merchant_id\":null}"}}, "email": profile["email"]}
        else:
            data = {"cartId": self.cartID, "billingAddress": {"countryId": countryCode, "region": self.region, "street": [profile["house"] + " " + profile["addressOne"]], "telephone": profile["phone"], "postcode": profile["zip"], "city": profile["city"], "firstname": profile["firstName"], "lastname": profile["lastName"], "customAttributes": [
                {"attribute_code": "taxvat", "value": ""}], "saveInAddressBook": None}, "paymentMethod": {"method": "braintree_paypal", "additional_data": {"payment_method_nonce": nonce, "device_data": "{\"device_session_id\":\"\",\"fraud_merchant_id\":null}"}}, "email": profile["email"]}

        try:
            r = self.session.post('https://www.sivasdescalzo.com/en/rest/en/V1/guest-carts/{}/payment-information'.format(
                self.cartID), headers=headers, json=data)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.braintreePaypal()

        logger.secondary(SITE,self.taskID,'PayPal checkout complete')
        while True:
            pass

    def braintreeCard(self):
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        countryCode = profile["countryCode"]

        logger.info(SITE,self.taskID,'Starting [CREDIT CARD] checkout...')

        choice = "0123456789abcdefghijklmnopqrstuvwxyz"
        self.referenceId = "0_" + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + "-" + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + "-" + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(
            choice) - 1)] + "-" + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + "-" + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)] + choice[random.randint(0, len(choice) - 1)]
        headers = {
            'authority': 'payments.braintree-api.com',
            'authorization': 'Bearer {}'.format(self.bearerToken),
            'sec-fetch-dest': 'empty',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'braintree-version': '2018-05-10',
            'content-type': 'application/json',
            'accept': '*/*',
            'origin': 'https://assets.braintreegateway.com',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'referer': 'https://assets.braintreegateway.com/web/3.48.0/html/hosted-fields-frame.min.html',
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
                              headers=headers, json=data)
        ccToken = r.json()['data']['tokenizeCreditCard']['token']

        cardinalHeaders = {
            'authority': 'centinelapi.cardinalcommerce.com',
            'sec-fetch-dest': 'empty',
            'x-cardinal-tid': 'Tid-ae964bae-f800-41fe-9048-5b9cb5431588',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'content-type': 'application/json;charset=UTF-8',
            'accept': '*/*',
            'origin': 'https://www.sivasdescalzo.com',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'referer': 'https://www.sivasdescalzo.com/en/checkout/',
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
            "ServerJWT": self.config["cardinalAuthenticationJWT"]
        }
        r = self.session.post('https://centinelapi.cardinalcommerce.com/V1/Order/JWT/Init',
                              headers=cardinalHeaders, json=data)
        self.CardinalJWT = r.json()['CardinalJWT'].split(".")[1]
        payload = str(base64.b64decode(
            str(self.CardinalJWT.replace('-', '+').replace('_', '/') + "==")))
        self.consumerId = payload.split('ConsumerSessionId":"')[
            1].split('"')[0]

        headers = {
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Origin': 'https://www.sivasdescalzo.com',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
        }
        data = {
            "amount": self.price,
            "additionalInfo": {
                "shippingGivenName": profile["firstName"],
                "shippingSurname": profile["lastName"],
                "shippingPhone": profile["phone"],
                "billingLine1": profile["house"] + " " + profile["addressOne"],
                "billingCity": profile["city"],
                "billingState": self.regionID,
                "billingPostalCode": profile["zip"],
                "billingCountryCode": countryCode,
                "billingPhoneNumber": profile["phone"],
                "billingGivenName": profile["firstName"],
                "billingSurname": profile["lastName"],
                "shippingLine1": profile["house"] + " " + profile["addressOne"],
                "shippingCity": profile["city"],
                "shippingState": self.regionID,
                "shippingPostalCode": profile["zip"],
                "shippingCountryCode": countryCode
            },
            "dfReferenceId": self.consumerId,
            "clientMetadata": {
                "sdkVersion": "web/3.48.0",
                "requestedThreeDSecureVersion": "2",
                "cardinalDeviceDataCollectionTimeElapsed": 12
            },
            "authorizationFingerprint": self.bearerToken,
            "braintreeLibraryVersion": "braintree/web/3.48.0",
            "_meta": {
                "merchantAppId": "www.sivasdescalzo.com",
                "platform": "web",
                "sdkVersion": "3.48.0",
                "source": "client",
                "integration": "custom",
                "integrationType": "custom",
                "sessionId": self.sessionId
            }
        }

        r = self.session.post('https://api.braintreegateway.com/merchants/7rgb8j8vb5f4hdwg/client_api/v1/payment_methods/{}/three_d_secure/lookup'.format(
            ccToken), headers=headers, json=data)
        self.nonce = r.json()['paymentMethod']['nonce']
        self.pareq = r.json()['lookup']['pareq']
        self.md = r.json()['lookup']['md']
        self.transactionId = r.json()['lookup']['transactionId']

        data = {
            "BrowserPayload": {
                "PaymentType": "CCA",
                "Order": {
                    "OrderDetails": {
                        "TransactionId": self.transactionId
                    },
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
                }
            },
            "Client": {
                "Agent": "SongbirdJS",
                "Version": "1.30.2"
            },
            "ConsumerSessionId": self.consumerId,
            "ServerJWT": self.config["cardinalAuthenticationJWT"]
        }
        headers = {
            'authority': 'centinelapi.cardinalcommerce.com',
            'sec-fetch-dest': 'empty',
            'x-cardinal-tid': 'Tid-ae964bae-f800-41fe-9048-5b9cb5431588',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'content-type': 'application/json;charset=UTF-8',
            'accept': '*/*',
            'origin': 'https://www.sivasdescalzo.com',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
        }
        r = self.session.post('https://centinelapi.cardinalcommerce.com/V1/Order/JWT/Continue',
                              headers=headers, json=data)

        redirectHeaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'https://www.sivasdescalzo.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Sec-Fetch-Dest': 'iframe',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'navigate',
        }
        data = {'PaReq': self.pareq, 'MD': self.consumerId,
                'TermUrl': 'https://centinelapi.cardinalcommerce.com/V1/TermURL/Overlay/CCA'}

        r = self.session.post('https://0eaf.cardinalcommerce.com/EAFService/jsp/v1/redirect',
                              headers=redirectHeaders, data=data)

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
        data = {'PaReq': self.pareq,
                'TermUrl': 'https://0eaf.cardinalcommerce.com/EAFService/jsp/v1/term', 'MD': self.md}
        r = self.session.post('https://verifiedbyvisa.acs.touchtechpayments.com/v1/payerAuthentication',
                              headers=headers, data=data)
        try:
            soup = BeautifulSoup(r.text, 'lxml')
            self.transToken = str(soup.find_all("script")[0]).split('"')[1]
        except:
            logger.error(SITE,self.taskID,'Failed to get trans token...')
            self.braintreeCard()

        if len(self.transToken) > 70:
            self.nonThreeDS()
        else:
            self.ThreeDS()

    def nonThreeDS(self):
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        countryCode = profile["countryCode"]

        # 3DS NOT REQUIRED
        logger.info(SITE,self.taskID,'Initiating non 3DS checkout')
        headers = {
            'authority': 'payments.braintree-api.com',
            'authorization': 'Bearer {}'.format(self.bearerToken),
            'sec-fetch-dest': 'empty',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'braintree-version': '2018-05-10',
            'content-type': 'application/json',
            'accept': '*/*',
            'origin': 'https://assets.braintreegateway.com',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
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
                    "options": {"validate": False}
                }
            },
            "operationName": "TokenizeCreditCard"
        }
        r = self.session.post('https://payments.braintree-api.com/graphql',
                              headers=headers, json=data)
        ccToken = r.json()['data']['tokenizeCreditCard']['token']
        self.sesssionId = str(uuid.uuid4())

        if self.regionID:
            orderData = {
                "cartId": self.cartID,
                "billingAddress": {
                    "countryId": countryCode,
                    "regionId": self.regionID,
                    "regionCode": self.region,
                    "region": self.region,
                    "street": [profile["house"] + " " + profile["addressOne"]],
                    "telephone": profile["phone"],
                    "postcode": profile["zip"],
                    "city": profile["city"],
                    "firstname": profile["firstName"],
                    "lastname": profile["lastName"],
                    "saveInAddressBook": None
                },
                "paymentMethod": {
                    "method": "braintree",
                    "additional_data": {
                        "payment_method_nonce": self.nonce,
                        "device_data": '{\\"device_session_id\\":\\"self.sessionId\\",\\"fraud_merchant_id\\":\\"600000\\"}'
                    }
                },
                "email": profile["email"]
            }
        else:
            orderData = {
                "cartId": self.cartID,
                "billingAddress": {
                    "countryId": countryCode,
                    "region": profile["region"],
                    "street": [profile["house"] + " " + profile["addressOne"]],
                    "telephone": profile["phone"],
                    "postcode": profile["zip"],
                    "city": profile["city"],
                    "firstname": profile["firstName"],
                    "lastname": profile["lastName"],
                    "saveInAddressBook": None
                },
                "paymentMethod": {
                    "method": "braintree",
                    "additional_data": {
                        "payment_method_nonce": self.nonce,
                        "device_data": '{\\"device_session_id\\":\\"self.sessionId\\",\\"fraud_merchant_id\\":\\"600000\\"}'
                    }
                },
                "email": profile["email"]
            }
        headers = {
            'authority': 'www.sivasdescalzo.com',
            'accept': '*/*',
            'sec-fetch-dest': 'empty',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'content-type': 'application/json',
            'origin': 'https://www.sivasdescalzo.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
        }

        try:
            r = self.session.post('https://www.sivasdescalzo.com/en/rest/en/V1/guest-carts/{}/payment-information'.format(
                self.cartID), headers=headers, json=orderData)
        except:
            logger.error(SITE,self.taskID,'Connection Error. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.braintreeCard()

        if r.status_code == 400:
            logger.error(SITE,self.taskID,'Checkout Failed. Retrying...')
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
            time.sleep(int(self.task["DELAY"]))
            self.braintreeCard()
        if r.status_code == 200:
            self.end = time.time() - self.start
            updateConsoleTitle(False,True,SITE)
            logger.secondary(SITE,self.taskID,'Checkout Complete!')
            sendNotification(SITE,self.productTitle)
            try:
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
                    proxy=self.session.proxies,
                    speed=self.end
                )
                while True:
                    pass
            except:
                pass

    def ThreeDS(self):
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        countryCode = profile["countryCode"]

        logger.info(SITE,self.taskID,'Initiating 3DS checkout')
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
        # NEED to poll the request until the user verified the payment in app
        r = self.session.post('https://poll.touchtechpayments.com/poll',
                              headers=headers, data=data)

        if r.json()["status"] == "blocked":
            logger.error(SITE,self.taskID,'Card Blocked. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.ThreeDS()
        if r.json()["status"] == "pending":
            logger.warning(SITE,self.taskID,'Polling 3DS...')
            while r.json()["status"] == "pending":
                r = self.session.post('https://poll.touchtechpayments.com/poll',
                                      headers=headers, data=data)

        try:
            json = r.json()
        except:
            logger.error(SITE,self.taskID,'Failed to retrieve auth token for 3DS. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.ThreeDS()

        if r.json()["status"] == "success":
            authToken = r.json()['authToken']
        else:
            logger.error(SITE,self.taskID,'Failed to retrieve auth token for 3DS. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.ThreeDS()

        authToken = r.json()['authToken']
        logger.alert(SITE,self.taskID,'3DS Authorised')

        data = '{"transToken":"%s","authToken":"%s"}' % (
            self.transToken, authToken)
        r = self.session.post("https://macs.touchtechpayments.com/v1/confirmTransaction",
                              headers=headers, data=data)
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
                              headers=headers, data=data)

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
                              headers=headers, data=data)

        soup = BeautifulSoup(r.text, 'lxml')
        jwtCheckout = str(soup.find_all("script")[0]).split('"')[1]

        headers = {
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Origin': 'https://www.sivasdescalzo.com',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
        }
        data = {
            "jwt": jwtCheckout,
            "paymentMethodNonce": self.nonce,
            "braintreeLibraryVersion": "braintree/web/3.48.0",
            "_meta": {
                "merchantAppId": "www.sivasdescalzo.com",
                "platform": "web",
                "sdkVersion": "3.48.0",
                "source": "client",
                "integration": "custom",
                "integrationType": "custom",
                "sessionId": self.sessionId
            },
            "authorizationFingerprint": self.bearerToken
        }
        r = self.session.post('https://api.braintreegateway.com/merchants/7rgb8j8vb5f4hdwg/client_api/v1/payment_methods/{}/three_d_secure/authenticate_from_jwt'.format(
            self.nonce), headers=headers, json=data)

        headers = {
            'authority': 'www.sivasdescalzo.com',
            'accept': '*/*',
            'sec-fetch-dest': 'empty',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'content-type': 'application/json',
            'origin': 'https://www.sivasdescalzo.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
        }
        if self.regionID:
            orderData = {
                "cartId": self.cartID,
                "billingAddress": {
                    "countryId": countryCode,
                    "regionId": self.regionID,
                    "regionCode": self.region,
                    "region": self.region,
                    "street": [profile["house"] + " " + profile["addressOne"]],
                    "telephone": profile["phone"],
                    "postcode": profile["zip"],
                    "city": profile["city"],
                    "firstname": profile["firstName"],
                    "lastname": profile["lastName"],
                    "customAttributes": [
                        {
                            "attribute_code": "taxvat",
                            "value": ""
                        }
                    ],
                    "saveInAddressBook": None
                },
                "paymentMethod": {
                    "method": "braintree",
                    "additional_data": {
                        "payment_method_nonce": self.nonce,
                        "device_data": '{\\"device_session_id\\":\\"self.sessionId\\",\\"fraud_merchant_id\\":\\"600000\\"}'
                    }
                },
                "email": profile["email"]
            }
        else:
            orderData = {
                "cartId": self.cartID,
                "billingAddress": {
                    "countryId": countryCode,
                    "region": profile["region"],
                    "street": [profile["house"] + " " + profile["addressOne"]],
                    "telephone": profile["phone"],
                    "postcode": profile["zip"],
                    "city": profile["city"],
                    "firstname": profile["firstName"],
                    "lastname": profile["lastName"],
                    "customAttributes": [
                        {
                            "attribute_code": "taxvat",
                            "value": ""
                        }
                    ],
                    "saveInAddressBook": None
                },
                "paymentMethod": {
                    "method": "braintree",
                    "additional_data": {
                        "payment_method_nonce": self.nonce,
                        "device_data": '{\\"device_session_id\\":\\"self.sessionId\\",\\"fraud_merchant_id\\":\\"600000\\"}'
                    }
                },
                "email": profile["email"]
            }

        try:
            r = self.session.post('https://www.sivasdescalzo.com/en/rest/en/V1/guest-carts/{}/payment-information'.format(
                self.cartID), headers=headers, json=orderData)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.braintreeCard()

        if r.status_code == 400:
            logger.error(SITE,self.taskID,'Checkout Failed. Retrying...')
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
            time.sleep(int(self.task["DELAY"]))
            self.braintreeCard()

        if r.status_code == 200:
            logger.secondary(SITE,self.taskID,'Checkout Complete!')
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
                    paymentMethod='Card',
                    profile=self.task["PROFILE"],
                    product=self.task["PRODUCT"],
                    proxy=self.session.proxies
                )
                while True:
                    pass
            except:
                pass
