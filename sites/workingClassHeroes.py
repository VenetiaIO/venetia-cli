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

from utils.logger import logger
from utils.webhook import discord
from utils.log import log
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies)
SITE = 'WorkingClassHeroes'



class WCH:
    def __init__(self, task,taskName):
        self.task = task
        self.session = requests.session()
        self.taskID = taskName

        twoCap = loadSettings()["2Captcha"]
        # self.session = cloudscraper.create_scraper(
            # requestPostHook=injection,
            # sess=self.sess,
            # interpreter='nodejs',
            # browser={
                # 'browser': 'chrome',
                # 'mobile': False,
                # 'platform': 'windows'
            #    'platform': 'darwin'
            # },
            # captcha={
                # 'provider': '2captcha',
                # 'api_key': twoCap
            # }
        # )
        
        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)

        self.collect()

    def collect(self):
        try:
            retrieve = self.session.get(self.task["PRODUCT"], headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'

            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.collect()

        if retrieve.status_code == 200:
            self.start = time.time()
            logger.success(SITE,self.taskID,'Got product page')
            try:
                soup = BeautifulSoup(retrieve.text, "html.parser")
                self.pid = soup.find('input',{'id':'currentProduct'})["value"]          
            except Exception as e:
               log.info(e)
               logger.error(SITE,self.taskID,'Failed to scrape page (Most likely out of stock). Retrying...')
               time.sleep(int(self.task["DELAY"]))
               self.collect()

            try:
                attrbs = self.session.post('https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/GetAttributes', headers={
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    
                },json={"controlLocation":"/modules/controls/clAttributeControl.ascx", "ProductID":self.pid, "DetailPage":True, "dollar":0, "percentage":0})
                logger.success(SITE,self.taskID,'Solved Cloudflare')
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                self.collect()
            
            try:
                data = attrbs.json()
            except Exception as e:
                log.info(e)

            if data:
                logger.info(SITE,self.taskID,'Successfully Scraped data')

                soup = BeautifulSoup(data["d"]["HTML"],"html.parser")
                foundSizes = soup.find_all('div',{'class':'attRow'})

                allSizes = []
                sizes = []
                for s in foundSizes:
                    try:
                        iAttributeDetailID = s.find('div',{'class':['hideme','Attattributeid']}).text
                        iAttributeID = s.find('input',{'class':'hiddenFieldAttID'})["value"]
                        fullSize = s.find('div',{'class':'name'}).text
                        splitSize = fullSize.split('UK ')[1]
                        sizes.append(splitSize)
                        allSizes.append('{}:{}:{}:{}'.format(splitSize,fullSize,iAttributeDetailID,iAttributeID))
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
                                self.size = size.split(':')[1]
                                self.iAttributeDetailID = size.split(':')[2]
                                self.iAttributeID = size.split(":")[3]
                                logger.success(SITE,self.taskID,f'Found Size => {self.size}')
    
                
                elif self.task["SIZE"].lower() == "random":
                    selected = random.choice(allSizes)
                    self.size = selected.split(':')[1]
                    self.iAttributeDetailID = selected.split(':')[2]
                    self.iAttributeID = selected.split(":")[3]
                    logger.success(SITE,self.taskID,f'Found Size => {self.size}')

                self.addToCart()
                    
            else:
                logger.error(SITE,self.taskID,'Failed to scrape data. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.collect()

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
            "iProductID":self.pid,
            "iQuantity":1,
            "iAttributeID":self.iAttributeID,
            "iAttributeDetailID":self.iAttributeDetailID
        }

        try:
            postCart = self.session.post('https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/AddToBasketJSNew', json=payload, headers={
                'authority': 'www.workingclassheroes.co.uk',
                'accept-language': 'en-US,en;q=0.9',
                'referer': self.task["PRODUCT"],
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()
        
        try:
            data = postCart.json()
        except:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

        if postCart.status_code == 200 and data:
            logger.success(SITE,self.taskID,'Successfully carted')
            if self.task["PAYMENT"].lower() == "paypal":
                self.paypal()
            elif self.task["PAYMENT"].lower() == "card":
                self.login()
        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()

    def paypal(self):
        try:
            cart = self.session.post('https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/WightPaypalBtnCallback', headers={
                'authority': 'www.workingclassheroes.co.uk',
                'accept-language': 'en-US,en;q=0.9',
                'accept':'application/json, text/javascript, */*; q=0.01',
                'referer': 'https://www.workingclassheroes.co.uk/shoppingcart.aspx',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
            },json={})
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.login()

        try:
            data = cart.json()
        except Exception as e:
            logger.error(SITE,self.taskID,'Failed to get paypal token.Retrying...')
            log.info(e)
            time.sleep(int(self.task["DELAY"]))
            self.paypal()


        if cart.status_code == 200 and data["d"]["status"] == True:
            self.end = time.time() - self.start

            try:
                GetProductLW = self.session.post('https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/GetProductLW', headers={
                    'authority': 'www.workingclassheroes.co.uk',
                    'accept-language': 'en-US,en;q=0.9',
                    'accept':'application/json, text/javascript, */*; q=0.01',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                },json={"productid":self.pid})
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.login()


            try:
                productData = GetProductLW.json()["d"]
            except Exception as e:
                logger.error(SITE,self.taskID,'Failed to get paypal token.Retrying...')
                log.info(e)
                time.sleep(int(self.task["DELAY"]))
                self.paypal()

            logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')
            url = storeCookies(data["d"]["errorMsg"],self.session)               
            sendNotification(SITE,productData["Name"])


            discord.success(
                webhook=loadSettings()["webhook"],
                site=SITE,
                url=url,
                image='https://www.workingclassheroes.co.uk/{}'.format(productData["ImageLargePath"]),
                title=productData["Name"],
                size=self.size,
                price=productData["Price"],
                paymentMethod='PayPal',
                profile=self.task["PROFILE"],
                product=self.task["PRODUCT"],
                proxy=self.session.proxies,
                speed=self.end
            )
            while True:
                pass



    
    def login(self):
        payload = {"emailAddress":self.task["ACCOUNT EMAIL"] , "password":self.task["ACCOUNT PASSWORD"]}
        try:
            login = self.session.post('https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/WightValidateCustomerLogin', json=payload, headers={
                'authority': 'www.workingclassheroes.co.uk',
                'accept-language': 'en-US,en;q=0.9',
                'referer': 'https://www.workingclassheroes.co.uk/ssl/secure/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.login()

        try:
            response = login.json()
            responeData = json.loads(response["d"])
            status = responeData["status"]
        except Exception as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Failed to login. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.login()

        if login.status_code == 200 and status == True:
            logger.success(SITE,self.taskID,'Successfully logged in')
            self.delivery()
        else:
            logger.error(SITE,self.taskID,'Failed to login. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.login()
    
    def delivery(self):
        profile = loadProfile(self.task["PROFILE"])
        payload = {
            "firstName":profile["firstName"],
            "lastName":profile["lastName"],
            "company":"",
            "address1":profile["house"] + " " + profile["addressOne"],
            "address2":profile["addressTwo"],
            "city":profile["city"],
            "postcode":profile["zip"],
            "country":profile["countryCode"]
        }
        try:
            options = self.session.post('https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/WightLoadShippingOptions', json=payload, headers={
                'authority': 'www.workingclassheroes.co.uk',
                'accept-language': 'en-US,en;q=0.9',
                'referer': 'https://www.workingclassheroes.co.uk/ssl/secure/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.delivery()

        try:
            response = options.json()
        except Exception as e:
            logger.error(SITE,self.taskID,'Failed to retrieve shipping methods.Retrying...')
            log.info(e)
            time.sleep(int(self.task["DELAY"]))
            self.login()

        if options.status_code == 200 and response:
            try:
                soup = BeautifulSoup(response["d"], "html.parser")
                self.shipMethod = json.loads(soup.find('input',{'id':'metapackJSONValues'})["value"])[0]
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to retrieve shipping methods.Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.delivery()

            payload = {
                "firstName":profile["firstName"],
                "lastName":profile["lastName"],
                "company":"",
                "address1":profile["house"] + " " + profile["addressOne"],
                "address2":profile["addressTwo"],
                "city":profile["city"],
                "phone":profile["phone"],
                "postcode":profile["zip"],
                "country":profile["countryCode"],
                "selectedShipping":self.shipMethod,
                "nickname":""
            }
            try:
                shipDetails = self.session.post('https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/WightPostShippingDetails', json=payload, headers={
                    'authority': 'www.workingclassheroes.co.uk',
                    'accept-language': 'en-US,en;q=0.9',
                    'referer': 'https://www.workingclassheroes.co.uk/ssl/secure/',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                    'accept':'application/json, text/javascript, */*; q=0.01',
                    'x-requested-with': 'XMLHttpRequest'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.delivery()

            try:
                response = shipDetails.json()
                responeData = json.loads(response["d"])
                status = responeData["status"]
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to post shipping details.Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.delivery()

            if shipDetails.status_code == 200 and status == True:
                logger.success(SITE,self.taskID,'Successfully posted shipping details')
                self.card()
                
            else:
                logger.error(SITE,self.taskID,'Failed to post shipping details. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.delivery()

            
        else:
            logger.error(SITE,self.taskID,'Failed to retrieve shipping methods.Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.delivery()


    def card(self):
        logger.info(SITE,self.taskID,'Starting [CREDIT CARD] checkout...')
        profile = loadProfile(self.task["PROFILE"])
        if len(profile["card"]["cardMonth"]) != 2:
            cardMonth = '0{}'.format(profile["card"]["cardMonth"])
        else:
            cardMonth = profile["card"]["cardMonth"]

        
        number = profile["card"]["cardNumber"]
        if str(number[0]) == "4":
            cType = 'Visa'
            cTypeUid = 8
        if str(number[0]) == "5":
            cType = 'MasterCard'
            cTypeUid = 9
        if str(number[0]) == "6":
            cType = 'Maestro' 
            cTypeUid = None


        payload = {
            "MethodType": "Standard",
            "SpecialInstructions": "",
            "PaymentMethod": "credit card",
            "cardTypeUid": cTypeUid,
            "cardType": cType,
            "cardNumber": profile["card"]["cardNumber"],
            "secureCode": profile["card"]["cardCVV"],
            "expMonth": cardMonth,
            "expYear": profile["card"]["cardYear"],
            "token": "",
            "selectedShipping": self.shipMethod,
            "paypalToken": "",
            "payPalPayerID": ""
        }

        try:
            paymentDetails = self.session.post('https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/WightHandlePaymentSelector', json=payload, headers={
                'authority': 'www.workingclassheroes.co.uk',
                'accept-language': 'en-US,en;q=0.9',
                'referer': 'https://www.workingclassheroes.co.uk/ssl/secure/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                'accept':'application/json, text/javascript, */*; q=0.01',
                'x-requested-with': 'XMLHttpRequest'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.delivery()

        if paymentDetails.status_code == 200:
            logger.success(SITE,self.taskID,'Successfully submitted card details.')
            try:
                threeDvalidation = self.session.get('https://www.workingclassheroes.co.uk/ssl/controls/3DAuthentication/3DRedirect.aspx')
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.card()
            if threeDvalidation.status_code == 200:
                soup = BeautifulSoup(threeDvalidation.text, "html.parser")
                PaReq = soup.find('input',{'name':'PaReq'})['value']
                termUrl = soup.find('input',{'name':'TermUrl'})['value']
                MD = soup.find('input',{'name':'MD'})['value']

                try:
                    payload = {"PaReq":PaReq, "TermUrl":termUrl,  "MD":MD}
                    payAuth = self.session.post('https://verifiedbyvisa.acs.touchtechpayments.com/v1/payerAuthentication', data=payload, headers={
                        'authority': 'verifiedbyvisa.acs.touchtechpayments.com',
                        'accept-language': 'en-US,en;q=0.9',
                        'referer': 'https://www.workingclassheroes.co.uk/ssl/controls/3DAuthentication/3DRedirect.aspx',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    })
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                    log.info(e)
                    logger.error(SITE,self.taskID,'Error: {}'.format(e))
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    self.card()
            
                if payAuth.status_code == 200:
                    soup = BeautifulSoup(payAuth.text, "html.parser")
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
                    except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                        log.info(e)
                        logger.error(SITE,self.taskID,'Error: {}'.format(e))
                        time.sleep(int(self.task["DELAY"]))
                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                        self.card()

                    if poll.json()["status"] == "blocked":
                        logger.error(SITE,self.taskID,'Card Blocked. Retrying...')
                        time.sleep(int(self.task["DELAY"]))
                        self.card()
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
                        self.card()

                    if poll.json()["status"] == "success":
                        authToken = poll.json()['authToken']
                    else:
                        logger.error(SITE,self.taskID,'Failed to retrieve auth token for 3DS. Retrying...')
                        time.sleep(int(self.task["DELAY"]))
                        self.card()

                    authToken = poll.json()['authToken']
                    logger.alert(SITE,self.taskID,'3DS Authorised')
            
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
                    except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                        log.info(e)
                        logger.error(SITE,self.taskID,'Error: {}'.format(e))
                        time.sleep(int(self.task["DELAY"]))
                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                        self.card()

                    pares = r.json()['Response']

                    data = {"MD":MD, "PaRes":pares}
                    try:
                        r = self.session.post(termUrl,headers={
                            'authority': 'www.workingclassheroes.co.uk',
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                            'content-type': 'application/x-www-form-urlencoded',
                            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                            'origin': 'https://verifiedbyvisa.acs.touchtechpayments.com',
                            'referer':'https://verifiedbyvisa.acs.touchtechpayments.com/v1/payerAuthentication',
                        }, data=data)
                    except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                        log.info(e)
                        logger.error(SITE,self.taskID,'Error: {}'.format(e))
                        time.sleep(int(self.task["DELAY"]))
                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                        self.card()

                    if r.status_code == 200:
                        print(r)
                        print(r.url)
                        try:
                            r = self.session.post('https://www.workingclassheroes.co.uk/ssl/secure/default.aspx?3DPostBack=true',headers={
                                'authority': 'www.workingclassheroes.co.uk',
                                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                                'content-type': 'application/x-www-form-urlencoded',
                                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                                'origin': 'https://verifiedbyvisa.acs.touchtechpayments.com',
                                'referer':termUrl,
                            })
                        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                            log.info(e)
                            logger.error(SITE,self.taskID,'Error: {}'.format(e))
                            time.sleep(int(self.task["DELAY"]))
                            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                            self.card()
                        
                        if r.status_code in [200,201,302] and 'confirm' in r.url.lower():
                            self.end = time.time() - self.start
                            logger.alert(SITE,self.taskID,'Sending Card checkout to Discord!')

                            try:
                                GetProductLW = self.session.post('https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/GetProductLW', headers={
                                    'authority': 'www.workingclassheroes.co.uk',
                                    'accept-language': 'en-US,en;q=0.9',
                                    'accept':'application/json, text/javascript, */*; q=0.01',
                                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                                },json={"productid":self.pid})
                            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                                log.info(e)
                                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                                time.sleep(int(self.task["DELAY"]))
                                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                                self.login()
                
                
                            try:
                                productData = GetProductLW.json()["d"]
                            except Exception as e:
                                logger.error(SITE,self.taskID,'Failed to get paypal token.Retrying...')
                                log.info(e)
                                time.sleep(int(self.task["DELAY"]))
                                self.paypal()
                            
        
                            discord.success(
                                webhook=loadSettings()["webhook"],
                                site=SITE,
                                image='https://www.workingclassheroes.co.uk/{}'.format(productData["ImageLargePath"]),
                                title=productData["Name"],
                                size=self.size,
                                price=productData["Price"],
                                paymentMethod='Card',
                                profile=self.task["PROFILE"],
                                product=self.task["PRODUCT"],
                                proxy=self.session.proxies,
                                speed=self.end
                            )
                            sendNotification(SITE,productData["Name"])
                            while True:
                                pass
                        
                        else:
                            log.info('{} [{}]'.format(r.status_code, r.url))
                            logger.error(SITE,self.taskID,'Checkout Failed []. Retrying...'.format(r.status_code))
                            time.sleep(int(self.task["DELAY"]))
                            self.card()
                    
                    else:
                        logger.error(SITE,self.taskID,'Checkout Failed []. Retrying...'.format(r.status_code))
                        time.sleep(int(self.task["DELAY"]))
                        self.card()
                    
                else:
                    logger.error(SITE,self.taskID,'Failed to auth card. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.card()

            else:
                logger.error(SITE,self.taskID,'Failed to get 3DS. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.card()
        else:
            logger.error(SITE,self.taskID,'Failed to submit details. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.card()


                    





        

