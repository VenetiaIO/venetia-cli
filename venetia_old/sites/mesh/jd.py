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
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies, updateConsoleTitle,scraper)
SITE = 'JD'
from tls.client import Session

class JD:
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

    def __init__(self, task,taskName, rowNumber):
        self.task = task
        # self.session = requests.session()
        self.session = Session()
        self.taskID = taskName
        self.rowNumber = rowNumber

        twoCap = loadSettings()["2Captcha"]
        # self.session = scraper()
        
        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)


        self.collect()

    def collect(self):
        self.region = '.co.uk'
        while True:
            if 'https' in self.task['PRODUCT']:
                self.url = self.task['PRODUCT']
            else:
                self.url = f'https://www.jdsports{self.region}/product/-/' + self.task['PRODUCT'] + '/stock/?_=' + str(int(time.time()))

            logger.prepare(SITE,self.taskID,'Getting product page...')
            try:
                retrieve = self.session.get(self.url,headers={
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/json',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest'
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue

            if retrieve.status_code == 200:
                logger.warning(SITE,self.taskID,'Got product page')

                try:
                    soup = BeautifulSoup(retrieve.text, "html.parser")
                    foundSizes = soup.find_all('button',{'data-e2e':'pdp-productDetails-size'})
                    
                    allSizes = []
                    sizes = []

                    for s in foundSizes:
                        try:
                            allSizes.append('{}:{}:{}'.format(s['title'].split(' ')[2],s['data-sku'],s['data-upc']))
                            sizes.append(s['title'].split(' ')[2])
                        except:
                            pass

                    if len(sizes) == 0:
                        logger.error(SITE,self.taskID,'Size Not Found')
                        time.sleep(int(self.task["DELAY"]))
                        continue

                        
                    if self.task["SIZE"].lower() != "random":
                        if self.task["SIZE"] not in sizes:
                            logger.error(SITE,self.taskID,'Size Not Found')
                            time.sleep(int(self.task["DELAY"]))
                            continue
                        else:
                            for size in allSizes:
                                if size.split(':')[0] == self.task["SIZE"]:
                                    self.size = size.split(':')[0]
                                    self.sizeSKU = size.split(':')[1]
                                    self.sizeUPC = size.split(":")[2]
                                    logger.warning(SITE,self.taskID,f'Found Size => {self.size}')
        
                    
                    elif self.task["SIZE"].lower() == "random":
                        selected = random.choice(allSizes)
                        self.size = selected.split(":")[0]
                        self.sizeSKU = selected.split(":")[1]
                        self.sizeUPC = selected.split(":")[2]
                        logger.warning(SITE,self.taskID,f'Found Size => {self.size}')

                    
                except Exception as e:
                    log.info(e)
                    continue

                self.addToCart()
            else:
                logger.error(SITE,self.taskID,f'Failed to get product page => {str(retrieve.status_code)}. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                continue

    def addToCart(self):
        while True:
            logger.prepare(SITE,self.taskID,'Carting product...')


            try:
                response = self.session.post(f'https://www.jdsports{self.region}/cart/{self.sizeSKU}/',headers={
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/json',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                    'newrelic': ''
                },data=json.dumps({
                "customisations":False,
                "cartPosition":'null',
                "recaptchaResponse":False,
                "cartProductNotification":'null',
                "quantityToAdd":1
            }))
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue


            if 'forbidden' in response.text.lower():
                logger.error(SITE,self.taskID,'Blocked.Retrying...')
                time.sleep(int(self.task["DELAY"]))
                continue

            try:
                responseBody = json.loads(response.text)
            except Exception as e:
                log.info(e)
                time.sleep(int(self.task["DELAY"]))
                continue
            if response.status_code == 200 and responseBody:
                logger.warning(SITE,self.taskID,'Successfully Carted')

                try:
                    self.deliveryData = responseBody['delivery']
                    self.cartID = responseBody['ID']
                    self.productTitle = responseBody['contents'][0]['name']
                    self.productPrice = '{} {}'.format(responseBody['productsSubtotal']['amount'],responseBody['productsSubtotal']['currency'])
                    self.productImage = responseBody['contents'][0]['image']['originalURL']
                except Exception as e:
                    log.info(e)
                    time.sleep(int(self.task["DELAY"]))
                    continue
                
                self.guestCheckout()
                
            else:
                logger.error(SITE,self.taskID,'Failed to cart')
                time.sleep(int(self.task["DELAY"]))
                continue
        

    def guestCheckout(self):
        while True:
            logger.prepare(SITE,self.taskID,'Setting email...')

            self.profile = loadProfile(self.task["PROFILE"])
            if self.profile == None:
                logger.error(SITE,self.taskID,'Profile Not Found.')
                time.sleep(10)
                sys.exit()


            try:
                response = self.session.post(f'https://www.jdsports{self.region}/checkout/guest/',headers={
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/json',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                    'newrelic': ''
                },data=json.dumps({
                "email":self.profile['email']
            }))
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue
            
            print(response)
            print(response.text)
            break
            return
            try:
                responseBody = json.loads(response.text)
            except Exception as e:
                log.info(e)
                time.sleep(int(self.task["DELAY"]))
                continue
            if response.status_code == 200 and responseBody:
                logger.warning(SITE,self.taskID,'Successfully set email')
                
            else:
                logger.error(SITE,self.taskID,'Failed to set email')
                time.sleep(int(self.task["DELAY"]))
                continue
    

    def deliveryMethod(self):
        while True:
            logger.prepare(SITE,self.taskID,'Setting delivery...')

            self.profile = loadProfile(self.task["PROFILE"])
            if self.profile == None:
                logger.error(SITE,self.taskID,'Profile Not Found.')
                time.sleep(10)
                sys.exit()


            try:
                response = self.session.put(f'https://www.jdsports{self.region}/cart/',headers={
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                    'newrelic': ''
                },data='{"deliveryMethodID":"{}","deliveryLocation":"{}"}'.format(self.deliveryData['deliveryMethodID'],self.profile['countryCode'].lower()))
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue
            
            print(response)
            print(response.text)
            break
            return
            try:
                responseBody = json.loads(response.text)
            except Exception as e:
                log.info(e)
                time.sleep(int(self.task["DELAY"]))
                continue
            if response.status_code == 200 and responseBody:
                logger.warning(SITE,self.taskID,'Successfully set delivery')
                
            else:
                logger.error(SITE,self.taskID,'Failed to set delivery')
                time.sleep(int(self.task["DELAY"]))
                continue
    
    def shipping(self):
        while True:
            logger.prepare(SITE,self.taskID,'Setting delivery...')

            self.profile = loadProfile(self.task["PROFILE"])
            if self.profile == None:
                logger.error(SITE,self.taskID,'Profile Not Found.')
                time.sleep(10)
                sys.exit()


            try:
                response = self.session.put(f'https://www.jdsports{self.region}/myaccount/addressbook/add/',headers={
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/json',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                    'newrelic': ''
                },data=json.dumps({
                    "useDeliveryAsBilling":True,
                    "country":"United Kingdom|gb",
                    "locale":"",
                    "firstName":self.profile['firstName'],
                    "lastName":self.profile['lastName'],
                    "phone":self.profile['phone'],
                    "address1":'{} {}'.format(self.profile['house'], self.profile['addressOne']),
                    "address2":self.profile['addressTwo'],
                    "town":self.profile['city'],
                    "county":self.profile['region'],
                    "postcode":self.profile['zip'],
                    "addressPredict":"",
                    "setOnCart":"deliveryAddressID",
                    "addressPredictflag":"false"
                }))
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                logger.error(SITE,self.taskID,'Error: {}'.format(e))
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
                time.sleep(int(self.task["DELAY"]))
                continue
            
            print(response)
            print(response.text)
            break
            return
            try:
                responseBody = json.loads(response.text)
            except Exception as e:
                log.info(e)
                time.sleep(int(self.task["DELAY"]))
                continue
            if response.status_code == 200 and responseBody:
                logger.warning(SITE,self.taskID,'Successfully set delivery')
                
            else:
                logger.error(SITE,self.taskID,'Failed to set delivery')
                time.sleep(int(self.task["DELAY"]))
                continue
            
           


