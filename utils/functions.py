import string
import random
import requests
import re
import json
import urllib.parse
import time
import random
import threading
import cloudscraper
import base64
from pynotifier import Notification
from win10toast import ToastNotifier

from utils.logger import logger
from utils.captcha import captcha
from utils.helheim import helheim

def injection(session, response):
    if session.is_New_IUAM_Challenge(response):
        return helheim('2044b982-151b-4fca-974d-ebad6fd10bec', session, response)
    else:
        return response


def loadSettings():
    with open(f'./data/config.json') as settings:
        settings = json.loads(settings.read())
        return settings


def loadProfile(profile):
    with open(f'./data/profiles/profile_{profile}.json') as profile:
        profile = json.loads(profile.read())
        return profile

def loadProxy(proxies,taskID, SITE):
    if proxies == "":
        return None
    elif proxies != "":
        with open(f'./data/{proxies}.txt', 'r') as proxyIn:
            try:
                proxyInput = proxyIn.read().splitlines()
            except:
                return None
    
        if len(proxyInput) == 0:
            return None

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
        logger.info(SITE,taskID,'Proxy Loaded')
        return proxies

def createId(length):
    return ''.join(random.choice(string.digits) for i in range(length))

def randomString(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


def loadCookie(SITE):
    with open('./data/cookies/datadome.json','r') as tokens:
        tokens = json.loads(tokens.read())
        if len(tokens[SITE]) > 0:
            t = tokens[SITE][0]
            tokens[SITE].pop(0)
            with open('./data/cookies/datadome.json','w') as output:
                json.dump(tokens,output)

            return t
            #note: MIGHT NEED TO MATCH UP PROXY WITH COOKIE.
            #cookie , hash , cid , icid , ua , parent_url , x-forwarded-for
        
        else:
            return {"cookie":"empty"}


def loadToken(SITE):
    try:
        with open('./data/captcha/tokens.json','r') as tokens:
            tokens = json.loads(tokens.read())
            if len(tokens[SITE]) > 0:
                t = tokens[SITE][0]
                tokens[SITE].pop(0)
                with open('./data/captcha/tokens.json','w') as output:
                    json.dump(tokens,output)
    
                return t["token"]
            
            else:
                return 'empty'
    except:
        return 'empty'


def sendNotification(site, text):
    try:
        hr = ToastNotifier()

        hr.show_toast(
            title='{} | Successful Checkout'.format(site.title()),
            msg=f'Checked out {text}',
            icon_path='E:\\venetia-io-cli\\favicon.ico',
            duration=5
        )
    except:
        pass



def encodeURIComponent(str):
    encoded = urllib.parse.quote(str, safe='~()*!.\'')
    return encoded

def decodeURIComponent(str):
    decoded = urllib.parse.unquote(str)
    return decoded

def birthday():
    day = random.randint(1,27)
    month = random.randint(1,9)
    year = random.randint(1970,2000)
    return {
        "day":day,
        "month":month,
        "year":year
    }


def storeCookies(checkoutURL,session):
    cookieList = []
    for c in session.cookies:
        try:
            url = c.domain.split('.')[1]
            cookieList.append(
                {"name": c.name, "value": c.value, "domain": c.domain, "path": c.path})
        except Exception as e:
            print(e)
            pass

    try:
        encoded = base64.b64encode(bytes(str(cookieList), 'utf-8'))
        encoded = str(encoded, 'utf8')
    
        encodedURL = base64.b64encode(
            bytes(str(checkoutURL), 'utf-8'))
        encodedURL = str(encodedURL, 'utf8')
    
        urlId = createId(15)
        r = requests.post('https://venetiacli.io/api/checkout/setCookies',headers={"apikey":"27acc458-f01a-48f8-88b8-06583fb39056"},data={"viewId":urlId,"cookies":encoded,"redirect":encodedURL})
        url = 'https://venetiacli.io/api/checkout/retrieve/?id={}'.format(urlId)
        return url
    except Exception as e:
        print(e)
        storeCookies(url,session)
    


def courir_datadome(proxy,taskID):
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

    if proxy == None:
        session.proxies = None
    else:
        session.proxies = proxy

    try:
        challenge = session.get(site)

    except (Exception, ConnectionError, ConnectionRefusedError, TimeoutError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
        logger.error('COURIR',taskID,'Failed to generate cookie. ERROR: {}'.format(e))
        courir_datadome(session.proxies,taskID)

    if 'DDUser' not in challenge.url:
        return session.cookies['datadome']

    if 'DDUser' in challenge.url:
        try:
            matches = re.search(r"dd={.+}", challenge.text, re.MULTILINE)
        except (Exception, ConnectionError, ConnectionRefusedError, TimeoutError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
            logger.error('COURIR',taskID,'Failed to generate cookie. ERROR: {}'.format(e))
            courir_datadome(session.proxies,taskID)
        if matches:
            try:
                ddConfig = json.loads(matches.group().split('dd=')[1].replace("'",'"'))
                ddCookie = session.cookies["datadome"]
            except (Exception, ConnectionError, ConnectionRefusedError, TimeoutError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
                logger.error('COURIR',taskID,'Failed to generate cookie. ERROR: {}'.format(e))
                courir_datadome(session.proxies,taskID)
            
            geoCaptchaScript = 'https://geo.captcha-delivery.com/captcha/?initialCid={}&hash={}&cid={}&t={}&referer={}'.format(encodeURIComponent(ddConfig["cid"]),ddConfig["hsh"],decodeURIComponent(ddCookie),encodeURIComponent(ddConfig["t"]),site)
            try:
                challenge = session.get(geoCaptchaScript)
            except (Exception, ConnectionError, ConnectionRefusedError, TimeoutError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
                logger.error('COURIR',taskID,'Failed to generate cookie. ERROR: {}'.format(e))
                courir_datadome(session.proxies,taskID)

            if challenge.status_code == 200:
                try:
                    xforwarded = challenge.text.split("'&x-forwarded-for=' + encodeURIComponent('")[1].split("'")[0]
                except (Exception, ConnectionError, ConnectionRefusedError, TimeoutError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
                    logger.error('COURIR',taskID,'Error scraping page. Most likely blocked.')
                    
                try:
                    geetestConfig = {
                        'api_server': challenge.text.split("api_server: '")[1].split("'")[0],
                        'gt': challenge.text.split("gt: '")[1].split("'")[0],
                        'challenge': challenge.text.split("challenge: '")[1].split("'")[0]
                    }
                except (Exception, ConnectionError, ConnectionRefusedError, TimeoutError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
                    logger.error('COURIR',taskID,'Error scraping page. Most likely blocked.')
                    courir_datadome(session.proxies,taskID)

                try:
                    results = captcha.geetest(geetestConfig["gt"],geetestConfig["challenge"],geetestConfig["api_server"],site,proxy,'COURIR',taskID)
                    geetestResponseChallenge = encodeURIComponent(results["request"]["geetest_challenge"])
                    geetestResponseValidate = encodeURIComponent(results["request"]["geetest_validate"])
                    geetestResponseSeccode = encodeURIComponent(results["request"]["geetest_seccode"])
                except (Exception, ConnectionError, ConnectionRefusedError, TimeoutError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
                    logger.error('COURIR',taskID,'Failed to generate cookie. ERROR: {}'.format(e))
                    courir_datadome(session.proxies,taskID)
    
        
                try:
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
                except (Exception, ConnectionError, ConnectionRefusedError, TimeoutError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
                    logger.error('COURIR',taskID,'Failed to generate cookie. ERROR: {}'.format(e))
                    courir_datadome(session.proxies,taskID)
                try:
                    getCookie = session.get(url)
                except (Exception, ConnectionError, ConnectionRefusedError, TimeoutError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
                    logger.error('COURIR',taskID,'Failed to generate cookie. ERROR: {}'.format(e))
                    courir_datadome(session.proxies,taskID)
                    
                if getCookie.status_code == 200:
                    cookie = getCookie.json()["cookie"].split('datadome=')[1].split(';')[0]
                    logger.secondary('COURIR',taskID,'Successfully generated cookie')
                    return cookie
                else:
                    print(getCookie)
                    logger.error('COURIR',taskID,'Failed to generate cookie. Retrying...')
                    courir_datadome(session.proxies,taskID)

            else:
                logger.error('COURIR',taskID,'Failed to generate cookie. Retrying...')
                courir_datadome(session.proxies,taskID)
                
                


def slamjam_datadome(proxy,taskID, pid, region):
    siteKey = '6LccSjEUAAAAANCPhaM2c-WiRxCZ5CzsjR_vd8uX'
    site = 'https://www.slamjam.com/on/demandware.store/Sites-slamjam-Site/en_{}/Product-Variation?pid={}'.format(region,pid)
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

    if proxy == None:
        session.proxies = None
    else:
        session.proxies = proxy
    

    try:
        challenge = session.get(site)
    except (Exception, ConnectionError, ConnectionRefusedError, TimeoutError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
        logger.error('SLAMJAM',taskID,'Failed to generate cookie. ERROR: {}'.format(e))
        slamjam_datadome(session.proxies,taskID, pid, region)

    if challenge:
        if 'DDUser' not in challenge.url:
            slamjam_datadome(session.proxies,taskID, pid, region)
    
        if 'DDUser' in challenge.url:
            try:
                matches = re.search(r"dd={.+}", challenge.text, re.MULTILINE)
            except Exception as e:
                logger.error('SLAMJAM',taskID,'Failed to generate cookie. ERROR: {}'.format(e))
                slamjam_datadome(session.proxies,taskID, pid, region)

            if matches:
                ddConfig = json.loads(matches.group().split('dd=')[1].replace("'",'"'))
                try:
                    ddCookie = session.cookies["datadome"]
                except:
                    logger.error('SLAMJAM',taskID,'Failed to generate cookie. Retrying...')
                    slamjam_datadome(session.proxies,taskID, pid, region)
                
                geoCaptchaScript = 'https://geo.captcha-delivery.com/captcha/?initialCid={}&hash={}&cid={}&t={}&referer={}'.format(encodeURIComponent(ddConfig["cid"]),ddConfig["hsh"],decodeURIComponent(ddCookie),encodeURIComponent(ddConfig["t"]),site)
                try:
                    challenge = session.get(geoCaptchaScript)
                except (Exception, ConnectionError, ConnectionRefusedError, TimeoutError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
                    logger.error('SLAMJAM',taskID,'Failed to generate cookie. ERROR: {}'.format(e))
                    slamjam_datadome(session.proxies,taskID, pid, region)
    
                if challenge.status_code == 200:
                    try:
                        xforwarded = challenge.text.split("'&x-forwarded-for=' + encodeURIComponent('")[1].split("'")[0]
                    except (Exception, ConnectionError) as e:
                        logger.error('SLAMJAM',taskID,'Error scraping page. Most likely blocked.')
                        slamjam_datadome(session.proxies,taskID, pid, region)
                    
    
                    try:
                        captchaResponse = captcha.v2(siteKey,challenge.url,session.proxies,'SLAMJAM',taskID)
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
                    except (Exception, ConnectionError, ConnectionRefusedError, TimeoutError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
                        logger.error('SLAMJAM',taskID,'Failed to generate cookie. ERROR: {}'.format(e))
                        slamjam_datadome(session.proxies,taskID, pid, region)

                    try:
                        getCookie = session.get(url)
                    except (Exception, ConnectionError, ConnectionRefusedError, TimeoutError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
                        logger.error('SLAMJAM',taskID,'Failed to generate cookie. ERROR: {}'.format(e))
                        slamjam_datadome(session.proxies,taskID, pid, region)
                    if getCookie.status_code == 200:
                        cookie = getCookie.json()["cookie"].split('datadome=')[1].split(';')[0]
                        logger.secondary('SLAMJAM',taskID,'Successfully generated cookie')
                        return cookie
    
                    else:
                        logger.error('SLAMJAM',taskID,'Failed to generate cookie. Retrying...')
                        slamjam_datadome(session.proxies,taskID, pid, region)
    
                else:
                    logger.error('SLAMJAM',taskID,'Failed to generate cookie. Retrying...')
                    slamjam_datadome(session.proxies,taskID, pid, region)
            else:
                logger.error('SLAMJAM',taskID,'Failed to generate cookie. Retrying...')
                slamjam_datadome(session.proxies,taskID, pid, region)
        
        else:
            logger.error('SLAMJAM',taskID,'Failed to get challenge. Retrying...')
            slamjam_datadome(session.proxies,taskID, pid, region)

                
def starcow_datadome(proxy,taskID):
    siteKey = '6LccSjEUAAAAANCPhaM2c-WiRxCZ5CzsjR_vd8uX'
    site = 'https://www.starcowparis.com'
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

    if proxy == None:
        session.proxies = None
    else:
        session.proxies = proxy

    try:
        challenge = session.get(site)

    except (Exception, ConnectionError, ConnectionRefusedError, TimeoutError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
        logger.error('STARCOW',taskID,'Failed to generate cookie. ERROR: {}'.format(e))
        starcow_datadome(session.proxies,taskID)

    if 'DDUser' not in challenge.url:
        return session.cookies['datadome']

    if 'DDUser' in challenge.url:
        try:
            matches = re.search(r"dd={.+}", challenge.text, re.MULTILINE)
        except (Exception, ConnectionError) as e:
            logger.error('STARCOW',taskID,'Failed to generate cookie. ERROR: {}'.format(e))
            starcow_datadome(session.proxies,taskID)
        if matches:
            ddConfig = json.loads(matches.group().split('dd=')[1].replace("'",'"'))
            ddCookie = session.cookies["datadome"]
            
            geoCaptchaScript = 'https://geo.captcha-delivery.com/captcha/?initialCid={}&hash={}&cid={}&t={}&referer={}'.format(encodeURIComponent(ddConfig["cid"]),ddConfig["hsh"],decodeURIComponent(ddCookie),encodeURIComponent(ddConfig["t"]),site)
            challenge = session.get(geoCaptchaScript)
            if challenge.status_code == 200:
                try:
                    xforwarded = challenge.text.split("'&x-forwarded-for=' + encodeURIComponent('")[1].split("'")[0]
                except (Exception, ConnectionError) as e:
                    logger.error('STARCOW',taskID,'Error scraping page. Most likely blocked.')
                    
                try:
                    geetestConfig = {
                        'api_server': challenge.text.split("api_server: '")[1].split("'")[0],
                        'gt': challenge.text.split("gt: '")[1].split("'")[0],
                        'challenge': challenge.text.split("challenge: '")[1].split("'")[0]
                    }
                except (Exception, ConnectionError) as e:
                    logger.error('STARCOW',taskID,'Error scraping page. Most likely blocked.')
                    starcow_datadome(session.proxies,taskID)

                try:
                    results = captcha.geetest(geetestConfig["gt"],geetestConfig["challenge"],geetestConfig["api_server"],site,proxy,'STARCOW',taskID)
                    geetestResponseChallenge = encodeURIComponent(results["request"]["geetest_challenge"])
                    geetestResponseValidate = encodeURIComponent(results["request"]["geetest_validate"])
                    geetestResponseSeccode = encodeURIComponent(results["request"]["geetest_seccode"])
                except (Exception, ConnectionError, ConnectionRefusedError, TimeoutError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
                    logger.error('STARCOW',taskID,'Failed to generate cookie. ERROR: {}'.format(e))
                    starcow_datadome(session.proxies,taskID)
    
                try:
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
                except (Exception, ConnectionError, ConnectionRefusedError, TimeoutError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
                    logger.error('STARCOW',taskID,'Failed to generate cookie. ERROR: {}'.format(e))
                    starcow_datadome(session.proxies,taskID)

                try:    
                    getCookie = session.get(url)
                except (Exception, ConnectionError, ConnectionRefusedError, TimeoutError, requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
                    logger.error('STARCOW',taskID,'Failed to generate cookie. ERROR: {}'.format(e))
                    starcow_datadome(session.proxies,taskID)

                if getCookie.status_code == 200:
                    cookie = getCookie.json()["cookie"].split('datadome=')[1].split(';')[0]
                    logger.secondary('STARCOW',taskID,'Successfully generated cookie')
                    return cookie
                else:
                    print(getCookie)
                    logger.error('STARCOW',taskID,'Failed to generate cookie. Retrying...')
                    starcow_datadome(session.proxies,taskID)

            else:
                logger.error('STARCOW',taskID,'Failed to generate cookie. Retrying...')
                starcow_datadome(session.proxies,taskID)
                