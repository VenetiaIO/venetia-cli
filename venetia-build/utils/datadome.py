import requests
import re
import json
import urllib.parse
import time
import random
import threading
import cloudscraper
import urllib
import js2py

from utils.logger import logger
from utils.captcha import captcha
from helheim import helheim
from utils.log import log
from utils.functions import (encodeURIComponent,decodeURIComponent,loadSettings,loadProxy,injection)

api_base = 'https://datadome.invincible.services/api/v1/datadome/'
headers = {"apiKey":"f441379a-8a72-4e41-8332-7749cc69b00f"}
class datadome:
    @staticmethod
    def reCaptchaMethod(SITE,taskID,session,responseUrl, siteUrl, UA):
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
            geoParams['t'] = responseUrl.replace('&t=bv','')
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
                "User-Agent": UA

            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            logger.error(SITE,taskID,'Error: {}'.format(e))

        with open('datadome.html','w') as dd:
            dd.write(response.text)
            dd.close()

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
                "ccid": 'null',
                "g-recaptcha-response": capResponse,
                "hash": response.text.split("'&hash=' + encodeURIComponent('")[1].split("'")[0],
                "ua": encodeURIComponent(UA),
                "referer": encodeURIComponent('https://' + response.text.split("'&referer=' + encodeURIComponent('")[1].split("'")[0]),
                "parent_url":encodeURIComponent('https://' + response.text.split("'&referer=' + encodeURIComponent('")[1].split("'")[0]),
                "x-forwarded-for": '',
                "captchaChallenge": capChallenge(datadomeCookie,10,UA,"en-US",["en-US", "en"]), #false
                "s": response.text.split("'&s=' + encodeURIComponent('")[1].split("'")[0],
            }
        except Exception as e:
            log.info(e)
            logger.error(SITE,taskID,'Failed to get cookie. Retrying...')
            return {"cookie":None}

        print(params)
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
                "User-Agent": UA

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
                    
    
    





def capChallenge(cookie,a,userAgent,language,languages):
    func = '''
    function solveChallenge(r,t,userAgent,language,languages){
        var seed = null,
            currentNumber = null,
            offsetParameter = null,
            multiplier
        function e(r, t, e) {
            seed = r
            currentNumber = r % t
            offsetParameter = t
            multiplier = e
            currentNumber <= 0 && (currentNumber += t);
        }
        var getNext = function () {
            return (
                (currentNumber =
                (multiplier * currentNumber) % offsetParameter),
                currentNumber
            );
        };
        for (
            var n = [
                function (r, t) {
                    var e = 26157,
                    n = 0;
                    if (
                    ((s =
                        "VEc5dmEybHVaeUJtYjNJZ1lTQnFiMkkvSUVOdmJuUmhZM1FnZFhNZ1lYUWdZWEJ3YkhsQVpHRjBZV1J2YldVdVkyOGdkMmwwYUNCMGFHVWdabTlzYkc5M2FXNW5JR052WkdVNklERTJOMlJ6YUdSb01ITnVhSE0"),
                    userAgent)
                    ) {
                    for (
                        var a = 0;
                        a < s.length;
                        a +=
                        1 %
                        Math.ceil(1 + 3.1425172 / userAgent.length)
                    )
                        n += s.charCodeAt(a).toString(2) | (e ^ t);
                    return n;
                    }
                    return s ^ t;
                },
                function (r, t) {
                    for (
                    var e = (
                        userAgent.length << Math.max(r, 3)
                        ).toString(2),
                        n = -42,
                        a = 0;
                    a < e.length;
                    a++
                    )
                    n += e.charCodeAt(a) ^ (t << a % 3);
                    return n;
                },
                function (r, t) {
                    for (
                    var e = 0,
                        n =
                        (language
                            ? language.substr(0, 2)
                            : void 0 !== languages
                            ? languages[0].substr(0, 2)
                            : "default"
                        ).toLocaleLowerCase() + t,
                        a = 0;
                    a < n.length;
                    a++
                    )
                    e =
                        ((e =
                        ((e +=
                            n.charCodeAt(a) << Math.min((a + t) % (1 + r), 2)) <<
                            3) -
                        e +
                        n.charCodeAt(a)) &
                        e) >>
                        a;
                    return e;
                },
                ],
                a = new e(
                (function (r) {
                    for (var t = 126 ^ r.charCodeAt(0), e = 1; e < r.length; e++)
                    t += ((r.charCodeAt(e) * e) ^ r.charCodeAt(e - 1)) >> e % 2;
                    return t;
                })(r),
                1723,
                7532
                ),
                o = seed,
                u = 0;
            u < t;
            u++
        ) {
        o ^= (0, n[getNext() % n.length])(u, seed);
        }
        return o;
    }
    '''
    solve = js2py.eval_js(func)
    return solve(
        cookie,
        10,
        userAgent,
        language,
        languages
    )