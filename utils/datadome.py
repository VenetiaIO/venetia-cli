import requests
import re
import json
import urllib.parse
import time
import random
import threading
import cloudscraper

from utils.logger import logger
from utils.captcha import captcha
from helheim import helheim
from utils.functions import (encodeURIComponent,decodeURIComponent,loadSettings,loadProxy,injection)

api_base = 'https://datadome.invincible.services/api/v1/datadome/'
headers = {"apiKey":"f441379a-8a72-4e41-8332-7749cc69b00f"}
class datadome:
    @staticmethod
    def courir(proxies, taskID, mode):
        if proxies == None:
            param = ''
        elif 'http' in proxies:
            param = '?proxy=' + proxies
        else:
            param = '?proxy=' + loadProxy(proxies,'','')['https']

        param += '?2cap=' + loadSettings()["2Captcha"]

        
        try:
            r = requests.get(api_base + 'courir',headers=headers)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            print(e)
        
        if r.status_code == 200:
            logger.secondary('COURIR',taskID,'Successfully Generated DATADOME Cookie')
            if mode == 'save':
                with open('./data/cookies/datadome.json') as config:
                    cookies = json.loads(config.read())

                cookies['COURIR'].append({
                    "cookie":r.json()["cookie"],
                    "proxy":r.json()["proxy"]
                })
                with open('./data/cookies/datadome.json','w') as output:
                    json.dump(cookies,output)

            elif mode == 'return':
                return r.json()["cookie"]
        else:
            return None
        threading.currentThread().handled = True
                    


    @staticmethod
    def starcow(proxies, taskID, mode):
        if proxies == None:
            param = ''
        elif 'http' in proxies:
            param = '?proxy=' + proxies
        else:
            param = '?proxy=' + loadProxy(proxies,'','')['https']

        param += '?2cap=' + loadSettings()["2Captcha"]

        try:
            r = requests.get(api_base + 'starcow' + param,headers=headers)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            print(e)
        
        if r.status_code == 200:
            logger.secondary('STARCOW',taskID,'Successfully Generated DATADOME Cookie')
            if mode == 'save':
                with open('./data/cookies/datadome.json') as config:
                    cookies = json.loads(config.read())

                cookies['STARCOW'].append({
                    "cookie":r.json()["cookie"],
                    "proxy":r.json()["proxy"]
                })
                with open('./data/cookies/datadome.json','w') as output:
                    json.dump(cookies,output)

            elif mode == 'return':
                return r.json()["cookie"]
        else:
            return None
        threading.currentThread().handled = True

    
    @staticmethod
    def slamjam(proxies, taskID, mode):
        if proxies == None:
            param = ''
        elif 'http' in proxies:
            param = '?proxy=' + proxies['https']
        else:
            param = '?proxy=' + loadProxy(proxies,'','')['https']

        param += '?2cap=' + loadSettings()["2Captcha"]


        try:
            r = requests.get(api_base + 'slamjam',headers=headers)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            print(e)
            
        
        if r.status_code == 200:
            logger.secondary('SLAMJAM',taskID,'Successfully Generated DATADOME Cookie')
            if mode == 'save':
                with open('./data/cookies/datadome.json') as config:
                    cookies = json.loads(config.read())

                cookies['SLAMJAM'].append({
                    "cookie":r.json()["cookie"],
                    "proxy":r.json()["proxy"]
                })
                with open('./data/cookies/datadome.json','w') as output:
                    json.dump(cookies,output)

            elif mode == 'return':
                return r.json()["cookie"]
        else:
            return None
        threading.currentThread().handled = True
                    
    
    



