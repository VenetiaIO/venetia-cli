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
    footlocker_snare
)
import utils.config as CONFIG

_SITE_ = 'DISNEY'
SITE = 'Disney'
class DISNEY:
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

        if self.profile['countryCode'].lower() == 'fr':
            self.disneyRegion = 'fr'
        if self.profile['countryCode'].lower() == 'de':
            self.disneyRegion = 'de'
        if self.profile['countryCode'].lower() == 'it':
            self.disneyRegion = 'it'
        if self.profile['countryCode'].lower() == 'es':
            self.disneyRegion = 'es'
        if self.profile['countryCode'].lower() == 'us':
            self.disneyRegion = 'com'
        else:
            self.disneyRegion = 'co.uk'

        self.tasks()
    
    def tasks(self):

        self.monitor()
        self.addToCart()
        self.secKey()
        self.shipKey()
        self.shipMethods()
        self.shipping()

        if self.task['PAYMENT'].strip().lower() == "paypal":
            self.paypal()
        else:
            self.card()

        self.sendToDiscord()

    def findProduct(self):
        self.prepare("Searching for product...")
        while True:
            try:
                response = self.session.get(self.kwUrl, headers={
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue
                # https://www.shopdisney.{}/new?srule=Newest&sz=96&start=0

            try:
                if response.status_code == 200:
                    try:
                        kws = self.task["PRODUCT"].split('|')
                        kws = [x.lower() for x in kws]
                        foundItem = ""
                        soup = BeautifulSoup(response.text,"html.parser")
                        section = soup.find('section',{'class':'catlisting__product-grid js-catlisting-product-grid'})
                        # print(section)
                        row = section.find('div',{'class':'row'}).find_all('div')
                        for r in row:
                            # r = BeautifulSoup(r,"htm.parser")
                            try:
                                p = r.find('a',{'class':'product__linkcontainer js-catlisting-productlink-container no-transform'})
                                title = p['title']
                                link = p['href']
                                title_ = [x.lower() for x in title.split(' ')]
                                if all(kw in title_ for kw in kws):
                                    link = p['href']
                                    foundItem = '{}|{}'.format(title,link)
                            except:
                                pass

                        if len(foundItem) > 0:
                            self.success("Found Product => {}".format(foundItem.split('|')[0]))
                            return foundItem.split('|')
                        else:
                            continue

                    except Exception as e:
                        log.info(e)
                        continue
            except:
                log.info(e)
                continue

    def monitor(self):
        while True:

            if '|' in self.task['PRODUCT']:
                self.kwUrl = "https://www.shopdisney.{}/search?srule=Newest&q={}".format(self.disneyRegion,"+".join(self.task["PRODUCT"].split('|')))
                self.prodUrl = self.findProduct()
            elif "shopdisney" in self.task["PRODUCT"]:
                self.prodUrl = self.task["PRODUCT"]
            else:
                self.prodUrl = "https://www.shopdisney.{}/{}.html".format(self.disneyRegion,self.task["PRODUCT"]) 

            self.prepare("Getting Product...")

            try:
                response = self.session.get(self.prodUrl)
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
                    regex = r"fe.data.urls.cartShow(.+);"
                    matches = re.search(regex, response.text, re.MULTILINE)
                    if matches:
                        self.bag = str(matches.group()).split('= "/')[1].split('"')[0]

                        soup = BeautifulSoup(response.text, "html.parser")

                        self.webhookData['product'] = str(soup.find("title").text.strip(" ").replace("\n","").split(' - ')[0])
                        self.webhookData['image'] = str(soup.find("meta", {"property": "og:image"})["content"])
                        self.webhookData['price'] = str(soup.find("meta", {"itemprop": "price"})["content"])

                        self.csrf = soup.find("input",{"name":"csrf_token"})["value"]
                        self.pid = soup.find("input",{"name":"pid"})["value"]
                        self.cartURL = soup.find("form",{"class":"js-pdp-form"})["action"]
                        self.siteBase = "https://www.shopdisney.{}".format(self.disneyRegion)
                        self.demandwareBase = self.cartURL.split('Cart-AddProduct')[0]
                        self.size = "One Size"
                        self.webhookData['size'] = self.size

                        self.warning(f"Found Size => {self.size}")
                        return

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
            
            payload = {
                'format': 'ajax',
                'Quantity': 1,
                'pid': self.pid,
                'csrf_token': self.csrf
            }   
            

            try:
                response = self.session.post(self.cartURL, data=payload, headers={
                    'accept': '*/*',
                    'referer': self.prodUrl,
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
                    soup = BeautifulSoup(response.text,"html.parser")
                    count = soup.find("span",{"class":"bag-count"}).text
                except Exception as e:
                    log.info(e)
                    self.error("Failed to cart [failed to parse response]. Retrying...")
                    time.sleep(int(self.task["DELAY"]))
                    continue
                
                if int(count) > 0:
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
    
    def secKey(self):
        while True:
            self.prepare("Getting secure key...")
            
            try:
                response = self.session.get(self.siteBase + '/' + self.bag, headers={
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'referer': self.prodUrl,
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
                    self.bagUrl = soup.find('form',{'name':'dwfrm_cart'})['action']
                    self.secureKey = self.bagUrl.split('?dwcont=')[1]
                    self.checkoutCart = soup.find('button',{'name':'dwfrm_cart_checkoutCart'})['value']
                except Exception as e:
                    log.info(e)
                    logger.error(SITE,self.taskID,'Failed to get secure key [failed to parse response]')
                    time.sleep(int(self.task["DELAY"]))
                    continue

                self.warning("Got secure key")
                return
            else:
                self.error(f"Failed to get secure key [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def shipKey(self):
        while True:
            self.prepare("Getting shipping key...")
            
            try:
                response = self.session.post(self.bagUrl,data={"dwfrm_cart_checkoutCart": self.checkoutCart} ,headers={
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'referer': self.siteBase + "/" + self.bag,
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
                    self.bagUrl = soup.find('form',{'id':'checkout-shipping-form'})['action']
                    self.shippingKey = soup.find('input',{'name':'dwfrm_singleshipping_securekey'})['value']
                except Exception as e:
                    log.info(e)
                    logger.error(SITE,self.taskID,'Failed to get shipping key [failed to parse response]')
                    time.sleep(int(self.task["DELAY"]))
                    continue

                self.warning("Got shipping key")
                return
            else:
                self.error(f"Failed to get shipping key [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def shipMethods(self):
        while True:
            self.prepare("Getting shipping method...")

            params = {
                'countryCode': self.profile["countryCode"],
                'postalCode': self.profile["zip"],
                'city': self.profile["city"],
                '_': int(time.time())
            }
            
            try:
                response = self.session.get(self.demandwareBase + "COShippingHook-UpdateShippingMethodList",params=params,headers={
                    'accept': '*/*',
                    'referer': self.bagUrl,
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
                    soup = BeautifulSoup(response.text,"html.parser")
                    methods = soup.find_all('input',{'name':'dwfrm_singleshipping_shippingAddress_shippingMethodList'})
                    self.method = methods[0]["value"]
                except Exception as e:
                    log.info(e)
                    logger.error(SITE,self.taskID,'Failed to get shipping method [failed to parse response]')
                    time.sleep(int(self.task["DELAY"]))
                    continue

                self.warning("Got shipping method")
                return
            else:
                self.error(f"Failed to get shipping method [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def shipping(self):
        while True:
            self.prepare("Submitting shipping...")
          
            try:
                payload = {
                    'dwfrm_singleshipping_securekey': self.shippingKey,
                    'dwfrm_singleshipping_shippingAddress_addressFields_addressid': None,
                    'dwfrm_singleshipping_shippingAddress_addressFields_firstName': self.profile["firstName"],
                    'dwfrm_singleshipping_shippingAddress_addressFields_lastName': self.profile["lastName"],
                    'dwfrm_singleshipping_shippingAddress_addressFields_phone': self.profile["phonePrefix"] + self.profile["phone"],
                    'dwfrm_singleshipping_shippingAddress_addressFields_email': self.profile["email"],
                    'dwfrm_singleshipping_shippingAddress_addressFields_country': self.profile["countryCode"],
                    'dwfrm_singleshipping_shippingAddress_addressFields_houseNumber': self.profile["house"],
                    'dwfrm_singleshipping_shippingAddress_addressFields_zip': self.profile["zip"],
                    'dwfrm_singleshipping_shippingAddress_addressFields_address1': self.profile["addressOne"],
                    'dwfrm_singleshipping_shippingAddress_addressFields_address2': self.profile["addressTwo"],
                    'dwfrm_singleshipping_shippingAddress_addressFields_city': self.profile["city"],
                    'accordionSectionCheckbox': 'on',
                    'dwfrm_singleshipping_shippingAddress_shippingMethodList': self.method,
                    'dwfrm_singleshipping_shippingAddress_addressFields_deliveryInstructions': '',
                    'dwfrm_singleshipping_shippingAddress_save': 1,
                }

            except Exception as e:
                self.error(f"Failed to construct shipping form ({e}). Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
                
            try:
                response = self.session.post(self.bagUrl,data=payload,headers={
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'referer': self.bagUrl,
                    'authority': f'www.shopdisney.{self.disneyRegion}',
                    'origin': f'https://www.shopdisney.{self.disneyRegion}',
                    'content-type': 'application/x-www-form-urlencoded',
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
                    self.billingSecureKey = soup.find('input',{'name':'dwfrm_billing_securekey'})['value']
                    self.bagUrl = soup.find('form',{'id':'js-checkout-billing-form'})['action']
                except Exception as e:
                    # print(response.text)
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

            try:
                payload = {
                    'dwfrm_billing_paymentMethods_selectedPaymentMethodID': 'WORLDPAY_PAYPAL',
                    'dwfrm_billing_paymentMethods_creditCard_type': '',
                    'dwfrm_billing_paymentMethods_creditCard_owner': '',
                    'dwfrm_billing_paymentMethods_creditCard_number': '',
                    'dwfrm_billing_paymentMethods_creditCard_month': '',
                    'dwfrm_billing_paymentMethods_creditCard_yearshort': '',
                    'dwfrm_billing_paymentMethods_creditCard_year': None,
                    'dwfrm_billing_paymentMethods_creditCard_cvn': '',
                    'dwfrm_billing_paymentMethods_creditCard_uuid': '',
                    'paymentmethods': 'WORLDPAY_PAYPAL',
                    'dwfrm_billing_threeDSReferenceId': '',
                    'dwfrm_billing_useShippingAddress': 0,
                    'dwfrm_billing_save': True,
                    'dwfrm_billing_billingAddress_addressFields_firstName': self.profile["firstName"],
                    'dwfrm_billing_billingAddress_addressFields_lastName': self.profile["lastName"],
                    'dwfrm_billing_billingAddress_addressFields_country': self.profile["countryCode"],
                    'dwfrm_billing_billingAddress_addressFields_houseNumber': self.profile["house"],
                    'dwfrm_billing_billingAddress_addressFields_zip': self.profile["zip"],
                    'dwfrm_billing_billingAddress_addressFields_address1': self.profile["addressOne"],
                    'dwfrm_billing_billingAddress_addressFields_address2': self.profile["addressTwo"],
                    'dwfrm_billing_billingAddress_addressFields_city': self.profile["city"],
                    'dwfrm_billing_securekey': self.billingSecureKey
                }
            except Exception as e:
                self.error(f"Failed to construct paypal form ({e}). Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

            try:
                response = self.session.post(self.bagUrl,data=payload,headers={
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'referer': self.demandwareBase + 'COShipping-Start/{}'.format(self.secureKey),
                    'authority': f'www.shopdisney.{self.disneyRegion}',
                    'origin': f'https://www.shopdisney.{self.disneyRegion}',
                    'content-type': 'application/x-www-form-urlencoded',
                })

            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if response.status_code in [200,302]:

                try:
                    soup = BeautifulSoup(response.text,"html.parser")
                    self.submitVal = soup.find('button',{'name':'submit-order'})['value']
                except:
                    self.error("Failed to get paypal checkout [failed to parse response]. Retrying...")
                    time.sleep(int(self.task["DELAY"]))
                    continue
                
                try:
                    response2 = self.session.post(self.demandwareBase + "COSummary-Submit",data={'submit-order': self.submitVal, 'csrf_token':self.csrf},headers={
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'referer': self.siteBase + '/{}?dwcont={}'.format(self.bag,self.secureKey),
                        'content-type': 'application/x-www-form-urlencoded',
                        'authority': f'www.shopdisney.{self.disneyRegion}',
                        'origin': f'https://www.shopdisney.{self.disneyRegion}',
                    })

                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    log.info(e)
                    self.error(f"error: {str(e)}")
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    continue

                if response2.status_code in [200,302] and "paypal" in response2.url:
                    self.end = time.time() - self.start
                    self.webhookData['speed'] = self.end

                    self.success("Got paypal checkout!")
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
                    self.error(f"Failed to get paypal checkout [{str(response.status_code)}]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue

                
            else:
                self.error(f"Failed to get paypal checkout [{str(response.status_code)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
  
    def card(self):
        while True:
            self.prepare("Completing card checkout...")
            number = self.profile["card"]["cardNumber"]
            if str(number[0]) == "3":
                cType = 'Amex'
            if str(number[0]) == "4":
                cType = 'Visa'
            if str(number[0]) == "5":
                cType = 'Master'
            if str(number[0]) == "6":
                cType = 'Master' 

            try:
                n = 4
                cardSplit = [number[i:i+n] for i in range(0, len(number), n)]
                cardNumbers = f'{cardSplit[0]} / {cardSplit[1]} / {cardSplit[2]} / {cardSplit[3]}'

                payload = {
                    'dwfrm_billing_paymentMethods_selectedPaymentMethodID': 'WORLDPAY_CREDIT_CARD',
                    'dwfrm_billing_paymentMethods_creditCard_type': cType,
                    'dwfrm_billing_paymentMethods_creditCard_owner': self.profile["firstName"] + " " + self.profile["lastName"],
                    'dwfrm_billing_paymentMethods_creditCard_number': cardNumbers,
                    'dwfrm_billing_paymentMethods_creditCard_month': self.profile["card"]["cardMonth"],
                    'dwfrm_billing_paymentMethods_creditCard_yearshort': self.profile["card"]["cardYear"][2:],
                    'dwfrm_billing_paymentMethods_creditCard_year': self.profile["card"]["cardYear"],
                    'dwfrm_billing_paymentMethods_creditCard_cvn': self.profile["card"]["cardCVV"],
                    'dwfrm_billing_paymentMethods_creditCard_uuid': '',
                    'paymentmethods': 'WORLDPAY_CREDIT_CARD',
                    'dwfrm_billing_threeDSReferenceId': '',
                    'dwfrm_billing_useShippingAddress': 0,
                    'dwfrm_billing_save': True,
                    'dwfrm_billing_billingAddress_addressFields_firstName': self.profile["firstName"],
                    'dwfrm_billing_billingAddress_addressFields_lastName': self.profile["lastName"],
                    'dwfrm_billing_billingAddress_addressFields_country': self.profile["countryCode"],
                    'dwfrm_billing_billingAddress_addressFields_houseNumber': self.profile["house"],
                    'dwfrm_billing_billingAddress_addressFields_zip': self.profile["zip"],
                    'dwfrm_billing_billingAddress_addressFields_address1': self.profile["addressOne"],
                    'dwfrm_billing_billingAddress_addressFields_address2': self.profile["addressTwo"],
                    'dwfrm_billing_billingAddress_addressFields_city': self.profile["city"],
                    'dwfrm_billing_securekey': self.billingSecureKey
                }
            except:
                self.error("Failed to construct checkout form. Retrying...")
                time.sleep(int(self.task["DELAY"]))
                continue

            try:
                response = self.session.post(self.bagUrl,data=payload,headers={
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'referer': self.demandwareBase + 'COShipping-Start/{}'.format(self.secureKey),
                    'authority': f'www.shopdisney.{self.disneyRegion}',
                    'origin': f'https://www.shopdisney.{self.disneyRegion}',
                    'content-type': 'application/x-www-form-urlencoded',
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue
 
            if response.status_code in [200,302]:

                try:
                    response2 = self.session.post(self.demandwareBase + "COSummary-Submit",data={'submit-order': 'Submit Order', 'csrf_token':self.csrf},headers={
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'referer': self.siteBase + '/{}?dwcont={}'.format(self.bag,self.secureKey),
                        'content-type': 'application/x-www-form-urlencoded',
                        'authority': f'www.shopdisney.{self.disneyRegion}',
                        'origin': f'https://www.shopdisney.{self.disneyRegion}',
                    })
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    log.info(e)
                    self.error(f"error: {str(e)}")
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    time.sleep(int(self.task["DELAY"]))
                    continue

                if response2.status_code in [200,302]:

                    try:
                        soup = BeautifulSoup(response2.text, "html.parser")
                        PaReq = soup.find('input',{'name':'PaReq'})['value']
                        termUrl = soup.find('input',{'name':'TermUrl'})['value']
                        MD = soup.find('input',{'name':'MD'})['value']
                    except Exception as e:
                        self.error(f"Failed to complete card checkout [{str(response.status_code)}]. Retrying...")
                        time.sleep(int(self.task['DELAY']))
                        continue

                    self.Dpayload = {
                        "TermUrl":termUrl,
                        "PaReq":PaReq,
                        "MD":MD 
                    }

                    three_d_data = threeDSecure.solve(
                        self.session,
                        self.profile,
                        self.Dpayload,
                        self.webhookData,
                        self.taskID,
                        f'https://www.shopdisney.{self.disneyRegion}'
                    )
                    if three_d_data == False:
                        self.error("Checkout Failed (3DS Declined or Failed). Retrying...")
                        time.sleep(int(self.task['DELAY']))
                        continue
                    

                    try:
                        response3 = self.session.post(termUrl,data=three_d_data,headers={
                            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                            'referer': self.siteBase + '/{}?dwcont={}'.format(self.bag,self.secureKey),
                            'content-type': 'application/x-www-form-urlencoded',
                            'authority': f'www.shopdisney.{self.disneyRegion}',
                            'origin': f'https://www.shopdisney.{self.disneyRegion}',
                        })
                    except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                        log.info(e)
                        self.error(f"error: {str(e)}")
                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                        time.sleep(int(self.task["DELAY"]))
                        continue

                    if response3.status_code in [200,302] and 'WorldPay' in response3.url:
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
                    self.error(f"Failed to complete card checkout [{str(response.status_code)}]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue

            else:
                self.error(f"Failed to complete card checkout [{str(response.status_code)}]. Retrying...")
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