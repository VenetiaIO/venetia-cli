import requests
import re
import json
import urllib.parse
import time
import random
import threading
import cloudscraper
import urllib

from utils.logger import logger
from utils.captcha import captcha
from helheim import helheim
from utils.log import log
from utils.functions import (encodeURIComponent,decodeURIComponent,loadSettings,loadProxy,injection)

api_base = 'https://datadome.invincible.services/api/v1/datadome/'
headers = {"apiKey":"f441379a-8a72-4e41-8332-7749cc69b00f"}
class datadome:
    @staticmethod
    def reCaptchaMethod(SITE,taskID,session,responseUrl, siteUrl):
        try:
            responseUrl = responseUrl.replace('&t=bv','')
        except:
            pass

        # https://geo.captcha-delivery.com/captcha/
        # ?initialCid=AHrlqAAAAAMAS2mURaQAc8YAueGcYg==
        # &referer=www.footlocker.co.uk?
        # &hash=A55FBF4311ED6F1BF9911EB71931D5
        # &s=17434
        try:
            datadomeCookie = str(session.cookies).split('datadome=')[1].split(' ')[0]
            geoUrl = 'https://geo.captcha-delivery.com/captcha/'
            geoParams = {
                'initialCid': responseUrl.split('?initialCid=')[1].split('&')[0],
                'referer': responseUrl.split('&referer=')[1].split('&')[0],
                'hash': responseUrl.split('&hash=')[1].split('&')[0],
                's': responseUrl.split('&s=')[1],
                'cid': datadomeCookie
            }
        except Exception as e:
            log.info(e)
            return {"cookie":None}

        try:
            geoParams['t'] = responseUrl.split('&t=')[1].split('&')[0]
        except:
            pass
        try:
            response = session.get(geoUrl,params=geoParams,headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-language": "en-US,en;q=0.9",
                "sec-ch-ua": "\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"",
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-dest": "iframe",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "cross-site",
                "upgrade-insecure-requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"

            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,taskID,'Error: {}'.format(e))


        try:
            siteKey = response.text.split("'sitekey' : '")[1].split("'")[0]
            capResponse = captcha.v2(siteKey,siteUrl,session.proxies,SITE,taskID)
        except Exception as e:
            log.info(e)
            logger.error(SITE,taskID,'Failed to solve captcha. Retrying...')
            return {"cookie":None}

        try:
            params = {
                "cid": encodeURIComponent(datadomeCookie),
                "icid": encodeURIComponent(response.text.split("'&icid=' + encodeURIComponent('")[1].split("'")[0]),
                "ccid": '',
                "g-recaptcha-response": capResponse,
                "hash": encodeURIComponent(response.text.split("'&hash=' + encodeURIComponent('")[1].split("'")[0]),
                "ua": encodeURIComponent(response.text.split("'&ua=' + encodeURIComponent('")[1].split("'")[0]),
                "referer": encodeURIComponent('https://' + response.text.split("'&referer=' + encodeURIComponent('")[1].split("'")[0]),
                "parent_url":encodeURIComponent('https://' + response.text.split("'&referer=' + encodeURIComponent('")[1].split("'")[0]),
                "x-forwarded-for": encodeURIComponent(response.text.split("'&x-forwarded-for=' + encodeURIComponent('")[1].split("'")[0]),
                "captchaChallenge": 'false',
                "s": encodeURIComponent(response.text.split("'&s=' + encodeURIComponent('")[1].split("'")[0]),
            }
        except Exception as e:
            log.info(e)
            logger.error(SITE,taskID,'Failed to get cookie. Retrying...')
            return {"cookie":None}

        try:
            response = session.get('https://geo.captcha-delivery.com/captcha/check',params=params,headers={
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.9",
                "sec-ch-ua": "\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"",
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-dest": "iframe",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "cross-site",
                "upgrade-insecure-requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"

            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,taskID,'Error: {}'.format(e))
        
  
        if response.status_code == 200:
            try:
                cookie = response.json()['cookie'].split('datadome=')[1].split(';')[0]
            except:
                logger.error(SITE,taskID,'Failed to get cookie. Retrying...')
                return {"cookie":None}
            
            logger.success(SITE,taskID,'Retrieved cookie')
            return {"cookie":cookie}
        
        else:
            logger.error(SITE,taskID,'Failed to get cookie. Retrying...')
            return {"cookie":None}
                    
    
    



