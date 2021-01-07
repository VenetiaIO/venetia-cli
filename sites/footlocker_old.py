import requests
from bs4 import BeautifulSoup
from datetime import timezone, datetime
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

from utils.logger import logger
from utils.webhook import discord
from utils.log import log
from utils.datadome import datadome
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies, updateConsoleTitle,scraper, footlocker_snare)
SITE = 'FOOTLOCKER'


class FOOTLOCKER_OLD:
    def __init__(self, task,taskName):
        self.task = task
        self.session = requests.session()
        self.taskID = taskName

        twoCap = loadSettings()["2Captcha"]
        # self.session = scraper()
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        self.countryCode = profile['countryCode'].lower()

        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
        self.baseSku = self.task['PRODUCT']

        if self.countryCode == 'fr':
            self.baseUrl = 'https://www.footlocker.fr'
            self.baseUrl2 = 'https://www.footlocker.de/INTERSHOP/web/FLE/Footlocker-Footlocker_FR-Site/en_GB/-/EUR/'
        if self.countryCode == 'de':
            self.baseUrl = 'https://www.footlocker.de'
            self.baseUrl2 = 'https://www.footlocker.de/INTERSHOP/web/FLE/Footlocker-Footlocker_DE-Site/en_GB/-/EUR/'
        if self.countryCode == 'nl':
            self.baseUrl = 'https://www.footlocker.nl'
            self.baseUrl2 = 'https://www.footlocker.de/INTERSHOP/web/FLE/Footlocker-Footlocker_NL-Site/en_GB/-/EUR/'
        if self.countryCode == 'gb':
            self.baseUrl = 'https://www.footlocker.co.uk'
            self.baseUrl2 = 'https://www.footlocker.co.uk/INTERSHOP/web/FLE/Footlocker-Footlocker_GB-Site/en_GB/-/GBP/'
        if self.countryCode == 'au':
            self.baseUrl = 'https://www.footlocker.com.au'
            self.baseUrl2 = 'https://www.footlocker.com.au/INTERSHOP/web/FLE/Footlocker-Footlocker_AU-Site/en_GB/-/AUD/'
        if self.countryCode == 'sg':
            self.baseUrl = 'https://www.footlocker.co.uk'
            self.baseUrl2 = 'https://www.footlocker.sg/INTERSHOP/web/FLE/FootlockerAsiaPacific-Footlocker_SG-Site/en_GB/-/SGD/'
        if self.countryCode == 'my':
            self.baseUrl = 'https://www.footlocker.my'
            self.baseUrl2 = 'https://www.footlocker.my/INTERSHOP/web/FLE/FootlockerAsiaPacific-Footlocker_MY-Site/en_GB/-/MYR/'
        if self.countryCode == 'hk':
            self.baseUrl = 'https://www.footlocker.hk'
            self.baseUrl2 = 'https://www.footlocker.hk/INTERSHOP/web/FLE/FootlockerAsiaPacific-Footlocker_HK-Site/en_GB/-/HKD/'
        
        self.retrieveSizes()

    # def collect(self):
        # logger.prepare(SITE,self.taskID,'Getting product page...')
        # try:
            # retrieve = self.session.get(self.task["PRODUCT"])
        # except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            # log.info(e)
            # logger.error(SITE,self.taskID,'Error: {}'.format(e))
            # self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            # time.sleep(int(self.task["DELAY"]))
            # self.collect()
# 
# 
        # if retrieve.status_code == 200:
            # self.start = time.time()
            # logger.warning(SITE,self.taskID,'Got product page')
            # try:
                # logger.prepare(SITE,self.taskID,'Getting product data...')
                # soup = BeautifulSoup(retrieve.text, "html.parser")
                # self.syncToken = soup.find('input',{'name':'SynchronizerToken'})['value']
                # self.relayCat = 'Relay42_Category'  #soup.find('input',{'value':'Product Pages'})['name']
                # self.tabgroup = retrieve.text.split('''_st('addTagProperties', {position:"0",id:"''')[1].split('",')[0]
                # self.baseSku = retrieve.text.split('ViewProduct-ProductVariationSelect?BaseSKU=')[1].split('&')[0]
            #   
            # except Exception as e:
            #    log.info(e)
            #    logger.error(SITE,self.taskID,'Failed to scrape page (Most likely out of stock). Retrying...')
            #    time.sleep(int(self.task["DELAY"]))
            #    self.collect()
# 
            # self.retrieveSizes()
# 
        # else:
            # try:
                # status = retrieve.status_code
            # except:
                # status = 'Unknown'
            # logger.error(SITE,self.taskID,f'Failed to get product page => {status}. Retrying...')
            # time.sleep(int(self.task["DELAY"]))
            # self.collect()


    def retrieveSizes(self):
        logger.prepare(SITE,self.taskID,'Getting product data...')
        self.start = time.time()
        self.relayCat = 'Relay42_Category'  #soup.find('input',{'value':'Product Pages'})['name']
        self.productImage = f'https://images.footlocker.com/is/image/FLEU/{self.baseSku}_01?wid=763&hei=538&fmt=png-alpha'
        try:
            retrieveSizes = self.session.get(f'{self.baseUrl2}ViewProduct-ProductVariationSelect?BaseSKU={self.baseSku}&InventoryServerity=ProductDetail',headers={
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-language": "en-US,en;q=0.9",
                "sec-ch-ua": "\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"",
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-requested-with": "XMLHttpRequest",
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.retrieveSizes()

        if retrieveSizes.status_code == 503:
            logger.info(SITE,self.taskID,'Queue...')
            time.sleep(30)
            self.retrieveSizes()

        if retrieveSizes.status_code == 404:
            logger.error(SITE,self.taskid,'Sold Out. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.retrieveSizes()


        try:
            data = retrieveSizes.json()
        except Exception as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Failed to get product data. Retrying...')
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.retrieveSizes()
        
        if retrieveSizes.status_code == 200:
            if 'sold out' in retrieveSizes.text.lower():
                logger.error(SITE,self.taskID,'Sold Out. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.retrieveSizes()

            try:
                htmlContent = data['content'].replace('\n','').replace("\\", "")
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to get product data. Retrying...')
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                self.retrieveSizes()
            
            try:
                soup = BeautifulSoup(htmlContent,"html.parser")
                eu_sizes = soup.find_all('section',{'class':'fl-accordion-tab--content'})[0].find_all('button')
            except:
                logger.error(SITE,self.taskID,'Sizes Not Found')
                time.sleep(int(self.task["DELAY"]))
                self.retrieveSizes()

            

            allSizes = []
            sizes = []

            for s in eu_sizes:
                try:
                    if 'not-available' in s['class']:
                        pass
                    else:
                        size = s.find('span').text
                        sizeSku = s['data-product-size-select-item']
                        allSizes.append('{}:{}'.format(size,sizeSku))
                        sizes.append(size)
                except:
                    pass

            self.tabgroup = self.baseSku + allSizes[0].split(':')[1]


            if len(sizes) == 0:
                logger.error(SITE,self.taskID,'Sizes Not Found')
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
                            self.sizeSku = size.split(":")[1]
                            logger.warning(SITE,self.taskID,f'Found Size => {self.size}')

            
            elif self.task["SIZE"].lower() == "random":
                selected = random.choice(allSizes)
                self.size = selected.split(":")[0]
                self.sizeSku = selected.split(":")[1]
                logger.warning(SITE,self.taskID,f'Found Size => {self.size}')

            self.addToCart()

    
                
            

    def addToCart(self):
        logger.prepare(SITE,self.taskID,'Carting product...')
        params = {
            'Ajax': True,
            self.relayCat: 'Category Pages',
            f'acctab-tabgroup-{self.tabgroup}': None,
            f'Quantity_{self.sizeSku}': 1,
            'SKU': self.sizeSku
        }

        try:
            atcResponse = self.session.post(f'{self.baseUrl}/en/addtocart',params=params,headers={
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-language": "en-US,en;q=0.9",
                "sec-ch-ua": "\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"",
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-requested-with": "XMLHttpRequest",
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

        if atcResponse.status_code == 403:
            logger.error(SITE,self.taskID,'Blocked by DataDome (Solving Challenge...)')
            try:
                challengeUrl = atcResponse.json()['url']
            except:
                logger.error(SITE,self.taskID,'Failed to get challenge url. Sleeping...')
                time.sleep(10)
                self.addToCart()
            cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl)
            while(cookie['cookie'] == None):
                del self.session.cookies["datadome"]
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl)
                

            del self.session.cookies["datadome"]
            self.session.cookies["datadome"] = cookie['cookie']
            self.addToCart()

        elif atcResponse.status_code == 200:
            try:
                self.syncToken = atcResponse.text.split('ViewCart-Checkout?SynchronizerToken=')[1].split('\\"')[0]
                self.productPrice = atcResponse.text.split('price:\\"')[1].split('\\"')[0]
            except:
                logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.addToCart()

            logger.warning(SITE,self.taskID,'Successfully carted product')
            self.checkoutDispatch()

        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()


    def checkoutDispatch(self):
        logger.prepare(SITE,self.taskID,'Getting checkout data...')

        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        self.countryCode = profile['countryCode'].lower()

        try:
            checkoutOverviewPage = self.session.get(f'{self.baseUrl}/en/checkout-overview?SynchronizerToken=' + self.syncToken,headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-language": "en-US,en;q=0.9",
                "sec-ch-ua": "\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"",
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.checkoutDispatch()

        if checkoutOverviewPage.status_code == 403:
            logger.error(SITE,self.taskID,'Blocked by DataDome (Solving Challenge...)')
            challengeUrl = checkoutOverviewPage.json()['url']
            cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl)
            while(cookie == None): cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl)

            del self.session.cookies["datadome"]
            self.session.cookies["datadome"] = cookie['cookie']
            self.checkoutDispatch()

        if checkoutOverviewPage.status_code in [200,302]:
            self.referer = checkoutOverviewPage.url
            try:

                soup = BeautifulSoup(checkoutOverviewPage.text, "html.parser")
                PaymentServiceSelection = soup.find('input',{'name':'PaymentServiceSelection'})['value']
                shipMethodUUID = soup.find('input',{'name':'ShippingMethodUUID'})['value']
                shippingAddressId = soup.find('input',{'name':'shipping_AddressID'})['value']
                # billingAddressId = soup.find('input',{'name':'billing_AddressID'})['value']
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to get checkout data. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.checkoutDispatch()
            
            logger.warning(SITE,self.taskID,'Got checkout data')

        else:
            logger.error(SITE,self.taskID,'Failed to get checkout data. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.checkoutDispatch()

        logger.prepare(SITE,self.taskID,'Submitting shipping')
        self.deviceId = footlocker_snare(self.task['PRODUCT'].split('/en')[0])
        form = "SynchronizerToken={}&isshippingaddress=&billing_Title=common.account.salutation.mr.text&billing_FirstName={}&billing_LastName={}&billing_CountryCode={}&billing_Address1={}&billing_Address2={}&billing_Address3={}&billing_City={}&billing_PostalCode={}&billing_PhoneHome={}&billing_BirthdayRequired=true&billing_Birthday_Day={}&billing_Birthday_Month={}&billing_Birthday_Year={}&email_Email={}&billing_ShippingAddressSameAsBilling=true&isshippingaddress=&shipping_Title=common.account.salutation.mr.text&shipping_FirstName=&shipping_LastName=&SearchTerm=&shipping_CountryCode={}&shipping_Address1=&shipping_Address2=&shipping_Address3=&shipping_City=&shipping_PostalCode=&shipping_PhoneHome=&shipping_AddressID={}&CheckoutRegisterForm_Password=&promotionCode=&PaymentServiceSelection={}&UserDeviceTypeForPaymentRedirect=Desktop&UserDeviceFingerprintForPaymentRedirect={}&ShippingMethodUUID={}&termsAndConditions=on&GDPRDataComplianceRequired=true&sendOrder=".format(
            self.syncToken,
            profile['firstName'],
            profile['lastName'],
            profile['countryCode'],
            profile['addressOne'],
            profile['house'],
            profile['addressTwo'],
            profile['city'],
            profile['zip'],
            profile['phone'],
            random.randint(1,25),#day
            random.randint(1,12), #month
            random.randint(1970,2000), #year
            profile['email'],
            profile['countryCode'],
            shippingAddressId,
            PaymentServiceSelection,
            self.deviceId,
            shipMethodUUID
        )
        # Finish form 

        try:
            checkoutOverviewDispatch = self.session.post(f'{self.baseUrl2}ViewCheckoutOverview-Dispatch',data=form,headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-language": "en-US,en;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "cache-control": "max-age=0",
                "content-type": "application/x-www-form-urlencoded",
                "sec-ch-ua": "\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"",
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "referer":self.referer,
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.checkoutDispatch()

        print(checkoutOverviewDispatch, checkoutOverviewDispatch.url)
        if checkoutOverviewDispatch.status_code == 403:
            logger.error(SITE,self.taskID,'Blocked by DataDome (Solving Challenge...)')
            challengeUrl = checkoutOverviewDispatch.json()['url']
            cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl)
            while(cookie == None): cookie = datadome.reCaptchaMethod(SITE,self.taskID,self.session,challengeUrl)

            del self.session.cookies["datadome"]
            self.session.cookies["datadome"] = cookie['cookie']
            self.checkoutDispatch()

        
        if checkoutOverviewDispatch.status_code in [200,302] and 'OrderID' in checkoutOverviewDispatch.url:
            logger.warning(SITE,self.taskID,'Shipping submitted')

            self.responseText = checkoutOverviewDispatch.text
            self.responseUrl = checkoutOverviewDispatch.url

            self.payment()
        else:
            logger.error(SITE,self.taskID,'Failed to submit shipping. Retrying...')
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.checkoutDispatch()

    def payment(self):
        logger.prepare(SITE,self.taskID,'Submitting payment details...')

        try:
            soup = BeautifulSoup(self.responseText, "html.parser")

            data = {
                'SynchronizerToken':self.syncToken,
                'riskdata.basket.item1.itemID': soup.find('input',{'name':'riskdata.basket.item1.itemID'})['value'],
                'riskdata.basket.item1.sku': soup.find('input',{'name':'riskdata.basket.item1.sku'})['value'],
                'riskdata.basket.item1.productTitle': soup.find('input',{'name':'riskdata.basket.item1.productTitle'})['value'],
                'riskdata.basket.item1.amountPerItem': soup.find('input',{'name':'riskdata.basket.item1.amountPerItem'})['value'],
                'riskdata.basket.item1.currency': soup.find('input',{'name':'riskdata.basket.item1.currency'})['value'],
                'riskdata.basket.item1.quantity': soup.find('input',{'name':'riskdata.basket.item1.quantity'})['value'],
                'riskdata.basket.item1.color': soup.find('input',{'name':'riskdata.basket.item1.color'})['value'],
                'riskdata.basket.item1.size': soup.find('input',{'name':'riskdata.basket.item1.size'})['value'],
                'shopperReference': soup.find('input',{'name':'shopperReference'})['value'],
                'shopperEmail': soup.find('input',{'name':'shopperEmail'})['value'],
                'shopper.dateOfBirthDayOfMonth': soup.find('input',{'name':'shopper.dateOfBirthDayOfMonth'})['value'],
                'shopper.dateOfBirthMonth': soup.find('input',{'name':'shopper.dateOfBirthMonth'})['value'],
                'shopper.dateOfBirthYear': soup.find('input',{'name':'shopper.dateOfBirthYear'})['value'],
                'shopperLocale': soup.find('input',{'name':'shopperLocale'})['value'],
                'shopper.firstName': soup.find('input',{'name':'shopper.firstName'})['value'],
                'shopper.LastName': soup.find('input',{'name':'shopper.LastName'})['value'],
                'shopper.telephoneNumber': soup.find('input',{'name':'shopper.telephoneNumber'})['value'],
                'sessionValidity': soup.find('input',{'name':'sessionValidity'})['value'],
                'shopperType': soup.find('input',{'name':'shopperType'})['value'],
                'shopper.gender': soup.find('input',{'name':'shopper.gender'})['value'],
                'billingAddressType': soup.find('input',{'name':'billingAddressType'})['value'],
                'billingAddress.street': soup.find('input',{'name':'billingAddress.street'})['value'],
                'billingAddress.city': soup.find('input',{'name':'billingAddress.city'})['value'],
                'billingAddress.houseNumberOrName': soup.find('input',{'name':'billingAddress.houseNumberOrName'})['value'],
                'billingAddress.stateOrProvince': soup.find('input',{'name':'billingAddress.stateOrProvince'})['value'],
                'billingAddress.country': soup.find('input',{'name':'billingAddress.country'})['value'],
                'billingAddress.postalCode': soup.find('input',{'name':'billingAddress.postalCode'})['value'],
                'deliveryAddressType': soup.find('input',{'name':'deliveryAddressType'})['value'],
                'deliveryAddress.street': soup.find('input',{'name':'deliveryAddress.street'})['value'],
                'deliveryAddress.city': soup.find('input',{'name':'deliveryAddress.city'})['value'],
                'deliveryAddress.houseNumberOrName': soup.find('input',{'name':'deliveryAddress.houseNumberOrName'})['value'],
                'deliveryAddress.stateOrProvince': soup.find('input',{'name':'deliveryAddress.stateOrProvince'})['value'],
                'deliveryAddress.country': soup.find('input',{'name':'deliveryAddress.country'})['value'],
                'deliveryAddress.postalCode': soup.find('input',{'name':'deliveryAddress.postalCode'})['value'],
                'SynchronizerToken': self.syncToken,
                'merchantReturnData': soup.find('input',{'name':'merchantReturnData'})['value'],
                'shipBeforeDate': soup.find('input',{'name':'shipBeforeDate'})['value'],
                'paymentAmount': soup.find('input',{'name':'paymentAmount'})['value'],
                'merchantReference': soup.find('input',{'name':'merchantReference'})['value'],
                'skinCode': soup.find('input',{'name':'skinCode'})['value'],
                'countryCode': soup.find('input',{'name':'countryCode'})['value'],
                'currencyCode': soup.find('input',{'name':'currencyCode'})['value'],
                'resURL': soup.find('input',{'name':'resURL'})['value'],
                'merchantAccount': soup.find('input',{'name':'merchantAccount'})['value'],
                'recurringContract': soup.find('input',{'name':'recurringContract'})['value'],
                'blockedMethods': soup.find('input',{'name':'blockedMethods'})['value'],
                'merchantSig': soup.find('input',{'name':'merchantSig'})['value'],
            }
        except:
            logger.error(SITE,self.taskID,'Failed to submit payment details.Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.payment()

        try:
            adyenPay = self.session.post('https://live.adyen.com/hpp/pay.shtml',data=data,headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "max-age=0",
                "content-type": "application/x-www-form-urlencoded",
                "sec-ch-ua": "\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"",
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "cross-site",
                "upgrade-insecure-requests": "1",
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.payment()

        if adyenPay.status_code == 200:
            logger.warning(SITE,self.taskID,'Submitted payment details')
            self.responseText = adyenPay.text

            if self.task['PAYMENT'].lower() == 'paypal':
                self.paypalCheckout()
            if self.task['PAYMENT'].lower() == 'card':
                self.cardPayment()
        else:
            logger.error(SITE,self.taskID,'Failed to submit payment details.Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.payment()


    def paypalCheckout(self):
        logger.prepare(SITE,self.taskID,'Getting paypal link...')

        data = {
                'displayGroup': 'paypal',
                'pay': 'pay',
                'paypal.storeOcDetails': False,
                'card.cardNumber': '',
                'card.cardHolderName': '',
                'card.expiryMonth': '',
                'card.expiryYear': '',
                'card.cvcCode': '',
                'card.storeOcDetails': True,
                'sig': '',
                'merchantReference': '',
                'brandCode': 'paypal',
                'paymentAmount': '',
                'currencyCode': '',
                'shipBeforeDate': '',
                'skinCode': '',
                'merchantAccount': '',
                'shopperLocale': '',
                'stage': '',
                'sessionId': '',
                'sessionValidity': '',
                'countryCode': '',
                'shopperEmail': '',
                'shopperReference': '',
                'recurringContract': '',
                'resURL': '',
                'blockedMethods': '',
                'merchantReturnData': '',
                'originalSession': '',
                'billingAddress.street': '',
                'billingAddress.houseNumberOrName': '',
                'billingAddress.city': '',
                'billingAddress.postalCode': '',
                'billingAddress.stateOrProvince': '',
                'billingAddress.country': '',
                'billingAddressType': '',
                'billingAddressSig': '',
                'deliveryAddress.street': '',
                'deliveryAddress.houseNumberOrName': '',
                'deliveryAddress.city': '',
                'deliveryAddress.postalCode': '',
                'deliveryAddress.stateOrProvince': '',
                'deliveryAddress.country': '',
                'deliveryAddressType': '',
                'deliveryAddressSig': '',
                'shopper.firstName': '',
                'shopper.lastName': '',
                'shopper.gender': '',
                'shopper.dateOfBirthDayOfMonth': '',
                'shopper.dateOfBirthMonth': '',
                'shopper.dateOfBirthYear': '',
                'shopper.telephoneNumber': '',
                'shopperType': '',
                'shopperSig': '',
                'riskdata.basket.item1.size': '',
                'riskdata.basket.item1.itemID': '',
                'riskdata.basket.item1.amountPerItem': '',
                'riskdata.basket.item1.quantity': '',
                'riskdata.basket.item1.productTitle': '',
                'riskdata.basket.item1.color': '',
                'merchantIntegration.type': '',
                'riskdata.basket.item1.sku': '',
                'riskdata.basket.item1.currency': '',
                'referrerURL': '',
                'dfValue': '',
                'usingFrame': '',
                'usingPopUp': '',
                'shopperBehaviorLog': '',
        }



        soup = BeautifulSoup(self.responseText, "html.parser")
        for s in data.keys():
            try:
                val = soup.find('input',{'name':s})['value']
                data[s] = val
            except:
                pass
        data['displayGroup'] = 'paypal'
        data['brandCode'] = 'paypal'
        data['shopperBehaviorLog'] = {"numberBind":"1","holderNameBind":"1","cvcBind":"1","activate":"12","deactivate":"10"}
        data['dfValue'] = 'ryEGX8eZpJ0030000000000000BTWDfYZVR30089146776cVB94iKzBGLWMw84D0Ss5S16Goh5Mk0045zgp4q8JSa00000qZkTE00000q6IQbnyNfpG2etdcqzfW:40'
        data['referrerURL'] = self.baseUrl

        self.productTitle = data['riskdata.basket.item1.productTitle']
        self.productPrice = '{} {}'.format(self.productPrice, data['currencyCode'])

        try:
            paypalRedirect = self.session.post('https://live.adyen.com/hpp/redirectPayPal.shtml',data=data,headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "max-age=0",
                "content-type": "application/x-www-form-urlencoded",
                "sec-ch-ua": "\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"",
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "cross-site",
                "upgrade-insecure-requests": "1",
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.paypalCheckout()

        if paypalRedirect.status_code == 200 and 'paypal' in paypalRedirect.url:
            logger.warning(SITE,self.taskID, 'Got paypal link')
            self.end = time.time() - self.start

            updateConsoleTitle(False,True,SITE)
            logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')
            url = storeCookies(paypalRedirect.url,self.session, self.productTitle, self.productImage, self.productPrice)
            
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
                    speed=self.end,
                    region=self.countryCode
                )
                sendNotification(SITE,self.productTitle)
                while True:
                    pass
            except Exception as e:
                log.info(e)
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
            logger.error(SITE,self.taskID,'Failed to get paypal link. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.paypalCheckout()


    def cardPayment(self):
        logger.info(SITE,self.taskID,'Starting [CARD] checkout...')

        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()

        data = {
                'displayGroup': '',
                'paypal.storeOcDetails': False,
                'card.cardNumber': '',
                'card.cardHolderName': '',
                'card.expiryMonth': '',
                'card.expiryYear': '',
                'card.cvcCode': '',
                'sig': '',
                'merchantReference': '',
                'brandCode': 'paypal',
                'paymentAmount': '',
                'currencyCode': '',
                'shipBeforeDate': '',
                'skinCode': '',
                'merchantAccount': '',
                'shopperLocale': '',
                'stage': '',
                'sessionId': '',
                'sessionValidity': '',
                'countryCode': '',
                'shopperEmail': '',
                'shopperReference': '',
                'recurringContract': '',
                'resURL': '',
                'blockedMethods': '',
                'merchantReturnData': '',
                'originalSession': '',
                'billingAddress.street': '',
                'billingAddress.houseNumberOrName': '',
                'billingAddress.city': '',
                'billingAddress.postalCode': '',
                'billingAddress.stateOrProvince': '',
                'billingAddress.country': '',
                'billingAddressType': '',
                'billingAddressSig': '',
                'deliveryAddress.street': '',
                'deliveryAddress.houseNumberOrName': '',
                'deliveryAddress.city': '',
                'deliveryAddress.postalCode': '',
                'deliveryAddress.stateOrProvince': '',
                'deliveryAddress.country': '',
                'deliveryAddressType': '',
                'deliveryAddressSig': '',
                'shopper.firstName': '',
                'shopper.lastName': '',
                'shopper.gender': '',
                'shopper.dateOfBirthDayOfMonth': '',
                'shopper.dateOfBirthMonth': '',
                'shopper.dateOfBirthYear': '',
                'shopper.telephoneNumber': '',
                'shopperType': '',
                'shopperSig': '',
                'riskdata.basket.item1.size': '',
                'riskdata.basket.item1.itemID': '',
                'riskdata.basket.item1.amountPerItem': '',
                'riskdata.basket.item1.quantity': '',
                'riskdata.basket.item1.productTitle': '',
                'riskdata.basket.item1.color': '',
                'merchantIntegration.type': '',
                'riskdata.basket.item1.sku': '',
                'riskdata.basket.item1.currency': '',
                'referrerURL': '',
                'dfValue': '',
                'usingFrame': '',
                'usingPopUp': '',
                'shopperBehaviorLog': '',
        }



        soup = BeautifulSoup(self.responseText, "html.parser")
        for s in data.keys():
            try:
                val = soup.find('input',{'name':s})['value']
                data[s] = val
            except:
                pass
        data['displayGroup'] = 'card'
        data['brandCode'] = 'brandCodeUndef'
        data['shopperBehaviorLog'] = {"numberBind":"1","holderNameBind":"1","cvcBind":"1","deactivate":"3","activate":"3","numberFieldFocusCount":"1","numberFieldLog":"fo@130,KN@537,KN@540,KN@549,KN@555,KN@565,KN@567,KN@575,KN@579,KN@588,KN@590,KN@601,KN@604,KN@629,KN@631,KN@633,KN@634,KU@638,ch@638,bl@638","numberFieldKeyCount":"17","numberUnkKeysFieldLog":"9@638","numberFieldChangeCount":"1","numberFieldEvHa":"total=0","numberFieldBlurCount":"1","holderNameFieldFocusCount":"1","holderNameFieldLog":"fo@638,KL@649,KL@650,KL@651,KL@655,KL@655,KL@656,Ks@657,KL@659,KL@660,KL@661,KL@663,KL@664,KL@666,KL@669,KL@670,KL@672,KU@676,ch@676,bl@676","holderNameFieldKeyCount":"17","holderNameUnkKeysFieldLog":"9@676","holderNameFieldChangeCount":"1","holderNameFieldEvHa":"total=0","holderNameFieldBlurCount":"1","cvcFieldFocusCount":"1","cvcFieldLog":"fo@811,cl@812,KN@826,KN@829,KN@831,ch@840,bl@840","cvcFieldClickCount":"1","cvcFieldKeyCount":"3","cvcFieldChangeCount":"1","cvcFieldEvHa":"total=0","cvcFieldBlurCount":"1"}
        data['dfValue'] = 'ryEGX8eZpJ0030000000000000BTWDfYZVR30089146776cVB94iKzBGLWMw84D0Ss5S16Goh5Mk0045zgp4q8JSa00000qZkTE00000q6IQbnyNfpG2etdcqzfW:40'
        data['referrerURL'] = self.baseUrl

        data['card.cardNumber'] = profile['card']['cardNumber'] #may need to add spaces between each 4 numbers.
        data['card.cardHolderName'] = profile['firstName'] + ' ' + profile['lastName']
        data['card.expiryMonth'] = profile['card']['cardMonth']
        data['card.expiryYear'] = profile['card']['cardYear']
        data['card.cvcCode'] = profile['card']['cardCVV']

        self.productTitle = data['riskdata.basket.item1.productTitle']
        self.productPrice = '{} {}'.format(self.productPrice, data['currencyCode'])



        logger.prepare(SITE,self.taskID,'Submitting payment...')
        try:
            completeCard = self.session.post('https://live.adyen.com/hpp/completeCard.shtml',data=data,headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "max-age=0",
                "content-type": "application/x-www-form-urlencoded",
                "sec-ch-ua": "\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"",
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "cross-site",
                "upgrade-insecure-requests": "1",
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.paypalCheckout()

        if completeCard.status_code == 200:
            # self.PaReq = completeCard.url.split('&paRequest=')[1].split('&')[0]
            # self.MD = completeCard.url.split('&md=')[1].split('&')[0]
            try:
                payerAuth = self.session.get(completeCard.url, headers={
                    'Referer':'https://live.adyen.com/hpp/pay.shtml',
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.cardPayment()

            try:
                soup = BeautifulSoup(payerAuth.text, "html.parser")
                self.pareq = soup.find('input',{'name':'PaReq'})['value']
                self.MD= soup.find('input',{'name':'MD'})['value']
            except:
                logger.error(SITE,self.taskID,'Failed to get checkout details. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.cardPayment()
            
            Dpayload = {
               "TermUrl":"https://live.adyen.com/hpp/complete3dIntermediate.shtml",
               "PaReq":self.pareq,
               "MD":self.MD,
               "shopperBehaviorLog":""
            }

            try:
                payerAuth = self.session.post('https://verifiedbyvisa.acs.touchtechpayments.com/v1/payerAuthentication', data=Dpayload, headers={
                    'referer':'https://live.adyen.com/',
                    'content-type': 'application/x-www-form-urlencoded',
                    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.cardPayment()

            if payerAuth.status_code == 200:
                soup = BeautifulSoup(payerAuth.text,"html.parser")
                # print(soup)
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
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    log.info(e)
                    logger.error(SITE,self.taskID,'Error: {}'.format(e))
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    self.cardPayment()

                if 'You are being rate limited.' in poll.text:
                    logger.error(SITE,self.taskID,'Rate limited. Sleeping...')
                    # time.sleep(int(poll.json()['retry_after']))
                    self.cardPayment()

                if poll.json()["status"] == "blocked":
                    logger.error(SITE,self.taskID,'Card Blocked. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.cardPayment()
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
                    self.cardPayment()
                if poll.json()["status"] == "success":
                    authToken = poll.json()['authToken']
                else:
                    logger.error(SITE,self.taskID,'Failed to retrieve auth token for 3DS. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.cardPayment()

                authToken = poll.json()['authToken']
                logger.warning(SITE,self.taskID,'3DS Authorised')
        
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
                    self.cardPayment()

                pares = r.json()['Response']

                data = {"MD":self.MD, "PaRes":pares}
                try:
                    r = self.session.post('https://live.adyen.com/hpp/complete3dIntermediate.shtml',headers={
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
                    self.cardPayment()

                if r.status_code in [200,302]:
                    try:
                        complete3d = self.session.post('https://live.adyen.com/hpp/complete3d.shtml',data=data,headers={
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                            'content-type': 'application/x-www-form-urlencoded',
                            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                            'origin': 'https://verifiedbyvisa.acs.touchtechpayments.com',
                            'referer':'https://live.adyen.com/hpp/complete3dIntermediate.shtml',
                        })
                    except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                        log.info(e)
                        logger.error(SITE,self.taskID,'Error: {}'.format(e))
                        time.sleep(int(self.task["DELAY"]))
                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                        self.cardPayment()

                    # if complete3d.status_code == 200:
                        # self.orderId = complete3d.url.split('?OrderID=')[1].split('&')[0]


                    self.end = time.time() - self.start
                    updateConsoleTitle(False,True,SITE)
                    logger.alert(SITE,self.taskID,'Completed Card Checkout')
                    

                    try:
                        discord.success(
                            webhook=loadSettings()["webhook"],
                            site=SITE,
                            url=self.baseUrl,
                            image=self.productImage,
                            title=self.productTitle,
                            size=self.size,
                            price=self.productPrice,
                            paymentMethod='Card',
                            profile=self.task["PROFILE"],
                            product=self.task["PRODUCT"],
                            proxy=self.session.proxies,
                            speed=self.end,
                            region=self.countryCode
                        )
                        sendNotification(SITE,self.productTitle)
                    except Exception as e:
                        log.info(e)
                        pass

                    while True:
                        pass


                else:
                    logger.error(SITE,self.taskID,'Failed to complete checkout. Retrying...')
                    discord.failed(
                        webhook=loadSettings()["webhook"],
                        site=SITE,
                        url=self.baseUrl,
                        image=self.productImage,
                        title=self.productTitle,
                        size=self.size,
                        price=self.productPrice,
                        paymentMethod='Card',
                        profile=self.task["PROFILE"],
                        proxy=self.session.proxies
                    )
                    time.sleep(int(self.task["DELAY"]))
                    self.cardPayment()
            
            else:
                logger.error(SITE,self.taskID,'Failed to get checkout details. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.cardPayment()

        else:
            logger.error(SITE,self.taskID,'Failed to get checkout details. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.cardPayment()