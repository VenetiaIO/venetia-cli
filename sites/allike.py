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

from utils.logger import logger
from utils.webhook import discord
from utils.log import log
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies, updateConsoleTitle, scraper)
SITE = 'ALLIKE'



class ALLIKE:
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
        # self.sess = requests.session()
        self.rowNumber = rowNumber
        self.taskID = taskName

        twoCap = loadSettings()["2Captcha"]
        try:
            self.session = scraper()
        except Exception as e:
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.__init__(task,taskName)
        
        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)

        threading.Thread(target=self.task_checker,daemon=True).start()
        self.collect()

    def collect(self):
        logger.prepare(SITE,self.taskID,'Getting product page...')
        try:
            retrieve = self.session.get(self.task["PRODUCT"])
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.collect()

        if retrieve.status_code == 200:
            self.start = time.time()
            logger.warning(SITE,self.taskID,'Got product page')
            try:
                logger.prepare(SITE,self.taskID,'Getting product data...')
                soup = BeautifulSoup(retrieve.text, "html.parser")
                self.productTitle = soup.find("title").text
                self.productImage = soup.find("img", {"id": "image-0"})["src"]
                self.atcUrl = soup.find("form", {"id": "product_addtocart_form"})[
                    "action"].replace("checkout/cart", "oxajax/cart")
                self.formKey = soup.find("input", {"name": "form_key"})["value"]
                self.productId = soup.find("input", {"name": "product"})["value"]
                self.productPrice = soup.find("span",{"class":"price"}).text
                self.attributeId = soup.find("select", {
                                            "class": "required-entry super-attribute-select no-display swatch-select"})["id"].split("attribute")[1]
    
                regex = r"{\"attributes\":(.*?)}}\)"
                matches = re.search(regex, retrieve.text, re.MULTILINE)
                if matches:
                    productData = json.loads(
                        matches.group()[:-1])["attributes"][self.attributeId]
    
                    allSizes = []
                    sizes = []
                    for s in productData["options"]:
                        allSizes.append('{}:{}:{}'.format(s["label"],s["products"][0],s["id"]))
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
                                    logger.warning(SITE,self.taskID,f'Found Size => {self.size}')
        
                    
                    elif self.task["SIZE"].lower() == "random":
                        selected = random.choice(allSizes)
                        self.size = selected.split(":")[0]
                        self.sizeID = selected.split(":")[2]
                        self.option = selected.split(":")[1]
                        logger.warning(SITE,self.taskID,f'Found Size => {self.size}')

                
                else:
                    logger.error(SITE,self.taskID,'Size Not Found')
                    time.sleep(int(self.task["DELAY"]))
                    self.collect()

                        
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
        logger.prepare(SITE,self.taskID,'Carting product...')
        payload = {
            'isAjax': 1,
            'form_key': self.formKey,
            'product': self.productId,
            'related_product': '',
            f'super_attribute[{self.attributeId}]': self.sizeID,
            'return_url': ''
        }

        try:
            postCart = self.session.post(self.atcUrl, data=payload, headers={
                'authority': 'www.allikestore.com',
                'accept-language': 'en-US,en;q=0.9',
                'origin': 'https://www.allikestore.com',
                'referer': self.task["PRODUCT"],
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'x-requested-with': 'XMLHttpRequest'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()
        
        try:
            splitText = postCart.text.split('({')[1].split('})')[0]
            data = json.loads('{' + splitText + '}')
            status = data["status"]
        except:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

        if postCart.status_code == 200 and data["status"] == "SUCCESS":
            updateConsoleTitle(True,False,SITE)
            logger.warning(SITE,self.taskID,'Successfully carted')
            if self.task["PAYMENT"].lower() == "paypal":
                self.method()
            else:
                self.method()
        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

    def ppExpress(self):
        
        try:
            startExpress = self.session.get('https://www.allikestore.com/default/paypal/express/start/button/1/',headers={
                'authority': 'www.allikestore.com',
                'referer': self.task["PRODUCT"],
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()



        self.end = time.time() - self.start
        if "paypal" in startExpress.url:
            updateConsoleTitle(False,True,SITE)
            logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')

            url = storeCookies(startExpress.url,self.session)

            
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
            self.ppExpress()

    def method(self):
        logger.prepare(SITE,self.taskID,'Submitting checkout method...')
        try:
            postMethod = self.session.post('https://www.allikestore.com/default/checkout/onepage/saveMethod/', data={"method": "guest"}, headers={
                'authority': 'www.allikestore.com',
                'referer': 'https://www.allikestore.com/default/checkout/onepage/',
                'x-requested-with': 'XMLHttpRequest',
                'accept':'text/javascript, text/html, application/xml, text/xml, */*'
            })
            postMethod = self.session.post('https://www.allikestore.com/default/checkout/onepage/saveMethod/', data={"method": "guest"}, headers={
                'authority': 'www.allikestore.com',
                'referer': 'https://www.allikestore.com/default/checkout/onepage/',
                'x-requested-with': 'XMLHttpRequest',
                'accept':'text/javascript, text/html, application/xml, text/xml, */*'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.method()

        if postMethod.status_code == 200:
            logger.warning(SITE,self.taskID,'Saved Method')
            self.billing()
        else:
            logger.error(SITE,self.taskID,'Failed to save method. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.method()

    def billing(self):
        logger.prepare(SITE,self.taskID,'Submitting billing...')
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        countryCode = profile["countryCode"]

        day = random.randint(1,29)
        month = random.randint(1,12)
        year = random.randint(1970,2000)
        payload = {
            'billing[address_id]': '',
            'billing[firstname]': profile["firstName"],
            'billing[lastname]': profile["lastName"],
            'billing[company]': '',
            'billing[email]': profile["email"],
            'billing[street][]': profile["house"] + " " + profile["addressOne"],
            'billing[city]': profile["city"],
            'billing[region_id]': '',
            'billing[region]': profile["region"],
            'billing[postcode]': profile["zip"],
            'billing[country_id]': countryCode,
            'billing[telephone]': profile["phone"],
            'billing[fax]': '',
            'billing[month]': month,
            'billing[day]': day,
            'billing[year]': year,
            'billing[dob]': '{}/{}/{}'.format(month,day,year),
            'billing[customer_password]': '',
            'billing[confirm_password]': '',
            'billing[save_in_address_book]': '1',
            'billing[use_for_shipping]': '1',
            'form_key': self.formKey
        }

        try:
            postBilling = self.session.post('https://www.allikestore.com/default/checkout/onepage/saveBilling/', data=payload, headers={
                'authority': 'www.allikestore.com',
                'accept-language': 'en-US,en;q=0.9',
                'origin': 'https://www.allikestore.com',
                'referer': 'https://www.allikestore.com/default/checkout/onepage/',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'x-requested-with': 'XMLHttpRequest',
                'accept': 'text/javascript, text/html, application/xml, text/xml, */*'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.billing()

        if postBilling.status_code == 200:
            if postBilling.text:
                shippingOptions = json.loads(postBilling.text)
                shippingHtml = shippingOptions["update_section"]["html"]
                soup = BeautifulSoup(shippingHtml,"html.parser")
                self.shippingMethods = soup.find_all('input',{'class':'radio'})
                #self.shippingMethod = shippingMethods[0]["value"]
                logger.warning(SITE,self.taskID,'Successfully set shipping')
                self.shippingMethod()
            else:
                logger.error(SITE,self.taskID,'Failed to set shipping. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.collect()
        elif postBilling.status_code != 200:
            logger.error(SITE,self.taskID,'Failed to set shipping. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.billing()


    def shippingMethod(self):
        logger.prepare(SITE,self.taskID,'Submitting shipping method...')
        try:
            postShippingMethod = self.session.post('https://www.allikestore.com/default/checkout/onepage/saveShippingMethod/', data={"shipping_method": self.shippingMethods[0]["value"], "form_key": self.formKey}, headers={
                'authority': 'www.allikestore.com',
                'accept-language': 'en-US,en;q=0.9',
                'origin': 'https://www.allikestore.com',
                'referer': 'https://www.allikestore.com/default/checkout/onepage/',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'x-requested-with': 'XMLHttpRequest'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.shippingMethod()

        if postShippingMethod.status_code == 200:
            logger.warning(SITE,self.taskID,'Successfully set shipping method')
            if self.task["PAYMENT"] == "paypal":
                self.paypal()
            if self.task["PAYMENT"] == "card":
                soup = BeautifulSoup(json.loads(postShippingMethod.text)["update_section"]["html"],"html.parser")
                paymentConfig = json.loads(soup.find("input",{"id":"payone_creditcard_config"})["value"])
                self.hash = paymentConfig["gateway"]["4"]["hash"]
                self.mid = paymentConfig["gateway"]["4"]["mid"]
                self.aid = paymentConfig["gateway"]["4"]["aid"]
                self.portalid = paymentConfig["gateway"]["4"]["portalid"]
    
                self.creditCard()
        else:
            logger.error(SITE,self.taskID,'Failed to set shipping method')
            time.sleep(int(self.task["DELAY"]))
            self.shippingMethod()

    def paypal(self):
        logger.info(SITE,self.taskID,'Starting [PAYPAL] checkout...')
        try:
            postVerifyPayment = self.session.post('https://www.allikestore.com/default/checkout/onepage/verifyPayment/', data={"payment[method]": "paypal_express", "form_key": self.formKey}, headers={
                'authority': 'www.allikestore.com',
                'accept-language': 'en-US,en;q=0.9',
                'origin': 'https://www.allikestore.com',
                'referer': 'https://www.allikestore.com/default/checkout/onepage/',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'x-requested-with': 'XMLHttpRequest'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.paypal()

        if postVerifyPayment.status_code == 200:
            self.end = time.time() - self.start
            logger.prepare(SITE,self.taskID,'Getting paypal link...')
            try:
                startExpress = self.session.get('https://www.allikestore.com/default/paypal/express/start/', headers={
                    'authority': 'www.allikestore.com',
                    'accept-language': 'en-US,en;q=0.9',
                    'referer': 'https://www.allikestore.com/default/checkout/onepage/',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'x-requested-with': 'XMLHttpRequest'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = None
                self.paypal()
                
            if "paypal" in startExpress.url:
                logger.warning(SITE,self.taskID,'Successfully got paypal link')
                updateConsoleTitle(False,True,SITE)
                logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')
 
                url = storeCookies(startExpress.url,self.session, self.productTitle, self.productImage, self.productPrice)

                
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
            logger.error(SITE,self.taskID,'Failed to verify payment. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.shippingMethod()

    def creditCard(self):
        logger.info(SITE,self.taskID,'Starting [CREDIT CARD] checkout...')
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        number = profile["card"]["cardNumber"]
        if str(number[0]) == "3":
            cType = 'A'
        if str(number[0]) == "4":
            cType = 'V'
        if str(number[0]) == "5":
            cType = 'M'
        if str(number[0]) == "6":
            cType = 'M' 

        cardplan = profile["card"]["cardNumber"]
        cardmonth = profile["card"]["cardMonth"]
        cardyear = profile["card"]["cardYear"]
        cvv = profile["card"]["cardCVV"]
        url = f'https://secure.pay1.de/client-api/?aid={self.aid}&encoding=UTF-8&errorurl=&hash={self.hash}&integrator_name=&integrator_version=&key=&language=&mid={self.mid}&mode=live&portalid={self.portalid}&request=creditcardcheck&responsetype=JSON&solution_name=&solution_version=&storecarddata=yes&successurl=&cardpan={cardplan}&cardexpiremonth={cardmonth}&cardexpireyear={cardyear}&cardtype={cType}&channelDetail=payoneHosted&cardcvc2={cvv}&callback_method=PayoneGlobals.callback'
        logger.prepare(SITE,self.taskID,'Getting SecurePay details...')
        try:
            securePay = self.session.get(url,headers={
                'Accept':'*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
                'Host': 'secure.pay1.de',
                'Referer': 'https://secure.pay1.de/client-api/js/v1/payone_iframe.html?1592385243729',
                'Sec-Fetch-Dest': 'script',
                'Sec-Fetch-Mode': 'no-cors',
                'Sec-Fetch-Site': 'same-origin',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.creditCard()

        if securePay.status_code == 200:
            split = securePay.text.split('PayoneGlobals.callback(')[1]
            secure = json.loads(split.split(');')[0])
            logger.warning(SITE,self.taskID,'Got SecurePay details')

            verifyPayload = {
                'payment[method]': 'payone_creditcard',
                'payone_creditcard_cc_type_select': '4_V',
                'payment[cc_type]': secure["cardtype"],
                'payment[payone_pseudocardpan]': secure["pseudocardpan"],
                'payment[payone_cardexpiredate]':secure["cardexpiredate"],
                'payment[cc_number_enc]': secure["truncatedcardpan"],
                'payment[payone_config_payment_method_id]': 4,
                'payment[payone_config]': {"gateway":{"4":{"aid":self.aid,"encoding":"UTF-8","errorurl":"","hash":self.hash,"integrator_name":"","integrator_version":"","key":"","language":"","mid":self.mid,"mode":"live","portalid":self.portalid,"request":"creditcardcheck","responsetype":"JSON","solution_name":"","solution_version":"","storecarddata":"yes","successurl":""}}},
                'payment[payone_config_cvc]': {"4_V":"always","4_M":"always"},
                'form_key': self.formKey,
            }

            logger.prepare(SITE,self.taskID,'Verifiyng payment...')
            try:
                verifyPayment = self.session.post('https://www.allikestore.com/default/payone_core/checkout_onepage/verifyPayment/',data=verifyPayload,headers={
                    'authority': 'www.allikestore.com',
                    'accept-language': 'en-US,en;q=0.9',
                    'referer': 'https://www.allikestore.com/default/checkout/onepage/',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'x-requested-with': 'XMLHttpRequest'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.creditCard()

            if verifyPayment.status_code == 200:
                logger.warning(SITE,self.taskID,'Payment Verified')
                savePayload = {
                    'payment[method]': 'payone_creditcard',
                    'payone_creditcard_cc_type_select': '4_V',
                    'payment[cc_type]': secure["cardtype"],
                    'payment[payone_pseudocardpan]': secure["pseudocardpan"],
                    'payment[payone_cardexpiredate]':secure["cardexpiredate"],
                    'payment[cc_number_enc]': secure["truncatedcardpan"],
                    'payment[payone_config_payment_method_id]': 4,
                    'payment[payone_config]': {"gateway":{"4":{"aid":self.aid,"encoding":"UTF-8","errorurl":"","hash":self.hash,"integrator_name":"","integrator_version":"","key":"","language":"","mid":self.mid,"mode":"live","portalid":self.portalid,"request":"creditcardcheck","responsetype":"JSON","solution_name":"","solution_version":"","storecarddata":"yes","successurl":""}}},
                    'payment[payone_config_cvc]': {"4_V":"always","4_M":"always"},
                    'form_key': self.formKey,
                    'agreement[2]': 1,
                    'agreement[4]': 1,
                    'customer_order_comment': ''
                }
                
                logger.prepare(SITE,self.taskID,'Saving Order...')
                try:
                    saveOrder = self.session.post('https://www.allikestore.com/default/checkout/onepage/saveOrder/',data=savePayload,headers={
                        'authority': 'www.allikestore.com',
                        'accept-language': 'en-US,en;q=0.9',
                        'referer': 'https://www.allikestore.com/default/checkout/onepage/',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-origin',
                        'x-requested-with': 'XMLHttpRequest'
                    })
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    log.info(e)
                    logger.error(SITE,self.taskID,'Error: {}'.format(e))
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    self.creditCard()

                if saveOrder.status_code == 200:
                    logger.warning(SITE,self.taskID,'Order saved')
                    response = json.loads(saveOrder.text)
                    if response["success"] == False:
                        logger.error(SITE,self.taskID,'ERROR => {}'.format(response["error_messages"]))
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

                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                        time.sleep(int(self.task["DELAY"]))
                        self.creditCard()

                    elif response["success"] == True:
                        self.end = time.time() - self.start
                        updateConsoleTitle(False,True,SITE)
                        logger.alert(SITE,self.taskID,'Sending Card checkout to Discord!')
                        
                        url = storeCookies(response["redirect"],self.session, self.productTitle, self.productImage, self.productPrice)
    
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
                        sendNotification(SITE,self.productTitle)
                        while True:
                            pass
                else:
                    logger.error(SITE,self.taskID,'Couldnt save order. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.creditCard()

            else:
                logger.error(SITE,self.taskID,'Couldnt verify card. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.creditCard()
