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
from urllib3.exceptions import HTTPError

SITE = 'AIRNESS'

from utils.logger import logger
from utils.webhook import discord
from utils.log import log
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification,storeCookies, updateConsoleTitle)

class AIRNESS:
    def __init__(self,task,taskName):
        self.task = task
        self.session = requests.session()
        self.taskID = taskName

        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)


        self.collect()

    def collect(self):
        logger.prepare(SITE,self.taskID,'Getting product page...')
        try:
            retrieve = self.session.get(self.task["PRODUCT"],headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.collect()


        if retrieve.status_code == 200:
            self.start = time.time()

            logger.warning(SITE,self.taskID,'Got product page')
            logger.prepare(SITE,self.taskID,'Getting Oauth Token...')
            try:
                getToken = self.session.post('https://airness-2.commercelayer.io/oauth/token',data={'scope':'market:2392','grant_type':'client_credentials'},headers={
                    'authorization': 'Basic b01tNXJtOGdOZDJoS01UZHZfZGMxSFd4Q1BPZXBrZHRHd2FxLWFiczhudzo=',
                    'content-type': 'application/x-www-form-urlencoded',
                    'origin': 'https://airness.it',
                    'referer': self.task["PRODUCT"],
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.collect()

            if getToken.status_code == 200:
                self.accesToken = getToken.json()["access_token"]
                logger.warning(SITE,self.taskID,'Retrieved oauth token')
                self.skus()
            elif getToken.status_code != 200:
                logger.error(SITE,self.taskID,'Failed to retrieve oauth token. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.collect()

        else:
            logger.error(SITE,self.taskID,'Failed to get product page. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.collect()

    def skus(self):

            try:
                logger.prepare(SITE,self.taskID,'Getting product data...')
                if '/en/' in self.task["PRODUCT"]:
                    self.region = '/en/'
                elif '/it/' in self.task["PRODUCT"]:
                    self.region = '/it/'

                slug = self.task["PRODUCT"].split(self.region)[1].replace('/','')
                url = 'https://cdn.contentful.com/spaces/40i19ww9637w/environments/master/entries'
                querystring = {"content_type":"node","fields.slug[in]":slug,"fields.toRoot":"true","include":"2","limit":"1","locale":"en-US"}
                
                payload = ""
                headers = {
                    'accept': "application/json, text/plain, */*",
                    'accept-language': "en-US,en;q=0.9",
                    'authorization': "Bearer DV9XvUVfM7e4yj0PxpHnm-0Hz0SByyAXqOE6IS9iV4o",
                    'origin': "https://airness.it",
                    'referer': self.task["PRODUCT"],
                    'sec-fetch-dest': "empty",
                    'sec-fetch-mode': "cors",
                    'sec-fetch-site': "cross-site",
                    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
                    }
                
                response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.skus()
            
            if response.json()["items"] == []:
                logger.error(SITE,self.taskID,'Sizes not loaded...')
                time.sleep(int(self.task["DELAY"]))
                self.skus()
            
            try:
                self.listingImages = response.json()["includes"]["Asset"]
                self.image = self.listingImages[4]["fields"]["file"]["url"]
    
                self.filterColors = []
                for i in response.json()["includes"]["Entry"]:
                    if i["sys"]["contentType"]["sys"]["id"] == "product":
                        details = i
                        try:
                            self.comingSoon = details["fields"]["comingSoon"]
                        except Exception as e:
                            log.info(e)
                            self.comingSoon = False
    
                        if self.comingSoon == True:
                            logger.warning(SITE,self.taskID,'Product "Coming Soon". Retrying...')
                            time.sleep(int(self.task["DELAY"]))
                            self.skus()
    
                        try:
                            self.instagramBlock = details["fields"]["htmlBlockInstagram"]
                        except Exception as e:
                            log.info(e)
                            self.instagramBlock = None
    
                        self.sku = details["fields"]["sku"]
                        self.name = details["fields"]["name"]
                        self.description = details["fields"]["description"]
                        self.colourLabel = details["fields"]["colorLabel"]
                        self.collection = details["fields"]["collection"]
                        self.outlet = details["fields"]["outlet"]
                        self.restockable = details["fields"]["restockable"]
                        self.reference = details["sys"]["id"]
    
                    
                    if i["sys"]["contentType"]["sys"]["id"] == "filterColor":
                        self.filterColors.append(i)
                    if i["sys"]["contentType"]["sys"]["id"] == "filterGender":
                        self.filterGender = i
                    if i["sys"]["contentType"]["sys"]["id"] == "filterCategory":
                        self.filterCategory = i
                    if i["sys"]["contentType"]["sys"]["id"] == "filterBrand":
                        self.filterBrand = i
                    if i["sys"]["contentType"]["sys"]["id"] == "filterFamily":
                        self.filterFamily = i
            except Exception as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Failed to scrape data. Retrying...')
                self.skus()
                

            #except:
            #    logger.productPage('',False,SITE,None,self.taskID)
            #    time.sleep(int(self.task["DELAY"]))
            #    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            #    self.skus()

            try:
                logger.prepare(SITE,self.taskID,'Getting product skus...')
                url = "https://airness-2.commercelayer.io/api/skus"

                querystring = {"filter[q][reference_eq]":self.sku,"page[number]":"1","page[size]":"25"}
                
                payload = ""
                headers = {
                    'accept': "application/json, text/plain, */*",
                    'accept-language': "en-US,en;q=0.9",
                    'authorization': "Bearer {}".format(self.accesToken),
                    'origin': "https://airness.it",
                    'referer': self.task["PRODUCT"],
                    'sec-fetch-dest': "empty",
                    'sec-fetch-mode': "cors",
                    'sec-fetch-site': "cross-site",
                    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
                    }
                
                response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.skus()

            if response.status_code == 401:
                logger.error(SITE,self.taskID,'Failed to get api. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.skus()
            else:
                skuData = response.json()["data"]
                self.skuData = response.json()["data"]
                allSizes = []
                sizes = []
                for sku in skuData:
                    skuid = sku["id"]
                    attributes = sku["attributes"]
                    skuCode = attributes["code"]
                    fullName = attributes["name"]

                    skuUsSize = attributes["metadata"]["US"]
                    skuPSKU = attributes["metadata"]["PSKU"]
                    skuORDER = attributes["metadata"]["ORDER"]
                    skuCategory = attributes["metadata"]["CATEGORY"]
                    #size : sku code : full name : created at : updated at : sku psku : sku order : sku category
                    allSizes.append('{}:{}:{}:{}:{}:{}:{}'.format(skuUsSize,skuCode,fullName,skuPSKU,skuORDER,skuCategory,skuid))
                    sizes.append(skuUsSize)
                
                
                #US SIZING
                if self.task["SIZE"] != "random": 
                    if self.task["SIZE"] not in sizes:
                        logger.error(SITE,self.taskID,'Size Not Found')
                        time.sleep(int(self.task["DELAY"]))
                        self.skus()
                    else:
                        for s in allSizes:
                            if s.split(':')[0] == self.task["SIZE"]:
                                self.size = s.split(':')[0]
                                self.skuCode = s.split(':')[1]
                                self.fullName = s.split(':')[2]
                                self.skuPSKU = s.split(':')[3]
                                self.skuORDER = s.split(':')[4]
                                self.skuCategory = s.split(':')[5]
                                self.skuId = s.split(':')[6]
                                logger.warning(SITE,self.taskID,f'Found Size => {self.size}')

                elif self.task["SIZE"] == "random":
                    s = random.choice(allSizes)
                    self.size = s.split(':')[0]
                    self.skuCode = s.split(':')[1]
                    self.fullName = s.split(':')[2]
                    self.skuPSKU = s.split(':')[3]
                    self.skuORDER = s.split(':')[4]
                    self.skuCategory = s.split(':')[5]
                    self.skuId = s.split(':')[6]
                    logger.warning(SITE,self.taskID,f'Found Size => {self.size}')

                
                self.addToCart()

    def addToCart(self):
        logger.prepare(SITE,self.taskID,'Carting product...')

        try:
            payload = {
                "data":{
                    "type":"orders",
                    "attributes":{
                        "language_code":"en",
                        "cart_url":"https://airness.it/{}/checkout/bag".format(self.region),
                        "return_url":"https://airness.it/{}/checkout/order-complete".format(self.region),
                        "terms_url":"https://airness.it/{}/terms-of-sale".format(self.region),
                        "privacy_url":"https://airness.it/{}/privacy-policy".format(self.region)
                    }
                }
            }
            headers = {
                'authority': 'airness-2.commercelayer.io',
                'path': '/api/orders',
                'scheme': 'https',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'en-US,en;q=0.9',
                'authorization': 'Bearer {}'.format(self.accesToken) ,
                'content-type': 'application/vnd.api+json',
                'origin': 'https://airness.it',
                'referer': self.task["PRODUCT"],
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
            }
            
            response = self.session.post('https://airness-2.commercelayer.io/api/orders', json=payload, headers=headers)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()

        if response.status_code == 201:
    
            self.checkoutUrl = response.json()["data"]["attributes"]["checkout_url"]
            self.orderId = response.json()["data"]["id"]
        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()


        
        variants = []
        order = 124
        for i in self.skuData:
            order = order + 1
            variants.append({
                "fields":{
                    "name":i["attributes"]["name"],
                    "size":{
                        "fields":{
                            "us":i["attributes"]["metadata"]["US"],
                            "uk":i["attributes"]["metadata"]["UK"],
                            "eu":i["attributes"]["metadata"]["EU"]
                        }
                    },
                    "code":{
                        "id":i["id"],
                        "code":i["attributes"]["code"],
                        "link":i["links"]["self"]
                    },
                    "order":order
                }
            })
        cartPayload = {
            "data":{
                "type":"line_items",
                "attributes":{
                    "quantity":1,
                    "reference":self.reference,
                    "image_url":self.image,
                    "metadata":{
                        "name":self.name,
                        "sku":self.sku,
                        "listingImage":[
                        self.listingImages
                        ],
                        "colorLabel":self.colourLabel,
                        "description":
                        self.description
                        ,
                        "htmlBlockInstagram":self.instagramBlock,
                        "filterGender":[
                        self.filterGender
                        ],
                        "filterColor":[
                        self.filterColors
                        ],
                        "filterBrand":
                        self.filterBrand
                        ,
                        "filterCategory":
                        self.filterCategory
                        ,
                        "filterFamily":
                        self.filterFamily
                        ,
                        "collection":self.collection,
                        "outlet":self.outlet,
                        "restockable":self.restockable,
                        "comingSoon":self.comingSoon,
                        "listingsOrder":1,
                        "variants":variants
                    },
                },
                "relationships":{
                    "order":{
                        "data":{
                            "type":"orders",
                            "id":self.orderId
                        }
                    },
                    "item":{
                        "data":{
                            "type":"skus",
                            "id":self.skuId
                        }
                    }
                }
            }
        }

        try:
            headers = {
                'authority': 'airness-2.commercelayer.io',
                'path': '/api/line_items',
                'scheme': 'https',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'en-US,en;q=0.9',
                'authorization': 'Bearer {}'.format(self.accesToken) ,
                'content-type': 'application/vnd.api+json',
                'origin': 'https://airness.it',
                'referer': self.task["PRODUCT"],
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
            }
            
            response = self.session.post('https://airness-2.commercelayer.io/api/line_items', json=cartPayload, headers=headers)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.addToCart()

        if response.status_code == 201:
            updateConsoleTitle(True,False,SITE)
            logger.warning(SITE,self.taskID,'Successfully carted')
            self.checkout()
        if response.status_code == 422:
            logger.error(SITE,self.taskID,'Failed to cart. [{}]'.format(response.json()["errors"][0]["meta"]["error"]))
            time.sleep(int(self.task["DELAY"]))
            if self.task["SIZE"] == "random":
                self.skus()
            else:
                self.addToCart()
        else:
            logger.error(SITE,self.taskID,'Failed to cart. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()


    def checkout(self):
        logger.info(SITE,self.taskID,'Initializing checkout...')
        headers = {
            'authority': 'checkout.airness.it',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9',
            'referer': self.task["PRODUCT"],
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-site',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }
        try:
            getCheckout = self.session.get(self.checkoutUrl,headers=headers)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.checkout()

        logger.warning(SITE,self.taskID,'Checkout initialized')
        if getCheckout.status_code == 200:
            logger.prepare(SITE,self.taskID,'Getting Oauth Token...')

            try:
                getToken = self.session.post('https://airness-2.commercelayer.io/oauth/token',json={'client_id':'oMm5rm8gNd2hKMTdv_dc1HWxCPOepkdtGwaq-abs8nw','grant_type':'client_credentials'},headers={
                    'content-type': 'application/json',
                    'origin': self.checkoutUrl,
                    'referer': self.task["PRODUCT"],
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.collect()

            if getToken.status_code == 200:
                self.accesToken = getToken.json()["access_token"]
                logger.warning(SITE,self.taskID,'Retrieved oauth token')
                self.customer()
            elif getToken.status_code != 200:
                logger.error(SITE,self.taskID,'Failed to retrieve oauth token. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.checkout()

        else:
            logger.error(SITE,self.taskID,'Failed to get checkout. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.checkout()


    def customer(self):
        profile = loadProfile(self.task["PROFILE"])
        if profile == None:
            logger.error(SITE,self.taskID,'Profile Not Found.')
            time.sleep(10)
            sys.exit()
        countryCode = profile["countryCode"]
        logger.prepare(SITE,self.taskID,'Submitting customer email...')
        headers = {
            'authority': 'airness-2.commercelayer.io',
            'scheme': 'https',
            'content-type': 'application/vnd.api+json',
            'authorization': 'Bearer {}'.format(self.accesToken),
            'accept-language': 'en-US,en;q=0.9',
            'referer': self.checkoutUrl,
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-user': '?1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }
        url = 'https://airness-2.commercelayer.io/api/orders/{}?include=line_items,billing_address,shipping_address,shipments.shipment_line_items.line_item,shipments.available_shipping_methods,shipments.shipping_method,available_payment_methods,payment_method,payment_source'.format(self.orderId)
        payload = {"data":{"type":"orders","id":self.orderId,"attributes":{"customer_email":profile["email"]}}}
        try:
            getCheckout = self.session.patch(url,headers=headers,json=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.checkout()

        if getCheckout.status_code == 200:
            logger.warning(SITE,self.taskID,'Successfully set email')
            payload = {
                "data":{
                    "type":"addresses",
                    "attributes":{
                        "first_name":profile["firstName"],
                        "last_name":profile["lastName"],
                        "line_1":profile["addressOne"],
                        "line_2":profile["addressTwo"],
                        "city":profile["city"],
                        "zip_code":profile["zip"],
                        "state_code":profile["region"],
                        "country_code":countryCode,
                        "phone":profile["phone"],
                        "billing_info":""
                    }
                }
            }
            logger.prepare(SITE,self.taskID,'Submitting customer address...')
            try:
                setAddress = self.session.post('https://airness-2.commercelayer.io/api/addresses',headers=headers,json=payload)
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.checkout()

            if setAddress.status_code == 201:
                self.addressId = setAddress.json()["data"]["id"]
                try:
                    payload = {"data":{"type":"orders","id":self.orderId,"attributes":{"_shipping_address_same_as_billing":True},"relationships":{"billing_address":{"data":{"type":"addresses","id":self.addressId}}}}}
                    patchBilling = self.session.patch(url,headers=headers,json=payload)
                except:
                    logger.error(SITE,self.taskID,'Connection Error. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                    self.checkout()

                if patchBilling.status_code == 200:
                    try:
                        self.paymentMethodId = patchBilling.json()["data"]["relationships"]["available_payment_methods"]["data"][0]["id"]
                        self.shipmentId = patchBilling.json()["data"]["relationships"]["shipments"]["data"][0]["id"]
                        self.methodId = patchBilling.json()["included"][4]["relationships"]["available_shipping_methods"]["data"][0]["id"]
                    except:
                        logger.error(SITE,self.taskID,'Failed to set shipping. Retrying...')
                        time.sleep(int(self.task["DELAY"]))
                        self.checkout()
                        
                    logger.warning(SITE,self.taskID,'Successfully set shipping')
                    self.shippingMethod()
                else:
                    logger.error(SITE,self.taskID,'Failed to set shipping. Retrying...')
                    time.sleep(int(self.task["DELAY"]))
                    self.checkout()

            else:
                logger.error(SITE,self.taskID,'Failed to set shipping. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.checkout()

        else:
            logger.error(SITE,self.taskID,'Failed to set email. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.checkout()

    def shippingMethod(self):
        logger.prepare(SITE,self.taskID,'Submitting shipping method....')
        headers = {
            'authority': 'airness-2.commercelayer.io',
            'scheme': 'https',
            'content-type': 'application/vnd.api+json',
            'authorization': 'Bearer {}'.format(self.accesToken),
            'accept-language': 'en-US,en;q=0.9',
            'referer': self.checkoutUrl,
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }
        url = 'https://airness-2.commercelayer.io/api/shipments/{}?include=shipment_line_items.line_item,available_shipping_methods,shipping_method'.format(self.shipmentId)

        try:
            payload = {"data":{"type":"shipments","id":self.shipmentId,"relationships":{"shipping_method":{"data":{"type":"shipping_methods","id":self.methodId}}}}}
            patchMethod = self.session.patch(url,headers=headers,json=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.checkout()

        if patchMethod.status_code == 200:
            data = patchMethod.json()["included"]
            for i in data:
                if i["type"] == "line_items":
                    self.productPrice = i["attributes"]["formatted_total_amount"]

            logger.warning(SITE,self.taskID,'Successfully set shipping method')
            self.payment()
        else:
            logger.error(SITE,self.taskID,'Failed to set shipping method. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.shippingMethod()

    def payment(self):
        logger.info(SITE,self.taskID,'Starting [PAYPAL] checkout...')
        headers = {
            'authority': 'airness-2.commercelayer.io',
            'scheme': 'https',
            'content-type': 'application/vnd.api+json',
            'authorization': 'Bearer {}'.format(self.accesToken),
            'accept-language': 'en-US,en;q=0.9',
            'referer': self.checkoutUrl,
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }
        url = 'https://airness-2.commercelayer.io/api/orders/{}?include=line_items,billing_address,shipping_address,shipments.shipment_line_items.line_item,shipments.available_shipping_methods,shipments.shipping_method,available_payment_methods,payment_method,payment_source'.format(self.orderId)

        try:
            payload = {"data":{"type":"orders","id":self.orderId,"relationships":{"payment_method":{"data":{"type":"payment_methods","id":self.paymentMethodId}}}}}
            patchPayment = self.session.patch(url,headers=headers,json=payload)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,self.taskID,'Error: {}'.format(e))
            time.sleep(int(self.task["DELAY"]))
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            self.payment()


        if patchPayment.status_code == 200:
            logger.prepare(SITE,self.taskID,'Setting payment method...')
            try:
                payload = {"data":{"type":"paypal_payments","attributes":{"return_url":"https://checkout.airness.it/{}/paypal".format(self.orderId),"cancel_url":self.checkoutUrl},"relationships":{"order":{"data":{"type":"orders","id":self.orderId}}}}}
                postPaypal = self.session.post('https://airness-2.commercelayer.io/api/paypal_payments',headers=headers,json=payload)
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                time.sleep(int(self.task["DELAY"]))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                self.payment()

            if postPaypal.status_code == 201:
                self.end = time.time() - self.start
                logger.warning(SITE,self.taskID,'Successfully set payment method')
                self.paypalUrl = postPaypal.json()["data"]["attributes"]["approval_url"]
                logger.alert(SITE,self.taskID,'Sending PayPal checkout to Discord!')
                updateConsoleTitle(False,True,SITE)

                url = storeCookies(self.paypalUrl,self.session, self.productTitle, self.productImage, self.productPrice)

                self.productImage = 'https:{}'.format(self.image)
                try:
                    discord.success(
                        webhook=loadSettings()["webhook"],
                        site=SITE,
                        url=url,
                        image=self.productImage,
                        title=self.name,
                        size=self.size,
                        price=self.productPrice,
                        paymentMethod='PayPal',
                        profile=self.task["PROFILE"],
                        product=self.task["PRODUCT"],
                        proxy=self.session.proxies,
                        speed=self.end
                    )
                    sendNotification(SITE,self.name)
                    while True:
                        pass
                except:
                    logger.alert(SITE,self.taskID,'Failed to send webhook. Checkout here ==> {}'.format(url))
            else:
                self.productImage = 'https:{}'.format(self.image)
                try:
                    discord.failed(
                        webhook=loadSettings()["webhook"],
                        site=SITE,
                        url=self.task["PRODUCT"],
                        image=self.productImage,
                        title=self.name,
                        size=self.size,
                        price=self.productPrice,
                        paymentMethod='PayPal',
                        profile=self.task["PROFILE"],
                        proxy=self.session.proxies
                    )
                except:
                    pass
                logger.error(SITE,self.taskID,'Failed to set payment method. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.payment()


        else:
            logger.error(SITE,self.taskID,'Failed to set payment method. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.payment()



        

