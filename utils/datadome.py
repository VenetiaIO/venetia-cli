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
from utils.functions import (encodeURIComponent,decodeURIComponent,loadSettings,loadProxy,injection)

api_base = 'https://datadome.invincible.services/api/v1/datadome/'
headers = {"apiKey":"f441379a-8a72-4e41-8332-7749cc69b00f"}
class datadome:
    @staticmethod
    def reCaptchaMethod(SITE,taskID,session,responseUrl):
        try:
            datadomeCookie = str(session.cookies).split('datadome=')[1].split(' ')[0]
            geoUrl = 'https://geo.captcha-delivery.com/captcha/'
            geoParams = {
                'initialCid': responseUrl.split('?initialCid=')[1].split('&')[0],
                'referer': responseUrl.split('&referer=')[1].split('&')[0],
                'hash': responseUrl.split('&hash=')[1].split('&')[0],
                't': responseUrl.split('&t=')[1].split('&')[0],
                's': responseUrl.split('&s=')[1],
                'cid': datadomeCookie
            }
        except Exception:
            return {"cookie":None}
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
            logger.error(SITE,taskID,'Error: {}'.format(e))

        try:
            if 'You have been blocked' in response.text:
                logger.error(SITE,taskID,'Blocked. Rotating Proxy...')
                # print(session.proxies)
                time.sleep(5)
                return {"cookie":None}
            else:
                try:
                    siteKey = response.text.split("'sitekey' : '")[1].split("'")[0]
                    capResponse = captcha.v2(siteKey,response.url,session.proxies,SITE,taskID)
                except Exception:
                    reCaptchaMethod(SITE,taskID,session,responseUrl)
        except Exception:
            return {"cookie":None}

        params = {
            "cid": encodeURIComponent(datadomeCookie),
            "icid": encodeURIComponent(response.text.split("'&icid=' + encodeURIComponent('")[1].split("'")[0]),
            "ccid": None,
            "g-recaptcha-response": capResponse,
            "hash": encodeURIComponent(response.text.split("'&hash=' + encodeURIComponent('")[1].split("'")[0]),
            "ua": encodeURIComponent(response.text.split("'&ua=' + encodeURIComponent('")[1].split("'")[0]),
            "referer": encodeURIComponent('https://' + response.text.split("'&referer=' + encodeURIComponent('")[1].split("'")[0]),
            "parent_url":encodeURIComponent('https://' + response.text.split("'&referer=' + encodeURIComponent('")[1].split("'")[0]),
            "x-forwarded-for": encodeURIComponent(response.text.split("'&x-forwarded-for=' + encodeURIComponent('")[1].split("'")[0]),
            "captchaChallenge": 'false',
            "s": encodeURIComponent(response.text.split("'&s=' + encodeURIComponent('")[1].split("'")[0]),
        }

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
            logger.error(SITE,taskID,'Error: {}'.format(e))
        
        if response.status_code == 200:
            try:
                cookie = response.json()['cookie'].split('datadome=')[1].split(';')[0]
            except:
                logger.error(SITE,taskID,'Failed to get cookie. Retrying...')
                return {"cookie":None}
            
            logger.success(SITE,taskID,'Retrieved cookie')
            return {"cookie":cookie}
                    
    
    



