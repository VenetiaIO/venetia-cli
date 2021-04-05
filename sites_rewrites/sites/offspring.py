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
import http.cookiejar


from utils.captcha import captcha
from utils.logger import logger
from utils.webhook import Webhook
from utils.log import log
from utils.adyen import ClientSideEncrypter
from utils.threeDS import threeDSecure

from utils.functions import (
    loadSettings,
    loadProfile,
    loadProxy2,
    createId,
    loadCookie,
    loadToken,
    sendNotification,
    injection,
    storeCookies,
    updateConsoleTitle,
    scraper,
    footlocker_snare,
    birthday
)
import utils.config as CONFIG

def getCookies(jar):
    cookieString = ""
    for c in jar:
        cookieString += '{}={};'.format(c.name,c.value)
    
    return cookieString

_SITE_ = 'OFFSPRING'
SITE = 'Offspring'
class OFFSPRING:
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

    def setCookies(self,response):
        for c in response.cookies:
            self.cookieJar.set_cookie(http.cookiejar.Cookie(
                version=0,
                name=c,
                value=response.cookies[c],
                port=None,
                port_specified=False,
                domain="www.offspring.co.uk",
                domain_specified=False,
                domain_initial_dot=False,
                path="/",
                path_specified=True,
                secure=False,
                expires=None,
                discard=True,
                comment=None,
                comment_url=None,
                rest={"HttpOnly": None},
                rfc2109=False,
            ))
    
    def rotateProxy(self):
        self.proxy = loadProxy2(self.task["PROXIES"],self.taskID,SITE)
        self.session = client.Session(
            browser=client.Fingerprint.CHROME_83,
            proxy=self.proxy
        )
        return

    def __init__(self, task, taskName, rowNumber):
        self.task = task
        self.taskID = taskName
        self.rowNumber = rowNumber

        if self.rowNumber != 'qt': 
            threading.Thread(target=self.task_checker,daemon=True).start()

        self.proxy = loadProxy2(self.task["PROXIES"],self.taskID,SITE)
        try:
            self.session = client.Session(
                browser=client.Fingerprint.CHROME_83,
                proxy=self.proxy
            )
            # self.session = scraper()
        except Exception as e:
            self.error(f'error => {e}')
            self.__init__(task,taskName,rowNumber)
        
        self.cookieJar = http.cookiejar.CookieJar()


        self.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'

        self.vp_offspring = None

        if 'https' not in self.task['PRODUCT']:
            self.prodUrl = 'https://www.offspring.co.uk/view/product/offspring_catalog/1,21/{}'.format(self.task['PRODUCT'])
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


        self.profile = loadProfile(self.task["PROFILE"])
        if self.profile == None:
            self.error("Profile Not found. Exiting...")
            time.sleep(10)
            sys.exit()



        self.capToken = None 
        self.tasks()
    
    def tasks(self):

        self.monitor()
        self.checkCaptcha()
        self.addToCart()
        self.shippingCountry()
        self.deliveryMode()
        self.shipping()

        if self.task['PAYMENT'].strip().lower() == "paypal":
            self.paypal()
        else:
            self.card()

        self.sendToDiscord()

    def monitor(self):
        self.q = False

        self.cookieJar.set_cookie(http.cookiejar.Cookie(
            version=0,
            name='_abck',
            value='A2BD19D77C92AD0722594334F4B52240~-1~YAAQhj9lXzN+1HJ4AQAAZvJzdQXbBfeAq9YZ1mJ+FKtVQwbzgQ5n1QwgrlQ8LEFNY5UFNSN0Y5ZzgPYWCXavLMblzlIcUF0iAvhlDIP5D5Vf/OSelMKz1vfFLwIs8SfDqRlKYkSCvOgylGdDDDJqfLEvSNDixmIMcb56tcNrlUYwSE1DcfvJtGx1lQ+411CBofmboFn51vlPq+h0yXH9n3FdWXJuoY39EfO0jzH2RDRv1OuhPorvG4fvzrIErEqHNTZelFvxRdmC/Wya9Rc8/ve0jpxe/towviCiXAwi1Kho7eJ12cZoWYud4dKPXEc88TKHfPyM/Y3lVOirz5uWFnRe0C1I1ZivKNOkjgl1gtklTiyRt/m/B08UCKqoE9YgBfzRE6RENKGdiC2ee3oY9GTMUUkhhJNjE8vOXKRzke83HTZTEXmDftIT51uG9pwDFVm9Foupq52pL4LpkyfejZPL~-1~-1~-1',
            port=None,
            port_specified=False,
            domain=".offspring.co.uk",
            domain_specified=False,
            domain_initial_dot=False,
            path="/",
            path_specified=True,
            secure=False,
            expires=None,
            discard=True,
            comment=None,
            comment_url=None,
            rest={"HttpOnly": None},
            rfc2109=False,
        ))
        while True:
            if self.q == False: self.prepare("Getting Product...")

            try:
                response = self.session.get(self.prodUrl,headers={
                    'user-agent':self.userAgent,
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'accept-language': 'en-US,en;q=0.9',
                    'cookie':getCookies(self.cookieJar),
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                self.rotateProxy()
                time.sleep(int(self.task["DELAY"]))
                continue


            try:
                akavpwr_VP_offspring_val = str(response.headers['set-cookie']).split('akavpwr_VP_offspring=')[1].split(';')[0]
                self.cookieJar.set_cookie(http.cookiejar.Cookie(
                    version=0,
                    name='akavpau_VP_offspring',
                    value=akavpwr_VP_offspring_val,
                    port=None,
                    port_specified=False,
                    domain="www.offspring.co.uk",
                    domain_specified=False,
                    domain_initial_dot=False,
                    path="/",
                    path_specified=True,
                    secure=False,
                    expires=None,
                    discard=True,
                    comment=None,
                    comment_url=None,
                    rest={"HttpOnly": None},
                    rfc2109=False,
                ))
            except Exception:
                pass

            for c in response.cookies:
                if c.lower() != 'akavpwr_VP_offspring':
                    self.cookieJar.set_cookie(http.cookiejar.Cookie(
                        version=0,
                        name=c,
                        value=response.cookies[c],
                        port=None,
                        port_specified=False,
                        domain="www.offspring.co.uk",
                        domain_specified=False,
                        domain_initial_dot=False,
                        path="/",
                        path_specified=True,
                        secure=False,
                        expires=None,
                        discard=True,
                        comment=None,
                        comment_url=None,
                        rest={"HttpOnly": None},
                        rfc2109=False,
                    ))

            try:
                currentVal = self.prodUrl.split('/offspring_catalog/')[1].split(',')[0]
                self.prodUrl = self.prodUrl.replace(currentVal + ',', str(random.randint(1,99)) + ',')
            except Exception:
                pass


            if response.status == 503:
                self.q = True
                logger.info(SITE,self.taskID,'Queue....')
                continue

            elif response.status == 200:
                self.q = False
                self.start = time.time()

                self.warning("Retrieved Product")

                try:
                    soup = BeautifulSoup(response.text, "html.parser")

                    self.pid = soup.find('input',{'name':'productCode'})['value']
                    self.csrf = soup.find('input',{'name':'CSRFToken'})['value']

                    self.cookieJar.set_cookie(http.cookiejar.Cookie(
                        version=0,
                        name='CSRFToken',
                        value=self.csrf,
                        port=None,
                        port_specified=False,
                        domain="www.offspring.co.uk",
                        domain_specified=False,
                        domain_initial_dot=False,
                        path="/",
                        path_specified=True,
                        secure=False,
                        expires=None,
                        discard=True,
                        comment=None,
                        comment_url=None,
                        rest={"HttpOnly": None},
                        rfc2109=False,
                    ))

                    foundSizes = soup.find('ul',{'data-locale':'UK'})

                    allSizes = []
                    sizes = []
                    for s in foundSizes:
                        try:
                            size = s['data-name']
                            sizes.append(size)
                            allSizes.append('{}:{}'.format(size, self.pid+s['data-value']))
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
                                    self.sizeId = size.split(":")[1]
                                    
                                    self.warning(f"Found Size => {self.size}")
        
                    else:
                        selected = random.choice(allSizes)
                        self.size = selected.split(":")[0]
                        self.sizeId = selected.split(":")[1]
                        
                        self.warning(f"Found Size => {self.size}")
  

                except Exception as e:
                    log.info(e)
                    self.error("Failed to parse product data (maybe OOS)")
                    time.sleep(int(self.task['DELAY']))
                    continue

                return
                    
            else:
                self.q = False
                self.error(f"Failed to get product [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def checkCaptcha(self):
        while True:
            self.prepare('Checking captcha...')

            try:
                response = self.session.post('https://www.offspring.co.uk/view/captcha/isCaptchaEnabledForProduct',
                data={"productCode":self.pid},headers={
                    'user-agent': self.userAgent,
                    'accept': '*/*',
                    'x-requested-with': 'XMLHttpRequest',
                    'referer':self.task['PRODUCT'],
                    'csrftoken':self.csrf,
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                    'cookie':getCookies(self.cookieJar)
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue
            
            self.setCookies(response)
            if 'false' in response.text:
                logger.warning(SITE,self.taskID,'No Captcha Required')
                self.capToken = None
            elif 'true' in response.text:
                logger.warning(SITE,self.taskID,'Captcha Required')
                captchaResponse = loadToken(SITE)

                if captchaResponse == "empty":

                    if CONFIG.captcha_configs[SITE]['type'].lower() == 'v3':
                        capToken = captcha.v3(CONFIG.captcha_configs[SITE]['siteKey'],CONFIG.captcha_configs[SITE]['url'],self.task['PROXIES'],SITE,self.taskID)
                    elif CONFIG.captcha_configs[SITE]['type'].lower() == 'v2':
                        capToken = captcha.v2(CONFIG.captcha_configs[SITE]['siteKey'],CONFIG.captcha_configs[SITE]['url'],self.task['PROXIES'],SITE,self.taskID)
                
                self.capToken = capToken
            
            return
    
    def addToCart(self):
        while True:
            self.prepare("Adding to cart...")
            
            payload = {
                "productCode":self.sizeId,
                "wishlist":False
            }
            if self.capToken != None: payload['grecaptcharesponse'] = self.capToken
            else: pass

            try:
                response = self.session.post('https://www.offspring.co.uk/view/basket/add',data=payload,headers={
                    'user-agent': self.userAgent,
                    'accept': '*/*',
                    'x-requested-with': 'XMLHttpRequest',
                    'referer':self.prodUrl,
                    'csrftoken':self.csrf,
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                    'cookie':getCookies(self.cookieJar),
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'origin': 'https://www.offspring.co.uk',
                    'authority': 'www.offspring.co.uk',
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue
            
            print(getCookies(self.cookieJar))
            self.setCookies(response)

            print(response.status)
            print(response.text)
            sys.exit()
            if response.status == 200:
                try:
                    data = response.json()
                    statusCode = data['statusCode']
                except:
                    self.error(f"Failed to cart [Failed to parse response]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue
                
                if statusCode == "success":
                    try:
                        self.webhookData['product'] = data['entry']['product']['name']
                        self.webhookData['price'] = data['entry']['totalPrice']['formattedValue']
                        self.webhookData['image'] = data['entry']['product']['images'][0]['url']
                        self.cartCode = data['cartCode']
                    except:
                        self.error(f"Failed to cart [failed to parse response]. Retrying...")
                        time.sleep(int(self.task['DELAY']))
                        continue

                    self.success("Added to cart!")
                    updateConsoleTitle(True,False,SITE)
                    return
                    
                else:
                    self.error(f"Failed to cart [{str(response.status)}]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue
            
            else:
                self.error(f"Failed to cart [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def shippingCountry(self):
        while True:
            self.prepare("Setting country...")
            
            payload = {
                "countryIsoCode": self.profile['countryCode'].upper(),
                "CSRFToken": self.csrf
            }


            try:
                response = self.session.post('https://www.offspring.co.uk/view/component/singlepagecheckout/setDeliveryCountry',
                data=payload,headers={
                    'user-agent': self.userAgent,
                    'accept': '*/*',
                    'x-requested-with': 'XMLHttpRequest',
                    'referer':'https://www.offspring.co.uk/checkout/singlePageCheckout',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                    'cookie':getCookies(self.cookieJar)
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue

            self.setCookies(response)
            if response.status == 200:
                try:
                    data = response.json()
                    statusCode = data['updateStatus']
                except:
                    self.error(f"Failed to set country [Failed to parse response]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue
                
                if statusCode == "SUCCESS":
                    try:
                        methods = data['orderSummary']['deliveryModes']
                        if len(methods) == 0:
                            raise Exception
                        elif len(methods) == 1:
                            self.deliveryOption = methods[0]["code"]
                        else:
                            for k in methods:
                                if 'standard' in k['name'].lower():
                                    self.deliveryOption = k['code']
                    except Exception:
                        self.error(f"Failed to set country  [failed to parse response]. Retrying...")
                        time.sleep(int(self.task['DELAY']))
                        continue

                    self.warning("Set country")
                    return
                    
                else:
                    self.error(f"Failed to set country  [{str(response.status)}]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue
            
            else:
                self.error(f"Failed to set country  [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def deliveryMode(self):
        while True:
            self.prepare("Setting delivery mode...")
            
            payload = {
                "deliveryModeCode": self.deliveryOption,
                "CSRFToken": self.csrf
            }


            try:
                response = self.session.post('https://www.offspring.co.uk/view/component/singlepagecheckout/setDeliveryMode',
                data=payload,headers={
                    'user-agent': self.userAgent,
                    'accept': '*/*',
                    'x-requested-with': 'XMLHttpRequest',
                    'referer':'https://www.offspring.co.uk/checkout/singlePageCheckout',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                    'cookie':getCookies(self.cookieJar)
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue

            self.setCookies(response)
            if response.status == 200:
                try:
                    data = response.json()
                    statusCode = data['updateStatus']
                except:
                    self.error(f"Failed to set delivery mode [Failed to parse response]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue
                
                if statusCode == "SUCCESS":
                    self.warning("Set delivery mode")
                    return
                    
                else:
                    self.error(f"Failed to set delivery mode [{str(response.status)}]. Retrying...")
                    time.sleep(int(self.task['DELAY']))
                    continue
            
            else:
                self.error(f"Failed to set delivery mode [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue

    def shipping(self):
        while True:
            self.prepare("Submitting shipping...")
            
            try:
                payload = {
                    "email": self.profile['email'],
                    "title": 'Mr',
                    "titleCode": 'mr',
                    "phone": self.profile['phone'],
                    "firstName": self.profile['firstName'],
                    "lastName": self.profile['lastName'],
                    "companyName": '',
                    "line1": self.profile['house'] + ' ' + self.profile['addressOne'],
                    "line2": self.profile['addressTwo'],
                    "town": self.profile['city'],
                    "postalCode": self.profile['zip'],
                    "country": self.profile['countryCode'],
                    "defaultAddress": True,
                    "CSRFToken": self.csrf
                }
            except Exception:
                self.error('Failed to submit shipping [failed to construct payload]. Retrying...')
                time.sleep(int(self.task['DELAY']))
                continue


            try:
                response = self.session.post('https://www.offspring.co.uk/view/component/singlepagecheckout/addEditDeliveryAddress',
                data=payload,headers={
                    'user-agent': self.userAgent,
                    'accept': '*/*',
                    'x-requested-with': 'XMLHttpRequest',
                    'referer':'https://www.offspring.co.uk/checkout/singlePageCheckout',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                    'cookie':getCookies(self.cookieJar)
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue

            self.setCookies(response)
            if response.status == 200:
                self.warning("Submitted shipping")
                return
            
            else:
                self.error(f"Failed to submit shipping [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    
    def paypal(self):
        while True:
            self.prepare("Getting paypal checkout...")
            
            payload = {
                'paymentMode': 'worldpay_paypal',
                'emailOptIn': 'true',
                'newsAlerts': 'true',
                'CSRFToken': self.csrf
            }


            try:
                response = self.session.post('https://www.offspring.co.uk/view/component/singlepagecheckout/continueToPaymentDetails',
                data=payload,headers={
                    'user-agent': self.userAgent,
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'x-requested-with': 'XMLHttpRequest',
                    'referer':'https://www.offspring.co.uk/checkout/singlePageCheckout',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                    'cookie':getCookies(self.cookieJar)
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                self.error(f"error: {str(e)}")
                time.sleep(int(self.task["DELAY"]))
                self.rotateProxy()
                continue

            self.setCookies(response)
            if response.status == 200 and 'paypal' in str(response.url):
                self.end = time.time() - self.start
                self.webhookData['speed'] = self.end

                self.success("Got paypal checkout!")
                updateConsoleTitle(False,True,SITE)

                self.webhookData['url'] = storeCookies(
                    response.url,self.cookieJar,
                    self.webhookData['product'],
                    self.webhookData['image'],
                    self.webhookData['price'],
                    True
                )
                return
            
            else:
                self.error(f"Failed to get paypal checkout [{str(response.status)}]. Retrying...")
                time.sleep(int(self.task['DELAY']))
                continue
    

    def sendToDiscord(self):
        while True:
            
            self.webhookData['proxy'] = self.proxy

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
                while True:
                    pass




# OFFSPRING({'PRODUCT': '2704696559', 'SIZE': 'random', 'DELAY': '1', 'PROFILE': 'hsbc', 'PAYMENT': 'paypal', 'PROXIES': 'resigame', 'ACCOUNT EMAIL': '', 'ACCOUNT PASSWORD': '', 'SITE': 'OFFSPRING', 'TASK_NAME': 'Task 0001', 'ROW_NUMBER': 0},'Task 0001','qt')