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

from utils.captcha import captcha
from utils.logger import logger
from utils.webhook import Webhook
from utils.log import log
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies, updateConsoleTitle, scraper)
from utils.config import *

SITE = 'ALLIKE'
class ALLIKE:
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
        self.shipping()
        self.shippingMethod()

        if self.task['PAYMENT'].strip().lower() == "paypal":
            self.paypal()
        else:
            self.card()

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

            if response.status == 200:
                self.start = time.time()

                self.warning("Retrieved Product")

                try:
                    soup = BeautifulSoup(response.text, "html.parser")

                    self.webhookData['product'] = str(soup.find("title").text)
                    self.webhookData['image'] = str(soup.find("img", {"id": "image-0"})["src"])
                    self.webhookData['price'] = str(soup.find("span",{"class":"price"}).text)

                    self.atcUrl = soup.find("form", {"id": "product_addtocart_form"})["action"].replace("checkout/cart", "oxajax/cart")
                    self.formKey = soup.find("input", {"name": "form_key"})["value"]
                    self.productId = soup.find("input", {"name": "product"})["value"]
                    self.attributeId = soup.find("select", {"class": "required-entry super-attribute-select no-display swatch-select"})["id"].split("attribute")[1]

                    regex = r"{\"attributes\":(.*?)}}\)"
                    matches = re.search(regex, response.text, re.MULTILINE)
                    if matches:
                        productData = json.loads(matches.group()[:-1])["attributes"][self.attributeId]

                        allSizes = []
                        sizes = []
                        for s in productData["options"]:
                            try:
                                allSizes.append('{}:{}:{}'.format(s["label"],s["products"][0],s["id"]))
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
                                        return
            
                        else:
                            selected = random.choice(allSizes)
                            self.size = selected.split(":")[0]
                            self.option = selected.split(":")[1]
                            self.sizeID = selected.split(":")[2]
                            
                            self.warning(f"Found Size => {self.size}")
                            return

                        

                    else:
                        raise Exception
                except Exception as e:
                    log.info(e)
                    self.error("Failed to parse product data (maybe OOS)")
                    time.sleep(int(self.task['DELAY']))
                    continue
                    
            else:
                self.error(f"Failed to get product [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def addToCart(self):
        while True:
            self.prepare("Adding to cart...")
            
            payload = {
                'isAjax': 1,
                'form_key': self.formKey,
                'product': self.productId,
                'related_product': '',
                f'super_attribute[{self.attributeId}]': self.sizeID,
                'return_url': ''
            }

            try:
                response = self.session.post(self.atcUrl, data=payload, headers={
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
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            try:
                splitText = response.text.split('({')[1].split('})')[0]
                data = json.loads('{' + splitText + '}')
                status = data["status"]
            except Exception as e:
                log.info(e)
                self.error("Failed to cart. Retrying...")
                time.sleep(int(self.task["DELAY"]))
                continue

            if response.status == 200 and status == "SUCCESS":
                self.success("Added to cart!")
                updateConsoleTitle(True,False,SITE)
                return
            
            else:
                self.error(f"Failed to cart [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def method(self):
        while True:
            self.prepare("Setting checkout method...")
            
            try:
                response = self.session.post('https://www.allikestore.com/default/checkout/onepage/saveMethod/', data={"method": "guest"}, headers={
                    'authority': 'www.allikestore.com',
                    'referer': 'https://www.allikestore.com/default/checkout/onepage/',
                    'x-requested-with': 'XMLHttpRequest',
                    'accept':'text/javascript, text/html, application/xml, text/xml, */*'
                })

            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if response.status == 200:
                self.warning("Set checkout method")
                return
            else:
                self.error(f"Failed to set checkout method [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def shipping(self):
        while True:
            self.prepare("Submitting shipping...")

            if captcha_configs[SITE]['siteKey'].lower() == 'v3':
                capToken = captcha.v3(captcha_configs[SITE]['siteKey'],captcha_configs[SITE]['url'],self.session.proxies,SITE,self.taskID)
            elif captcha_configs[SITE]['siteKey'].lower() == 'v2':
                capToken = captcha.v2(captcha_configs[SITE]['siteKey'],captcha_configs[SITE]['url'],self.session.proxies,SITE,self.taskID)

            try:
                day = random.randint(1,29)
                month = random.randint(1,12)
                year = random.randint(1970,2000)
                payload = {
                    'billing[address_id]': '',
                    'billing[firstname]': self.profile["firstName"],
                    'billing[lastname]': self.profile["lastName"],
                    'billing[company]': '',
                    'billing[email]': self.profile["email"],
                    'billing[street][]': self.profile["house"] + " " + self.profile["addressOne"],
                    'billing[city]': self.profile["city"],
                    'billing[region_id]': '',
                    'billing[region]': self.profile["region"],
                    'billing[postcode]': self.profile["zip"],
                    'billing[country_id]': self.profile["countryCode"],
                    'billing[telephone]': self.profile["phone"],
                    'billing[fax]': '',
                    'billing[month]': month,
                    'billing[day]': day,
                    'billing[year]': year,
                    'billing[dob]': '{}/{}/{}'.format(month,day,year),
                    'billing[customer_password]': '',
                    'billing[confirm_password]': '',
                    'billing[save_in_address_book]': '1',
                    'billing[use_for_shipping]': '1',
                    'form_key': self.formKey,
                    'g-recaptcha-response':capToken
                }
            except:
                self.error("Failed to construct shipping form. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
                
            try:
                response = self.session.post('https://www.allikestore.com/default/checkout/onepage/saveBilling/', data=payload, headers={
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
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if response.status == 200:
                try:
                    shippingOptions = json.loads(response.text)
                    shippingHtml = shippingOptions["update_section"]["html"]
                    soup = BeautifulSoup(shippingHtml,"html.parser")
                    self.shippingMethods = soup.find_all('input',{'name':'shipping_method'})

                    self.warning("Successfully set shipping")
                    return
                except Exception:
                    self.error(f"Failed to set shipping. Retrying...")
                    time.sleep(int(self.task["DELAY"]))
                    continue
            else:
                self.error(f"Failed to set shipping [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def shippingMethod(self):
        while True:
            self.prepare("Setting shipping method...")
            
            try:
                response = self.session.post('https://www.allikestore.com/default/checkout/onepage/saveShippingMethod/', data={
                    "shipping_method": self.shippingMethods[0]["value"], "form_key": self.formKey
                }, headers={
                    'authority': 'www.allikestore.com',
                    'accept-language': 'en-US,en;q=0.9',
                    'origin': 'https://www.allikestore.com',
                    'referer': 'https://www.allikestore.com/default/checkout/onepage/',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'x-requested-with': 'XMLHttpRequest',
                    'accept':'text/javascript, text/html, application/xml, text/xml, */*'
                })

            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if response.status == 200:
                self.warning("Set shipping method")


                if self.task["PAYMENT"].strip().lower() == "card":
                    try:
                        soup = BeautifulSoup(json.loads(response.text)["update_section"]["html"],"html.parser")
                        paymentConfig = json.loads(soup.find("input",{"id":"payone_creditcard_config"})["value"])
                        self.hash = paymentConfig["gateway"]["4"]["hash"]
                        self.mid = paymentConfig["gateway"]["4"]["mid"]
                        self.aid = paymentConfig["gateway"]["4"]["aid"]
                        self.portalid = paymentConfig["gateway"]["4"]["portalid"]
                    except Exception:
                        self.error("Failed to parse response")
                        time.sleep(int(self.task['DELAY']))
                        continue
    
                return
            else:
                self.error(f"Failed to set shipping method [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def paypal(self):
        while True:
            self.prepare("Getting paypal checkout...")
            
            try:
                response = self.session.post('https://www.allikestore.com/default/checkout/onepage/verifyPayment/', data={
                    "payment[method]": "paypal_express", "form_key": self.formKey
                }, headers={
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
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue

            if response.status == 200:
                
                try:
                    response2 = self.session.get('https://www.allikestore.com/default/paypal/express/start/', headers={
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
                    self.error(f"error: {str(e)}")
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    continue

                if response2.status in [200,302] and "paypal" in response2.url:
                    self.end = time.time() - self.start
                    self.webhookData['speed'] = self.end

                    self.success("Got paypal checkout!")
                    updateConsoleTitle(False,True,SITE)

                    self.webhookData['url'] = storeCookies(
                        response2.url,self.session,
                        self.webhookData['product'],
                        self.webhookData['image'],
                        self.webhookData['price']
                    )
                    return
                
                else:
                    self.error(f"Failed to get paypal checkout [{str(response.status)}]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue

                
            else:
                self.error(f"Failed to get paypal checkout [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    
    def card(self):
        while True:
            self.prepare("Completing card checkout...")
            number = self.profile["card"]["cardNumber"]
            if str(number[0]) == "3":
                cType = 'A'
            if str(number[0]) == "4":
                cType = 'V'
            if str(number[0]) == "5":
                cType = 'M'
            if str(number[0]) == "6":
                cType = 'M' 

            cardplan  = self.profile["card"]["cardNumber"]
            cardmonth = self.profile["card"]["cardMonth"]
            cardyear  = self.profile["card"]["cardYear"]
            cvv       = self.profile["card"]["cardCVV"]
            url = (
                f'https://secure.pay1.de/client-api/?aid={self.aid}'
                f'&encoding=UTF-8&errorurl=&hash={self.hash}&integrator_name=&integrator_version=&key=&language=&mid={self.mid}'
                f'&mode=live&portalid={self.portalid}&request=creditcardcheck&responsetype=JSON&solution_name=&solution_version=&storecarddata=yes'
                f'&successurl=&cardpan={cardplan}&cardexpiremonth={cardmonth}&cardexpireyear={cardyear}&cardtype={cType}&channelDetail=payoneHosted'
                f'&cardcvc2={cvv}&callback_method=PayoneGlobals.callback'
            )

            try:
                response = self.session.get(url,headers={
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
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                continue
            
            if response.status == 200:
                try:
                    split = response.text.split('PayoneGlobals.callback(')[1]
                    secure = json.loads(split.split(');')[0])

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

                except:
                    self.error("Failed to complete card checkout. Retrying...")
                    time.sleep(int(self.task["DELAY"]))
                    continue

                try:
                    response2 = self.session.get('https://www.allikestore.com/default/payone_core/checkout_onepage/verifyPayment/',data=verifyPayload,headers={
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
                    self.error(f"error: {str(e)}")
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    continue

                if response2.status == 200:
                    try:
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
                    except:
                        self.error("Failed to complete card checkout. Retrying...")
                        time.sleep(int(self.task["DELAY"]))
                        continue

                    try:
                        response3 = self.session.post('https://www.allikestore.com/default/checkout/onepage/saveOrder/',data=savePayload,headers={
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
                        self.error(f"error: {str(e)}")
                        time.sleep(int(self.task["DELAY"]))
                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                        continue
                    
                    if response3.status == 200:
                        try:
                            response3_data = json.loads(response3.text)
                            status = response3_data["success"]
                            redirect = response["redirect"]
                        except:
                            self.error("Failed to complete card checkout. Retrying...")
                            time.sleep(int(self.task["DELAY"]))
                            continue

                        if status == True:
                            self.end = time.time() - self.start
                            self.webhookData['speed'] = self.end

                            self.success("Got card checkout!")
                            updateConsoleTitle(False,True,SITE)

                            self.webhookData['url'] = storeCookies(
                                redirect,self.session,
                                self.webhookData['product'],
                                self.webhookData['image'],
                                self.webhookData['price']
                            )
                            return

                    else:
                        self.error("Failed to complete card checkout. Retrying...")
                        time.sleep(int(self.task["DELAY"]))
                        continue

                else:
                    self.error("Failed to complete card checkout. Retrying...")
                    time.sleep(int(self.task["DELAY"]))
                    continue
            
            else:
                self.error("Failed to complete card checkout. Retrying...")
                time.sleep(int(self.task["DELAY"]))
                continue
    
    def sendToDiscord(self):
        while True:
            
            self.webhookData['proxy'] = self.session.proxies
            sendNotification(SITE,self.productTitle)
            try:
                Webhook.success(
                    webhook=loadSettings()["webhook"],
                    site=SITE,
                    url=self.webhookData['url'],
                    image=self.webhookData['image'],
                    title=self.webhookData['product'],
                    size=self.size,
                    price=self.productPrice,
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
