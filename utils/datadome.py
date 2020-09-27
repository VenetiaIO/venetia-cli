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

def injection(session, response):
    if session.is_New_IUAM_Challenge(response):
        return helheim('2044b982-151b-4fca-974d-ebad6fd10bec', session, response)
    else:
        return response

def loadSettings():
    with open(f'./data/config.json') as settings:
        settings = json.loads(settings.read())
        return settings

def loadProxy(proxies,taskID):
    if proxies == "":
        return None
    elif proxies != "":
        with open(f'./data/{proxies}.txt', 'r') as proxyIn:
            proxyInput = proxyIn.read().splitlines()
    
        proxyList = [i for i in proxyInput]
        p = random.choice(proxyList)
        p = p.split(':')
        try:
            proxies = {
                'http': f'http://{p[2]}:{p[3]}@{p[0]}:{p[1]}',
                'https': f'https://{p[2]}:{p[3]}@{p[0]}:{p[1]}'
            }
        except:
            proxies = {
                'http': f'http://{p[0]}:{p[1]}',
                'https': f'https://{p[0]}:{p[1]}'
            }
        return proxies

def encodeURIComponent(str):
    encoded = urllib.parse.quote(str, safe='~()*!.\'')
    return encoded

def decodeURIComponent(str):
    decoded = urllib.parse.unquote(str)
    return decoded

class datadome:
    @staticmethod
    def courir(proxies):
        siteKey = '6LccSjEUAAAAANCPhaM2c-WiRxCZ5CzsjR_vd8uX'
        site = 'https://www.courir.com'
        session = requests.session()
        session.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "dnt": "1",
            "pragma": "no-cache",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        }

        if proxies == None:
            session.proxies = None
        else:
            session.proxies = loadProxy(proxies,'COOKIE GEN')

        try:
            challenge = session.get(site)
        except (Exception, ConnectionError) as e:
            logger.error('COURIR','COOKIE GEN','Failed to generate cookie. ERROR: {}'.format(e))

        while 'DDUser' not in challenge.url:
            logger.error('COURIR','COOKIE GEN','Error getting challenge page. Retrying...')
            time.sleep(3)
            challenge = session.get(site)

        if 'DDUser' in challenge.url:
            matches = re.search(r"dd={.+}", challenge.text, re.MULTILINE)
            if matches:
                ddConfig = json.loads(matches.group().split('dd=')[1].replace("'",'"'))
                ddCookie = session.cookies["datadome"]
                
                geoCaptchaScript = 'https://geo.captcha-delivery.com/captcha/?initialCid={}&hash={}&cid={}&t={}&referer={}'.format(encodeURIComponent(ddConfig["cid"]),ddConfig["hsh"],decodeURIComponent(ddCookie),encodeURIComponent(ddConfig["t"]),site)
                challenge = session.get(geoCaptchaScript)
                if challenge.status_code == 200:
                    try:

                        xforwarded = challenge.text.split("'&x-forwarded-for=' + encodeURIComponent('")[1].split("'")[0]
                        geetestConfig = {
                            'api_server': challenge.text.split("api_server: '")[1].split("'")[0],
                            'gt': challenge.text.split("gt: '")[1].split("'")[0],
                            'challenge': challenge.text.split("challenge: '")[1].split("'")[0]
                        }
                        results = captcha.geetest(geetestConfig["gt"],geetestConfig["challenge"],geetestConfig["api_server"],site,proxies,'COURIR','COOKIE-GEN')
                        geetestResponseChallenge = encodeURIComponent(results["request"]["geetest_challenge"])
                        geetestResponseValidate = encodeURIComponent(results["request"]["geetest_validate"])
                        geetestResponseSeccode = encodeURIComponent(results["request"]["geetest_seccode"])
        
            
                        url = 'https://c.captcha-delivery.com/captcha/check?'
                        url += 'cid={}'.format(encodeURIComponent(ddCookie))
                        url += '&icid={}'.format(encodeURIComponent(ddConfig["cid"]))
            
                        url += '&geetest-response-challenge={}'.format(geetestResponseChallenge)
                        url += '&geetest-response-validate={}'.format(geetestResponseValidate)
                        url += '&geetest-response-seccode={}'.format(geetestResponseSeccode)
            
                        url += '&hash={}'.format(encodeURIComponent(ddConfig["hsh"]))
                        url += '&ua={}'.format(encodeURIComponent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'))
                        url += '&referer={}'.format(encodeURIComponent(challenge.url))
                        url += '&parent_url={}'.format(encodeURIComponent(challenge.url))
                        url += '&x-forwarded-for={}'.format(encodeURIComponent(xforwarded))
                        url += '&captchaChallenge=false'
                        
                        getCookie = session.get(url)
                        if getCookie.status_code == 200:
                            cookie = getCookie.json()["cookie"].split('datadome=')[1].split(';')[0]
                            logger.secondary('COURIR','COOKIE GEN','Successfully generated cookie. Storing in cookies folder...')
                            with open('./data/cookies/datadome.json') as config:
                                cookies = json.loads(config.read())
                                
                    
                            cookies['COURIR'].append({
                                "cookie":cookie,
                                "proxy":session.proxies
                            })
                    
                            with open('./data/cookies/datadome.json','w') as output:
                                json.dump(cookies,output)
                    
                    except (Exception, ConnectionError) as e:
                        logger.error('COURIR','COOKIE GEN','Failed to generate cookie. ERROR: {}'.format(e))
    
                threading.currentThread().handled = True
                    


    @staticmethod
    def slamjam(proxies,region):
        siteKey = '6LccSjEUAAAAANCPhaM2c-WiRxCZ5CzsjR_vd8uX'
        site = 'https://www.slamjam.com/on/demandware.store/Sites-slamjam-Site/en_{}/Product-Variation?pid=J11111'.format(region)
        session = requests.session()
        session.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "dnt": "1",
            "pragma": "no-cache",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        }
    
        if proxies == None:
            session.proxies = None
        else:
            session.proxies = loadProxy(proxies,'COOKIE GEN')
        
    
        try:
            challenge = session.get(site)
        except (Exception, ConnectionError, ConnectionRefusedError, TimeoutError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
            logger.error('SLAMJAM','COOKIE GEN','Failed to generate cookie. ERROR: {}'.format(e))
            threading.currentThread().handled = True
    
        if challenge:
            if 'DDUser' not in challenge.url:
                threading.currentThread().handled = True
        
            if 'DDUser' in challenge.url:
                matches = re.search(r"dd={.+}", challenge.text, re.MULTILINE)
                if matches:
                    ddConfig = json.loads(matches.group().split('dd=')[1].replace("'",'"'))
                    try:
                        ddCookie = session.cookies["datadome"]
                    except:
                        logger.error('SLAMJAM','COOKIE GEN','Failed to generate cookie')
                        threading.currentThread().handled = True
                    
                    geoCaptchaScript = 'https://geo.captcha-delivery.com/captcha/?initialCid={}&hash={}&cid={}&t={}&referer={}'.format(encodeURIComponent(ddConfig["cid"]),ddConfig["hsh"],decodeURIComponent(ddCookie),encodeURIComponent(ddConfig["t"]),site)
                    try:
                        challenge = session.get(geoCaptchaScript)
                    except (Exception, ConnectionError, ConnectionRefusedError, TimeoutError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
                        logger.error('SLAMJAM','COOKIE GEN','Failed to generate cookie. ERROR: {}'.format(e))
                        threading.currentThread().handled = True
        
                    if challenge.status_code == 200:
                        try:
                            xforwarded = challenge.text.split("'&x-forwarded-for=' + encodeURIComponent('")[1].split("'")[0]
                        except (Exception, ConnectionError) as e:
                            logger.error('SLAMJAM','COOKIE GEN','Error scraping page. Most likely blocked.')
                            threading.currentThread().handled = True
                        
        
                        captchaResponse = captcha.v2(siteKey,challenge.url,session.proxies,'SLAMJAM','COOKIE GEN')
                        url = 'https://c.captcha-delivery.com/captcha/check?'
                        url += 'cid={}'.format(encodeURIComponent(ddCookie))
                        url += '&icid={}'.format(encodeURIComponent(ddConfig["cid"]))
            
                        url += '&g-recaptcha-response={}'.format(encodeURIComponent(captchaResponse))
            
                        url += '&hash={}'.format(encodeURIComponent(ddConfig["hsh"]))
                        url += '&ua={}'.format(encodeURIComponent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'))
                        url += '&referer={}'.format(encodeURIComponent(challenge.url))
                        url += '&parent_url={}'.format(encodeURIComponent(challenge.url))
                        url += '&x-forwarded-for={}'.format(encodeURIComponent(xforwarded))
                        url += '&captchaChallenge=false'
                        getCookie = session.get(url)
                        if getCookie.status_code == 200:
                            cookie = getCookie.json()["cookie"].split('datadome=')[1].split(';')[0]
                            logger.secondary('SLAMJAM','COOKIE GEN','Successfully generated cookie')
                            with open('./data/cookies/datadome.json') as config:
                                cookies = json.loads(config.read())
                                
                    
                            cookies['SLAMJAM'].append({
                                "cookie":cookie,
                                "proxy":session.proxies
                            })
                    
                            with open('./data/cookies/datadome.json','w') as output:
                                json.dump(cookies,output)

                            threading.currentThread().handled = True
        
                        else:
                            logger.error('SLAMJAM','COOKIE GEN','Failed to generate cookie')
                            threading.currentThread().handled = True
        
                    else:
                        logger.error('SLAMJAM','COOKIE GEN','Failed to generate cookie')
                        threading.currentThread().handled = True
                else:
                    logger.error('SLAMJAM','COOKIE GEN','Failed to generate cookie')
                    threading.currentThread().handled = True
            
            else:
                logger.error('SLAMJAM','COOKIE GEN','Failed to get challenge. Retrying...')
                threading.currentThread().handled = True
    
    @staticmethod
    def starcow(proxies):
        site = 'https://www.starcowparis.com/'

        session = requests.session()

        session = cloudscraper.create_scraper(
            requestPostHook=injection,
            sess=session,
            interpreter='nodejs',
            browser={
                'browser': 'chrome',
                'mobile': False,
                'platform': 'windows'
                #'platform': 'darwin'
            },
            recaptcha={
                'provider': '2captcha',
                'api_key': loadSettings()["2Captcha"]
            }
        )

        session.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "dnt": "1",
            "pragma": "no-cache",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        }
        if proxies == None:
            session.proxies = None
        else:
            session.proxies = loadProxy(proxies,'COOKIE GEN')

        
        challenge = session.get(site)
        if challenge:
            if 'DDUser' not in challenge.url:
                threading.currentThread().handled = True

            if 'DDUser' in challenge.url:
                matches = re.search(r"dd={.+}", challenge.text, re.MULTILINE)
                if matches:
                    ddConfig = json.loads(matches.group().split('dd=')[1].replace("'",'"'))
                    ddCookie = challenge.headers['Set-Cookie'].split('datadome=')[1].split(';')[0]
            
                    
                    geoCaptchaScript = 'https://geo.captcha-delivery.com/captcha/?initialCid={}&hash={}&cid={}&t={}&referer={}'.format(encodeURIComponent(ddConfig["cid"]),ddConfig["hsh"],decodeURIComponent(ddCookie),encodeURIComponent(ddConfig["t"]),site)
                    challenge = session.get(geoCaptchaScript)
                    if challenge.status_code == 200:
                        try:
                            xforwarded = challenge.text.split("'&x-forwarded-for=' + encodeURIComponent('")[1].split("'")[0]
                
                            geetestConfig = {
                                'api_server': challenge.text.split("api_server: '")[1].split("'")[0],
                                'gt': challenge.text.split("gt: '")[1].split("'")[0],
                                'challenge': challenge.text.split("challenge: '")[1].split("'")[0]
                            }
                            results = captcha.geetest(geetestConfig["gt"],geetestConfig["challenge"],geetestConfig["api_server"],site,proxies,'STARCOW','COOKIE GEN')
                            geetestResponseChallenge = encodeURIComponent(results["request"]["geetest_challenge"])
                            geetestResponseValidate = encodeURIComponent(results["request"]["geetest_validate"])
                            geetestResponseSeccode = encodeURIComponent(results["request"]["geetest_seccode"])
                
                
                            url = 'https://c.captcha-delivery.com/captcha/check?'
                            url += 'cid={}'.format(encodeURIComponent(ddCookie))
                            url += '&icid={}'.format(encodeURIComponent(ddConfig["cid"]))
                            url += '&geetest-response-challenge={}'.format(geetestResponseChallenge)
                            url += '&geetest-response-validate={}'.format(geetestResponseValidate)
                            url += '&geetest-response-seccode={}'.format(geetestResponseSeccode)
                            url += '&hash={}'.format(encodeURIComponent(ddConfig["hsh"]))
                            url += '&ua={}'.format(encodeURIComponent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'))
                            url += '&referer={}'.format(encodeURIComponent('https://www.starcowparis.com/'))
                            url += '&parent_url={}'.format(encodeURIComponent('https://www.starcowparis.com/'))
                            url += '&x-forwarded-for={}'.format(encodeURIComponent(xforwarded))
                            url += '&captchaChallenge=false'
                            
                            getCookie = session.get(url)
                            if getCookie.status_code == 200:
                                cookie = getCookie.json()["cookie"].split('datadome=')[1].split(';')[0]
                                logger.secondary('STARCOW','COOKIE GEN','Successfully generated cookie. Storing in cookies folder...')
                                with open('./data/cookies/datadome.json') as config:
                                    cookies = json.loads(config.read())
                                    
                        
                                cookies['STARCOW'].append({
                                    "cookie":cookie,
                                    "proxy":session.proxies
                                })
                        
                                with open('./data/cookies/datadome.json','w') as output:
                                    json.dump(cookies,output)
                                threading.currentThread().handled = True
        
                        except Exception as e:
                            logger.error('STARCOW','COOKIE GEN','Failed to generate cookie. ERROR: {}'.format(e))
        
                    threading.currentThread().handled = True
    
            else:
                logger.error('STARCOW','COOKIE GEN','Failed to get challenge. Retrying...')
                threading.currentThread().handled = True
        
    
    
    
    



