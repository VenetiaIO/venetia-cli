import string
import random
import requests
import re
import json
import urllib.parse
import time
import random
import threading
from utils.config import VERSION
import cloudscraper
import base64
from pynotifier import Notification
# from win10toast import ToastNotifier
try:
  import winsound
except:
  pass

from utils.logger import logger
from utils.captcha import captcha
from helheim import helheim

try:
  import win32console 
except:
  pass

def injection(session, response):
    if session.is_New_IUAM_Challenge(response) \
    or session.is_New_Captcha_Challenge(response):
        return helheim('2044b982-151b-4fca-974d-ebad6fd10bec', session, response)
    else:
        return response

def loadSettings():
    with open(f'./data/config.json') as settings:
        settings = json.loads(settings.read())
        return settings


def loadProfile(profile):
    profileFound = []
    with open(f'./data/profiles/profiles.json') as data:
        profiles = json.loads(data.read())
        for p in profiles["profiles"]:
            if p["profileName"] == profile:
                profileFound.append('1')
                return p
    
    if len(profileFound) == 0:
        return None

def loadProxy(proxies,taskID, SITE):
    if proxies == "":
        return None
    elif proxies != "":
        try:
            with open(f'./data/{proxies}.txt', 'r') as proxyIn:
                try:
                    proxyInput = proxyIn.read().splitlines()
                except:
                    return None
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
        # logger.info(SITE,taskID,'Proxy Loaded')
        return proxies

def createId(length):
    return ''.join(random.choice(string.digits) for i in range(length))

def randomString(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def getUser():
    key = loadSettings()["key"]
    headers = {"apikey":"27acc458-f01a-48f8-88b8-06583fb39056"}
    response = requests.post('https://venetiacli.io/api/get/user/key',headers=headers,data={"key":key})
    if response.status_code == 200:
        return response.json()
    else:
        return None


def updateConsoleTitle(carted,checkedOut, SITE):
    if carted == True:
        try:
          title = win32console.GetConsoleTitle()
          carted = title.split('Carted: ')[1].split(' |')[0]
          newCarted = int(carted) + 1
  
          checked = title.split('Checked Out: ')[1].split(' |')[0]
          win32console.SetConsoleTitle("[{}] VenetiaIO CLI - {} | Carted: {} | Checked Out: {}".format(VERSION,SITE.title(),newCarted,checked))
        except:
          pass
    if checkedOut == True:
        try:
          title = win32console.GetConsoleTitle()
          checked = title.split('Checked Out: ')[1].split(' |')[0]
          newChecked = int(checked) + 1
  
          carted = title.split('Carted: ')[1].split(' |')[0]
          win32console.SetConsoleTitle("[{}] VenetiaIO CLI - {} | Carted: {} | Checked Out: {}".format(VERSION,SITE.title(),carted,newChecked))
        except:
          pass

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
        noise = loadSettings()["checkoutNoise"]
    except:
        noise = ""
    if noise.upper() == "Y" or noise.upper() == "":
        try:
          winsound.PlaySound('sound.wav', winsound.SND_FILENAME)
        except:
          pass

    try:
        hr = ToastNotifier()

        hr.show_toast(
            title='{} | Successful Checkout'.format(site.title()),
            msg=f'Checked out {text}',
            icon_path='E:\\venetia-io-cli\\favicon.ico',
            duration=5
        )
    except:
      
        Notification(
          title='{} | Successful Checkout'.format(site.title()),
          description=f'Checked out {text}',
          icon_path='E:\\venetia-io-cli\\favicon.ico', # On Windows .ico is required, on Linux - .png
          duration=5,                              # Duration in seconds
          urgency=Notification.URGENCY_CRITICAL
        ).send()

def urlEncode(quote):
    return urllib.parse.quote(str(quote))

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
                if 'paypal' in c.domain:
                    # url = c.domain.split('.')[1]
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
                

def randomUA():
    return random.choice(userAgents)["ua"]

userAgents = [
  {
    "commonality": "Very common",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "44",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "57",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "57",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "55",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "55",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "52",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "61",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "43",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "57",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "57",
    "ua": "Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "52",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "57",
    "ua": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "57",
    "ua": "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "58",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "41",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.104 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "42",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "39",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "55",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "55",
    "ua": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "55",
    "ua": "Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "61",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "58",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; vivo 1603 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "55",
    "ua": "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "v1",
    "ua": "Mozilla/5.0 (Unknown; Linux) AppleWebKit/538.1 (KHTML, like Gecko) Chrome/v1.0.0 Safari/538.1"
  },
  {
    "commonality": "Very common",
    "version": "61",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "65",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "61",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "53",
    "ua": "Mozilla/5.0 (Linux; Android 6.0; vivo 1713 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.124 Mobile Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "56",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "58",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "56",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "55",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "56",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "41",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "53",
    "ua": "Mozilla/5.0 (Linux; Android 6.0; vivo 1610 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.124 Mobile Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "63",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; SM-G532G Build/MMB29T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.83 Mobile Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "55",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "48",
    "ua": "Mozilla/5.0 (Linux; Android 5.1.1; vivo X7 Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 baiduboxapp/8.6.5 (Baidu; P1 5.1.1)"
  },
  {
    "commonality": "Very common",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "43",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "41",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 5.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "26",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31"
  },
  {
    "commonality": "Common",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "58",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 5.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "56",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "57",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "65",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "42",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 5.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "57",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "43",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "52",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 5.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "57",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "56",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "52",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "58",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "22",
    "ua": "Mozilla/5.0 (Linux; U) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4"
  },
  {
    "commonality": "Common",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "52",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "55",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "61",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "61",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "44",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "55",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.0.12195 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "43",
    "ua": "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "58",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "43",
    "ua": "Mozilla/5.0 (Windows NT 5.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "24",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17"
  },
  {
    "commonality": "Common",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "58",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "56",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "62",
    "ua": "Mozilla/5.0 (Linux; Android 6.0; MYA-L22 Build/HUAWEIMYA-L22) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "52",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "53",
    "ua": "Mozilla/5.0 (Linux; Android 6.0; vivo 1606 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.124 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "60",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "52",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "61",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "52",
    "ua": "Mozilla/5.0 (Windows NT 5.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "52",
    "ua": "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "52",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "58",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "52",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "58",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; ASUS_T00J Build/KVT49L) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "58",
    "ua": "Mozilla/5.0 (Linux; Android 7.1; Mi A1 Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "60",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; SM-T800 Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.107 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; RKM MK902 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "52",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "58",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "61",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "58",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.34 Safari/534.24"
  },
  {
    "commonality": "Common",
    "version": "58",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "61",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "43",
    "ua": "Mozilla/5.0 (Linux; Android 5.1; A37f Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.93 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "63",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; CPH1607 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.111 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "1.0",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.36 Safari/525.19"
  },
  {
    "commonality": "Common",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; Android 4.4; Nexus 5 Build/LMY48B ) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "52",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "62",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; SM-G7102 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "16",
    "ua": "Mozilla/5.0 (Linux; U; Android-4.0.3; en-us; Galaxy Nexus Build/IML74K) AppleWebKit/535.7 (KHTML, like Gecko) CrMo/16.0.912.75 Mobile Safari/535.7"
  },
  {
    "commonality": "Common",
    "version": "56",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "53",
    "ua": "Mozilla/5.0 (Linux; Android 5.0.2; vivo Y51 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.124 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "52",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "49",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "16",
    "ua": "Mozilla/5.0 (Linux; U; Android-4.0.3; en-us; Xoom Build/IML77) AppleWebKit/535.7 (KHTML, like Gecko) CrMo/16.0.912.75 Safari/535.7"
  },
  {
    "commonality": "Common",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "46",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "60",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; Redmi 4A Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.116 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "42",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "61",
    "ua": "Mozilla/5.0 (Linux; Android 7.1; vivo 1716 Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "59",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; TRT-LX2 Build/HUAWEITRT-LX2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "25",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22"
  },
  {
    "commonality": "Common",
    "version": "43",
    "ua": "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.65 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "62",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 9901.77.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.97 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "55",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "59",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "63",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 10032.86.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.140 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "63",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "65",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "9",
    "ua": "Mozilla/5.0 (en-us) AppleWebKit/534.14 (KHTML, like Gecko; Google Wireless Transcoder) Chrome/9.0.597 Safari/534.14"
  },
  {
    "commonality": "Common",
    "version": "65",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "24",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17"
  },
  {
    "commonality": "Common",
    "version": "62",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "55",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "49",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "58",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "52",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "44",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "56",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "60",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "55",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "26",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31"
  },
  {
    "commonality": "Common",
    "version": "24",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17"
  },
  {
    "commonality": "Common",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
  },
  { "commonality": "Common", "version": "", "ua": "Chrome" },
  {
    "commonality": "Common",
    "version": "41",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "26",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31"
  },
  {
    "commonality": "Common",
    "version": "63",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; Redmi Note 4 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "23",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11"
  },
  {
    "commonality": "Common",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "63",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; SM-G610F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "58",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "57",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "26",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31"
  },
  {
    "commonality": "Common",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "65",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "56",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "63",
    "ua": "Mozilla/5.0 (Linux; Android 7.1.2; Redmi 4X Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "63",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; SM-J730GM Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "58",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "62",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; SM-J710F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "63",
    "ua": "Mozilla/5.0 (Linux; Android 7.1.2; Redmi Note 5A Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.111 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "55",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; BLL-L22 Build/HUAWEIBLL-L22) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "62",
    "ua": "Mozilla/5.0 (Linux; Android 6.0; CAM-L21 Build/HUAWEICAM-L21; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 5.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "63",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "52",
    "ua": "Mozilla/5.0 (Linux; Android 5.1; A1601 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "17",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
  },
  {
    "commonality": "Common",
    "version": "61",
    "ua": "Mozilla/5.0 (Linux; Android 7.1.1; CPH1723 Build/N6F26Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "62",
    "ua": "Mozilla/5.0 (Linux; Android 5.1.1; A37fw Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "61",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "49",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "44",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "41",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "65",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "62",
    "ua": "Mozilla/5.0 (Linux; Android 5.1; HUAWEI CUN-L22 Build/HUAWEICUN-L22; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "57",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "60",
    "ua": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "65",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "61",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "60",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 9592.96.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.114 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "58",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "62",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "54",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "52",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "64",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "65",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "56",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "57",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "34",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "52",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "49",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "13",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.112 Safari/535.1"
  },
  {
    "commonality": "Common",
    "version": "26",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31"
  },
  {
    "commonality": "Common",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "56",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "44",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "54",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "53",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "57",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "62",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "52",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 8350.68.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "44",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "40",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "55",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "26",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"
  },
  {
    "commonality": "Common",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "65",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "24",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17"
  },
  {
    "commonality": "Common",
    "version": "43",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36 http://notifyninja.com/monitoring"
  },
  {
    "commonality": "Common",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "61",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "63",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "43",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.45 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "25",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.152 Safari/537.22"
  },
  {
    "commonality": "Common",
    "version": "63",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "53",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; en-us; SAMSUNG SM-G900T Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.6 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "28",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; en-us; SAMSUNG SCH-I545 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "49",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "61",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "59",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "52",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "55",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "16",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.77 Safari/535.7"
  },
  {
    "commonality": "Common",
    "version": "63",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 10032.75.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "23",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
  },
  {
    "commonality": "Common",
    "version": "39.5",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.5.2171.95 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "39.5",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.5.2171.95 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "56",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 9000.91.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.110 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "58",
    "ua": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "63",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "56",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "48",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "36",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "25",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.97 Safari/537.22"
  },
  {
    "commonality": "Common",
    "version": "59",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "57",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "64",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "58",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "61",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "19",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5"
  },
  {
    "commonality": "Common",
    "version": "23",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11"
  },
  {
    "commonality": "Common",
    "version": "55",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "13",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.112 Safari/535.1"
  },
  {
    "commonality": "Common",
    "version": "61",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "45",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "37",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "27",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "37",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "25",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.99 Safari/537.22"
  },
  {
    "commonality": "Common",
    "version": "58",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "61",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 9765.85.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.123 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "57",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 9202.64.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.146 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "55",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "64",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 10176.76.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.190 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "61",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "57",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "54",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.0 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "40",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36 XaxisSemanticsClassifier/1.0 http://crystalsemantics.com"
  },
  {
    "commonality": "Common",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "55",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 8872.76.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.105 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; en-us; SAMSUNG SM-T230NU Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "20",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11"
  },
  {
    "commonality": "Common",
    "version": "47",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "26",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31"
  },
  {
    "commonality": "Common",
    "version": "47",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "61",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "51",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/51.0.2704.104 Mobile/13F69 Safari/601.1.46"
  },
  {
    "commonality": "Common",
    "version": "52",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "60",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "52",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "57",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "59",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "52",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
  },
  {
    "commonality": "Common",
    "version": "24",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "43",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "26",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "52",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "58",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "20",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39.5",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.5.2171.95 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "57",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "58",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "52",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; en-us; SAMSUNG-SM-G900A Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.6 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 8530.96.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.154 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "24",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17"
  },
  {
    "commonality": "Average",
    "version": "56",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "57",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 9460.60.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.91 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "23",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "57",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "57",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "61",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Chedot/8.0.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "57",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; LGMS210 Build/NRD90U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "44",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; 7040N Build/KVT49L) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "42",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "56",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "58",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "19",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "23",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; LG-F180L Build/KOT49I.F180L30b) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "38",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "58",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "31",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "43",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; MS5.V2 Build/MS5.V2) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "25",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "24",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17"
  },
  {
    "commonality": "Average",
    "version": "21",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 9460.73.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.134 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "43",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "55",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "40",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "36",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 9460.73.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.134 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "56",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; en-us; SAMSUNG SM-N900T Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "44",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; en-us; SAMSUNG SM-G386T Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.6 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "56",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "55",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "57",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2444.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "26",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "43",
    "ua": "Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 (KHTML, like Gecko)Chrome/43.0.2357.134 Safari/537.36http://notifyninja.com/monitoring"
  },
  {
    "commonality": "Average",
    "version": "32",
    "ua": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 8172.60.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 8172.62.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "25",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "25",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 7390.68.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.82 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 7262.57.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.98 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "40",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.28 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "61",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 9765.81.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.120 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "56",
    "ua": "Mozilla/5.0 (Linux; Android 4.1.2; Xperia Tipo Build/JZO54K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 9901.66.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.82 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 7647.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "26",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.108 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "26",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; U; Android 4.4; en-us; LGL34C/V100 Build/KRT16S.L34CV10c) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.2 Chrome/30.0.1599.103 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "34",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "18",
    "ua": "Mozilla/5.0 (Linux; Android 4.2.2; en-us; SAMSUNG SGH-M919 Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Version/1.0 Chrome/18.0.1025.308 Mobile Safari/535.19"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "58",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "31",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; LGMS323 Build/KOT49I.MS32310b) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.1599.103 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "56",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.79 Mobile/14D27 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "61",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "56",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; SM-J700F Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; en-us; SAMSUNG SM-G900P Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.6 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "41",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 9592.85.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.112 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "44",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "55",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 8530.81.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.103 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "34",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; Z981 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "58",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 9334.72.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.140 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "52",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.3; en-us; SAMSUNG SM-N900T Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "18",
    "ua": "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "44",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2683.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "58",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "40",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) CriOS/63.0.3239.73 Mobile/15C153 Safari/604.1"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "25",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.152 Safari/537.22"
  },
  {
    "commonality": "Average",
    "version": "34",
    "ua": "Mozilla/5.0 (Linux; Android 5.0.2; LG-V410/V41020c Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/34.0.1847.118 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "57",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Linux; Android 5.1.1; Coolpad 3622A Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.16 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "27",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko; Google Web Preview) Chrome/27.0.1453 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 8743.85.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 10.0 WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "58",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; LGMS210 Build/NRD90U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "57",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "27",
    "ua": "Mozilla/5.0 (en-US) AppleWebKit/537.36 (KHTML, like Gecko; Hound) Chrome/27.0.1453 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "52",
    "ua": "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "17",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.8 (KHTML, like Gecko) Beamrise/17.2.0.9 Chrome/17.0.939.0 Safari/535.8"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; rk31sdk Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "23",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11"
  },
  {
    "commonality": "Average",
    "version": "58",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "18",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.162 Safari/535.19"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "43",
    "ua": "'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.65 Mobile Safari/537.36'"
  },
  {
    "commonality": "Average",
    "version": "61",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) CriOS/61.0.3163.73 Mobile/14G60 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.108 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "57",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "61",
    "ua": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "21",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.90 Safari/537.1"
  },
  {
    "commonality": "Average",
    "version": "39",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95  Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "55",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "11",
    "ua": "Mozilla/5.0 (Linux; GoogleTV 3.2; NSZ-GS7/GX70 Build/MASTER) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.77 Safari/534.24"
  },
  {
    "commonality": "Average",
    "version": "58",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2988.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "24",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; SM-G955U Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; en-us; SAMSUNG-SM-G870A Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.6 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "58",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "42",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "23",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
  },
  {
    "commonality": "Average",
    "version": "24",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17"
  },
  {
    "commonality": "Average",
    "version": "43",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "55",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "58",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "36",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.4; Nexus 7 Build/KTU84P) AppleWebKit/537.36 (KHTML like Gecko) Chrome/36.0.1985.135 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "44",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "33",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "52",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "56",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "61",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "33",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.4; SM-G935S Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "58",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "61",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "41",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "25",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "19",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; PLAYipp PLAYport MAX A3188; installer/1.0; playipplauncher/2.1.1; system_provider/1.7.2; media_unit/2.0.69; networkmanager/2.0.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.0.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "52",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "44",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "19",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5"
  },
  {
    "commonality": "Average",
    "version": "55",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 8872.73.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "40",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "56",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.114 Safari/537.36 SRAF/3.0"
  },
  {
    "commonality": "Average",
    "version": "34",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.4; en-us; SAMSUNG SM-N910T Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/2.0 Chrome/34.0.1847.76 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "44",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 7520.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.110 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "55",
    "ua": "Mozilla/5.0 (Linux; Android 5.1.1; SM-J200G Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "23",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
  },
  {
    "commonality": "Average",
    "version": "61",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39",
    "ua": "Mozilla/5.0 (Linux;) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36 SRAF/3.5"
  },
  {
    "commonality": "Average",
    "version": "25",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.152 Safari/537.22"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "25",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "43",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/47.0.2526.70 Mobile/13C71 Safari/601.1.46"
  },
  {
    "commonality": "Average",
    "version": "40",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "24",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 10176.68.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.144 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "20",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; SM-G950U Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "40",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "56",
    "ua": "Mozilla/5.0 (Linux; Android 7.1.1; Z982 Build/NMF26V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "21",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39",
    "ua": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "41",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.104 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "38",
    "ua": "Mozilla/5.0 (Linux; Android 5.1.1; LGMS345 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/38.0.2125.102 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "61",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; Z981 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.91 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "24",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17"
  },
  {
    "commonality": "Average",
    "version": "22",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 7834.70.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "61",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "57",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.4; en-us; SAMSUNG SGH-M919 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Linux; Android 5.1.1; Coolpad 3622A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/46.0.2490.76 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "37",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "55",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/55.0.2883.79 Mobile/14C92 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "58",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "55",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.44 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; Android SDK built for x86 Build/KK) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 7978.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.103 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "25",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.97 Safari/537.22"
  },
  {
    "commonality": "Average",
    "version": "52",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39",
    "ua": "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "19",
    "ua": "Mozilla/5.0 (iPad;U;CPU OS 5_1_1 like Mac OS X; zh-cn)AppleWebKit/534.46.0(KHTML, like Gecko)CriOS/19.0.1084.60 Mobile/9B206 Safari/7534.48.3"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) CriOS/65.0.3325.152 Mobile/15D100 Safari/604.1"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Linux; Android 7.1.1; Z982 Build/NMF26V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "52",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "23",
    "ua": "Mozilla/5.0 (X11; FreeBSD; U; Viera; en-IE) AppleWebKit/537.11 (KHTML, like Gecko) Viera/3.10.14 Chrome/23.0.1271.97 Safari/537.11"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "40",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "58",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "43",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 6310.68.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.96 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; Redmi Note 4 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.85 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "31",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/31.0.1650.63 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "44",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; LGMP260 Build/NRD90U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; en-us; SAMSUNG SM-N900V Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) CriOS/64.0.3282.112 Mobile/15D60 Safari/604.1"
  },
  {
    "commonality": "Average",
    "version": "56",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "56",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "52",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "20",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) CriOS/59.0.3071.102 Mobile/14F89 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.34 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "20",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; en-us; SAMSUNG-SM-N900A Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "24",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "23",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.11 (KHTML like Gecko) Chrome/23.0.1271.95 Safari/537.11"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "41",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2220.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/51.0.2704.104 Mobile/13F69 Safari/601.1.46"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.91 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "57",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "57",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "43",
    "ua": "Mozilla/5.0 (Linux; Android 5.1.1; LGMS330 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.93 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "25",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.97 Safari/537.22"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "31",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML like Gecko) Chrome/31.0.1650.63 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 7390.61.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 7262.52.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.86 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "44",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 7077.134.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.156 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3043.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "27",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "44",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "57",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "57",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 9202.60.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.137 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "44",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.133 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.168 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/39.0.2171.95 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/30.0.1599.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "32",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "55",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.3; en-us; SAMSUNG SCH-I545 Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.4; Z970 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "61",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; LGMS210 Build/NRD90U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "37",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/37.0.2062.120 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "36",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML like Gecko) Chrome/36.0.1985.143 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "52",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "61",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; SM-G928V Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.98 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "23",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.11 (KHTML like Gecko) Chrome/23.0.1271.64 Safari/537.11"
  },
  {
    "commonality": "Average",
    "version": "55",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "37",
    "ua": "Mozilla/5.0 (Linux; Android 5.0; RCT6303W87DK Build/LRX21M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "36",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/36.0.1985.125 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "22",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4"
  },
  {
    "commonality": "Average",
    "version": "5",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.99 Safari/533.4"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "61",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; Z981 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "37",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "BrightSign/R3E6DP000834/6.2.94 (XD233) Mozilla/5.0 (Unknown; Linux arm) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/5.6.0 Chrome/45.0.2454.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 7834.66.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.111 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "55",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "37",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML like Gecko) Chrome/37.0.2062.120 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "23",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML like Gecko) Chrome/23.0.1271.95 Safari/537.11"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.3; en-us; SAMSUNG SGH-M919 Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "23",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "19",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "18",
    "ua": "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"
  },
  {
    "commonality": "Average",
    "version": "26",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML like Gecko) Chrome/26.0.1410.64 Safari/537.31"
  },
  {
    "commonality": "Average",
    "version": "56",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 9000.82.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "24",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2625.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "27",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko; Google Page Speed Insights) Chrome/27.0.1453 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "57",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; en-us; SAMSUNG SPH-L720T Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "18",
    "ua": "Mozilla/5.0 (Linux; Android 4.1.2; SGH-T599N Build/JZO54K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "37",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/37.0.2062.103 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "55",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "26",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; LGMS323 Build/KOT49I.MS32310c) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.1599.103 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "31",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML like Gecko) Chrome/31.0.1650.63 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "36",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/36.0.1985.143 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "55",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.91 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "58",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "55",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; LGMS210 Build/NRD90U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "18",
    "ua": "Mozilla/5.0 (Linux; Android 4.0.3; HTC One X Build/IML74K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; en-gb; SAMSUNG GT-I9505 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "27",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/27.0.1453.110 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "36",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/36.0.1985.143 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; GT-I9505 Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "36",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "61",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "19",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5"
  },
  {
    "commonality": "Average",
    "version": "44",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "20",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11"
  },
  {
    "commonality": "Average",
    "version": "61",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 7520.63.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "35",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/35.0.1916.153 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; en-us; SAMSUNG-SGH-I337 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "24",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17"
  },
  {
    "commonality": "Average",
    "version": "35",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) CriOS/60.0.3112.89 Mobile/14G60 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "26",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "42",
    "ua": "Mozilla/5.0 (Linux; Android 4.0.4; BNTV400 Build/IMM76L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.111 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/63.0.3239.73 Mobile/13G36 Safari/601.1.46"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "56",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "37",
    "ua": "Mozilla/5.0 (Linux; Android 5.0.2; NX512J Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile Safari/537.36 Browser"
  },
  {
    "commonality": "Average",
    "version": "56",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; SM-J510FN Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3204.0 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 7647.73.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.92 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (X11; CrOS armv7l 9592.96.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.114 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "38",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.102 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "21",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.60 Safari/537.1"
  },
  {
    "commonality": "Average",
    "version": "40",
    "ua": "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 4 Build/LMY48T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.89 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2480.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) CriOS/63.0.3239.73 Mobile/15C202 Safari/604.1"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "57",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "26",
    "ua": "Mozilla/5.0 (Linux; Android 4.0.4; BNTV400 Build/IMM76L) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.58 Safari/537.31"
  },
  {
    "commonality": "Average",
    "version": "55",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "56",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "42",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "44",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "52",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "26",
    "ua": "Mozilla/5.0 (Linux; Android 4.0.4; BNTV600 Build/IMM76L) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.58 Safari/537.31"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "44",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "44",
    "ua": "Mozilla/5.0 (iPod; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/44.0.2403.67 Mobile/12H143 Safari/600.1.4"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 10323.62.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.184 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 7834.60.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.95 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 8172.56.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "33",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/33.0.1750.154 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; LGMS210 Build/NRD90U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; en-gb; SAMSUNG GT-I9195 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "44",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 10176.72.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "61",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "42",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; SAMSUNG-SM-N900A Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "44",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Linux; Android 5.1.1; A571VL Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/46.0.2490.76 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "61",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.70 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "58",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.113 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "26",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.1.2; GT-S7262 Build/JZO54K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "37",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Linux; Android 5.1.1; LGMS330 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.89 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; LG-D415 Build/KOT49I.D41510c) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.1599.103 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "44",
    "ua": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "52",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "23",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11"
  },
  {
    "commonality": "Average",
    "version": "40",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; LG-V410 Build/KOT49I.V41010d) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.103 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Linux; Android 7.1.1; SM-N950U Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "18",
    "ua": "Mozilla/5.0 (Linux; Android 4.2.2; en-us; SAMSUNG SPH-L720 Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Version/1.0 Chrome/18.0.1025.308 Mobile Safari/535.19"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/53.0.2785.109 Mobile/14A456 Safari/601.1.46"
  },
  {
    "commonality": "Average",
    "version": "25.1",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.1.0.0 Safari/537.22"
  },
  {
    "commonality": "Average",
    "version": "26",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31"
  },
  {
    "commonality": "Average",
    "version": "34",
    "ua": "Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; LGL16C/V100 Build/KOT49I.L16CV11a) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/34.0.1847.118 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "41",
    "ua": "Mozilla/5.0 (en-US) AppleWebKit/537.36 (KHTML, like Gecko; Hound) Chrome/41.0.2272.118 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; en-ca; SGH-I337M Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "24",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17"
  },
  {
    "commonality": "Average",
    "version": "18",
    "ua": "Mozilla/5.0 (Linux; Android 4.1; Galaxy Nexus Build/JRN84D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; SM-G900F Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "55",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; SM-G550T1 Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "55",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/28.0.1469.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "43",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"
  },
  {
    "commonality": "Average",
    "version": "26",
    "ua": "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "18",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.162 Safari/535.19"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "38",
    "ua": "Mozilla/5.0 (Linux; Android 6.0; LGLS770 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/38.0.2125.102 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "27",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; LG-V410/V41010d Build/KOT49I.V41010d) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.1599.103 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "35",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; SM-J327P Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "23",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; en-us; SAMSUNG SM-P600 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "44",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "52",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; SM-J210F Build/MMB29Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "57",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.89 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.108 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "23",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.21 Safari/537.36 MMS/1.0.2531.0"
  },
  {
    "commonality": "Average",
    "version": "38",
    "ua": "Mozilla/5.0 (Linux; Android 5.1.1; LGL62VL Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/38.0.2125.102 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "55",
    "ua": "Mozilla/5.0 (Linux; Android 5.1.1) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Focus/1.1.2 Chrome/55.0.2883.91 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (Linux; Android 5.1.1; Coolpad 3623A Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "12",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_7) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.91 Safari/534.30"
  },
  {
    "commonality": "Average",
    "version": "34",
    "ua": "Mozilla/5.0 (Linux; Android 5.0.2; LG-D415 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/34.0.1847.118 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "58",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; LGMP260 Build/NRD90U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "=Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 9592.94.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.114 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; ASUS_T00I Build/KVT49L) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Linux; Android 5.1.1; SM-G360T1 Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.89 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; LGMS210 Build/NRD90U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.137 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "55",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.59 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Linux; Android 5.1.1; VS425PP Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.89 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "18",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19"
  },
  {
    "commonality": "Average",
    "version": "16",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; XDS-1078 Build/HAWK) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; LG-D850/D85010f Build/KVT49L.D85010f) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.1599.103 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "43",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "18",
    "ua": "Mozilla/5.0 (Linux; Android 4.2.2; en-us; SAMSUNG-SGH-I337 Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Version/1.0 Chrome/18.0.1025.308 Mobile Safari/535.19"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; Z981 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "17",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
  },
  {
    "commonality": "Average",
    "version": "52",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "34",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.132 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; HUAWEI NXT-AL10 Build/HUAWEINXT-AL10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.107 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "25",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.4; en-us; SAMSUNG SM-N900P Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "57",
    "ua": "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "'mozilla/5.0 (Linux; Android 6.0.1; Nexus 5x build/mtc19t applewebkit/537.36 (KHTML, like Gecko) Chrome/51.0.2702.81 Mobile Safari/537.36'"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; SM-J327T1 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) CriOS/62.0.3202.70 Mobile/15A432 Safari/604.1"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "20",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11"
  },
  {
    "commonality": "Average",
    "version": "34",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "21",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "40",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.4; N817 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.109 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; LG-M153 Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.124 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; en-us; SAMSUNG SM-T520 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; en-us; SAMSUNG SM-G386T1 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.6 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_2_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) CriOS/63.0.3239.73 Mobile/15C153 Safari/604.1"
  },
  {
    "commonality": "Average",
    "version": "23",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 5.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "25.2",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.2.0.0 Safari/537.22"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (X11; CrOS armv7l 7262.57.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.98 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "43",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "34",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; LG-M153 Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; Hol-U19 Build/HUAWEIHol-U19) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; C6730 Build/KVT49L) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "26.2",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.2.2.0 Safari/537.31"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; BLU STUDIO 5.0 C Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "24",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.2.2; QMV7A Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.94 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; HUAWEI VNS-L21 Build/HUAWEIVNS-L21; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/130.0.0.45.70;]"
  },
  {
    "commonality": "Average",
    "version": "24",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "35",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (X11; CrOS armv7l 9901.77.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.97 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "61",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) CriOS/61.0.3163.73 Mobile/15A372 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "56",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; en-us; SAMSUNG SPH-L720 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 9592.71.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.80 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; LGMS323 Build/KOT49I.MS32310b) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.103 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "58",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "55",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.21 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "36",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "11",
    "ua": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.77 Large Screen Safari/534.24 GoogleTV/092754"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) CriOS/64.0.3282.112 Mobile/15D100 Safari/604.1"
  },
  {
    "commonality": "Average",
    "version": "58",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "55",
    "ua": "Mozilla/5.0 (X11; CrOS armv7l 8872.76.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.105 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2683.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "18",
    "ua": "Mozilla/5.0 (Linux; Android 4.2.1; Nexus 7 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19"
  },
  {
    "commonality": "Average",
    "version": "35",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) MxNitro/1.0.1.3000 Chrome/35.0.1849.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.4; Z970 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.105 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.4; en-us; SAMSUNG-SM-N900A Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "18",
    "ua": "Mozilla/5.0 (Linux; Android 4.2.2; en-us; SAMSUNG SGH-T399 Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Version/1.0 Chrome/18.0.1025.308 Mobile Safari/535.19"
  },
  {
    "commonality": "Average",
    "version": "57",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.3; en-us; SM-S975L Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "33",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/33.0.0.0 Safari/534.24"
  },
  {
    "commonality": "Average",
    "version": "61",
    "ua": "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3053.4 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "27",
    "ua": "Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; F3211 Build/36.1.A.0.182) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.116 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "56",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_2_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.79 Mobile/14D27 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (X11; CrOS armv7l 8530.96.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.154 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "'Mozilla/5.0 (Linux; Android 7.1.2; Moto G Build/N2G47O) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3095.0 Mobile Safari/537.36'"
  },
  {
    "commonality": "Average",
    "version": "58",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "26",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31"
  },
  {
    "commonality": "Average",
    "version": "23",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.101 Safari/537.11"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.26 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; en-gb; SAMSUNG SM-T230 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "57",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/57.0.2987.100 Mobile/14D27 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; 7040N Build/KVT49L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "56",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/54.0.2840.91 Mobile/14B100 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "18",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.45 Safari/535.19"
  },
  {
    "commonality": "Average",
    "version": "44",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "33",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39",
    "ua": "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "43",
    "ua": "Windows NT 6.1; WOW64) Chrome/43.0.2357.65 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; SM-G900F Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.93 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.3; en-us; SAMSUNG SM-N900V Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "43",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "55",
    "ua": "Mozilla/5.0 (Linux; Android 5.1.1) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Focus/2.0.1 Chrome/55.0.2883.91 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.82 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "21",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.79 Safari/537.1"
  },
  {
    "commonality": "Average",
    "version": "19",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "18",
    "ua": "Mozilla/5.0 (Linux; Android 4.0.4; LG-MS770 Build/IMM76I) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
  },
  {
    "commonality": "Average",
    "version": "44",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "61",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.4; en-us; SAMSUNG-SM-G900A Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.6 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; SM-G935F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "56",
    "ua": "Mozilla/5.0 (Linux; Android 7.1.1; Moto E (4) Build/NCQ26.69-46) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "43",
    "ua": "Mozilla/5.0 (Linux; Android 5.1.1; 5017B Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.93 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/28.0.1469.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.34 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; en-us; SAMSUNG SM-T330NU Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "29",
    "ua": "Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) CriOS/29.0.1547.11 Mobile/9B206 Safari/7534.48.3"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "56",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "36",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "31",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "58",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.3; en-us; SAMSUNG SM-S765C Build/JLS36C) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "21",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.75 Safari/537.1"
  },
  {
    "commonality": "Average",
    "version": "61",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; SM-G955U Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.1.2; LGMS500 Build/JZO54K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.94 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; LGLS676 Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.21 Safari/537.36 MMS/1.0.2459.0"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Linux; Android 5.1.1; 5065N Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.95 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "23",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11"
  },
  {
    "commonality": "Average",
    "version": "24",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Linux; Android 5.1; C6740N Build/LMY47O; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/46.0.2490.76 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "60",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "41",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "19",
    "ua": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3"
  },
  {
    "commonality": "Average",
    "version": "43",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "11",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2480.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "20",
    "ua": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (X11; CrOS armv7l 7390.68.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.82 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "38",
    "ua": "Mozilla/5.0 (Linux; Android 6.0; LG-H815 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/38.0.2125.102 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "39.5",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.5.2171.95 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; Redmi 4 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.85 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "56",
    "ua": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; Redmi 4A Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.85 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "12",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30"
  },
  {
    "commonality": "Average",
    "version": "38",
    "ua": "Mozilla/5.0 (Linux; Android 5.1.1; LGMS631 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/38.0.2125.102 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6 Build/MMB29X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.89 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "19",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 5_1_1 like Mac OS X; en-us) AppleWebKit/534.46.0 (KHTML, like Gecko) CriOS/19.0.1084.60 Mobile/9B206 Safari/7534.48.3"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "65",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "57",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/ Safari/530.5"
  },
  {
    "commonality": "Average",
    "version": "18.6",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/18.6.872.0 Safari/535.2 UNTRUSTED/1.0 3gpp-gba UNTRUSTED/1.0"
  },
  {
    "commonality": "Average",
    "version": "38",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; vivo 1606 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.124 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "23",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.101 Safari/537.11"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "4",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/531.3 (KHTML, like Gecko) Chrome/4.0.249.89 Safari/531.3"
  },
  {
    "commonality": "Average",
    "version": "29",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "28",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; en-us; SAMSUNG SM-T530NU Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "31",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; LGMS323 Build/KOT49I.MS32310b) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "34",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Linux; Android 7.1.1; Moto E (4) Build/NCQ26.69-46) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "42",
    "ua": "Mozilla/5.0 (Linux; Android 5.1.1; SM-G360T1 Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.111 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "31",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; SM-G950U Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.137 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; LGMP260 Build/NRD90U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; LG-D850/D85010d Build/KVT49L.D85010d) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.1599.103 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (X11; CrOS armv7l 10032.75.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "30",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.2; XT1031 Build/KXB20.9-1.10-1.18-1.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.92 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "38",
    "ua": "Mozilla/5.0 (Linux; Android 5.0.1; LGL33L/V100 Build/LRX21Y) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/38.0.2125.102 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (X11; CrOS armv7l 8172.62.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "31",
    "ua": "Mozilla/5.0 (X11; CrOS x86_64 4731.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.67 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "24",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17"
  },
  {
    "commonality": "Average",
    "version": "24",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17"
  },
  {
    "commonality": "Average",
    "version": "43",
    "ua": "Mozilla/5.0 (Linux; Android 5.0; Lenovo A1000 Build/S100) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.93 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "48",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/48.0.2564.104 Mobile/13D15 Safari/601.1.46"
  },
  {
    "commonality": "Average",
    "version": "44",
    "ua": "Mozilla/5.0 (Linux; Android 6.0; Android SDK built for x86 Build/MASTER; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/44.0.2403.119 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "61",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; SM-G950U Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "61",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) CriOS/61.0.3163.73 Mobile/14G60 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "45",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; ZTE-Z832 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/45.0.2454.95 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "52",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "55",
    "ua": "Mozilla/5.0 (Linux; Android 6.0; LG-D855 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "59",
    "ua": "Mozilla/5.0 (Linux; Android 4.4.4; E2124 Build/24.0.B.5.14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "56",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "49",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "37",
    "ua": "Mozilla/5.0 (Linux; Android 5.0; Micromax AQ5001 Build/LRX21M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (X11; CrOS armv7l 10032.86.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.140 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "62",
    "ua": "Mozilla/5.0 (Linux; Android 7.0; SM-G950U Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "53",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "42",
    "ua": "Mozilla/5.0 (Linux; Android 5.1.1; Z828 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.111 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "50",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "25",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/47.0.2526.107 Mobile/12F69 Safari/600.1.4"
  },
  {
    "commonality": "Average",
    "version": "64",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_2_5 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) CriOS/64.0.3282.112 Mobile/15D60 Safari/604.1"
  },
  {
    "commonality": "Average",
    "version": "63",
    "ua": "Mozilla/5.0 (Linux; Android 7.1.1; SM-T350 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "61",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "43",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "56",
    "ua": "Mozilla/5.0 (Linux; Android 6.0.1; SM-G610F Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "54",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "46",
    "ua": "Mozilla/5.0 (Linux; Android 5.1.1; 5065N Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/46.0.2490.76 Mobile Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "51",
    "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "47",
    "ua": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"
  },
  {
    "commonality": "Very common",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7"
  },
  {
    "commonality": "Very common",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1"
  },
  {
    "commonality": "Very common",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
  },
  {
    "commonality": "Very common",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/10.0 Mobile/14D27 Safari/602.1"
  },
  {
    "commonality": "Very common",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8"
  },
  {
    "commonality": "Very common",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
  },
  {
    "commonality": "Very common",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G36 Safari/601.1"
  },
  {
    "commonality": "Very common",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/10.0 Mobile/14D27 Safari/602.1"
  },
  {
    "commonality": "Very common",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4"
  },
  {
    "commonality": "Very common",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/601.4.4 (KHTML, like Gecko) Version/9.0.3 Safari/601.4.4"
  },
  {
    "commonality": "Very common",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30"
  },
  {
    "commonality": "Very common",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8"
  },
  {
    "commonality": "Very common",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E188a Safari/601.1"
  },
  {
    "commonality": "Very common",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/601.5.17 (KHTML, like Gecko) Version/9.1 Safari/601.5.17"
  },
  {
    "commonality": "Very common",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8"
  },
  {
    "commonality": "Very common",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17"
  },
  {
    "commonality": "Very common",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6"
  },
  {
    "commonality": "Very common",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 Mobile/14G60 Safari/602.1"
  },
  {
    "commonality": "Very common",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14"
  },
  {
    "commonality": "Very common",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4"
  },
  {
    "commonality": "Very common",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1"
  },
  {
    "commonality": "Very common",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38"
  },
  {
    "commonality": "Very common",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7"
  },
  {
    "commonality": "Very common",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7"
  },
  {
    "commonality": "Very common",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 Mobile/14C92 Safari/602.1"
  },
  {
    "commonality": "Very common",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50"
  },
  {
    "commonality": "Very common",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9"
  },
  {
    "commonality": "Very common",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E238 Safari/601.1"
  },
  {
    "commonality": "Very common",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13D15 Safari/601.1"
  },
  {
    "commonality": "Very common",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.12"
  },
  {
    "commonality": "Very common",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5"
  },
  {
    "commonality": "Very common",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.4.4 (KHTML, like Gecko) Version/9.0.3 Safari/601.4.4"
  },
  {
    "commonality": "Very common",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 Mobile/14B100 Safari/602.1"
  },
  {
    "commonality": "Very common",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.5.17 (KHTML, like Gecko) Version/9.1 Safari/601.5.17"
  },
  {
    "commonality": "Very common",
    "version": "7",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"
  },
  {
    "commonality": "Very common",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.59.10 (KHTML, like Gecko) Version/5.1.9 Safari/534.59.10"
  },
  {
    "commonality": "Very common",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/9.1.3 Safari/537.86.7"
  },
  {
    "commonality": "Very common",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/9.1.3 Safari/601.7.8"
  },
  {
    "commonality": "Very common",
    "version": "6.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/6.1.6 Safari/537.78.2"
  },
  {
    "commonality": "Very common",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A456 Safari/602.1"
  },
  {
    "commonality": "Very common",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50"
  },
  {
    "commonality": "Very common",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56"
  },
  {
    "commonality": "Very common",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/534.50.2 (KHTML, like Gecko) Version/5.0.6 Safari/533.22.3"
  },
  {
    "commonality": "Common",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 Mobile/14F89 Safari/602.1"
  },
  {
    "commonality": "Common",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 Mobile/15C153 Safari/604.1"
  },
  {
    "commonality": "Common",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7"
  },
  {
    "commonality": "Common",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13D15 Safari/601.1"
  },
  {
    "commonality": "Common",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G36 Safari/601.1"
  },
  {
    "commonality": "Common",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5"
  },
  {
    "commonality": "Common",
    "version": "6.2",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/6.2.8 Safari/537.85.17"
  },
  {
    "commonality": "Common",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13C75 Safari/601.1"
  },
  {
    "commonality": "Common",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9"
  },
  {
    "commonality": "Common",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14"
  },
  {
    "commonality": "Common",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 Mobile/14G60 Safari/602.1"
  },
  {
    "commonality": "Common",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G34 Safari/601.1"
  },
  {
    "commonality": "Common",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8"
  },
  {
    "commonality": "Common",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.2.5 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.5"
  },
  {
    "commonality": "Common",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17"
  },
  {
    "commonality": "Common",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_3_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E238 Safari/601.1"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0 Mobile/15D100 Safari/604.1"
  },
  {
    "commonality": "Common",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.21 (KHTML, like Gecko) Mwendo/1.1.5 Safari/537.21"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7"
  },
  {
    "commonality": "Common",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_2 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B202 Safari/604.1"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A432 Safari/604.1"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 Mobile/15C202 Safari/604.1"
  },
  {
    "commonality": "Common",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3"
  },
  {
    "commonality": "Common",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_4 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G35 Safari/601.1"
  },
  {
    "commonality": "Common",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"
  },
  {
    "commonality": "Common",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12"
  },
  {
    "commonality": "Common",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8"
  },
  {
    "commonality": "Common",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30"
  },
  {
    "commonality": "Common",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
  },
  {
    "commonality": "Common",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/603.2.5 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.5"
  },
  {
    "commonality": "Common",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.12"
  },
  {
    "commonality": "Common",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56"
  },
  {
    "commonality": "Common",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30"
  },
  {
    "commonality": "Common",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13C75 Safari/601.1"
  },
  {
    "commonality": "Common",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8"
  },
  {
    "commonality": "Common",
    "version": "7",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53"
  },
  {
    "commonality": "Common",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.12"
  },
  {
    "commonality": "Common",
    "version": "8",
    "ua": "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4"
  },
  {
    "commonality": "Common",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_0_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A456 Safari/602.1"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0 Mobile/15D60 Safari/604.1"
  },
  {
    "commonality": "Common",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 Mobile/14C92 Safari/602.1"
  },
  {
    "commonality": "Common",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4"
  },
  {
    "commonality": "Common",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 Mobile/14B100 Safari/602.1"
  },
  {
    "commonality": "Common",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G34 Safari/601.1"
  },
  {
    "commonality": "Common",
    "version": "6",
    "ua": "Mozilla/5.0 (iPad; CPU OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B329 Safari/8536.25"
  },
  {
    "commonality": "Common",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_1 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A402 Safari/604.1"
  },
  {
    "commonality": "Common",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"
  },
  {
    "commonality": "Common",
    "version": "8",
    "ua": "Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F69 Safari/600.1.4"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6"
  },
  {
    "commonality": "Common",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 Mobile/14F89 Safari/602.1"
  },
  {
    "commonality": "Common",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A452 Safari/601.1"
  },
  {
    "commonality": "Common",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38"
  },
  {
    "commonality": "Common",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_2 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A421 Safari/604.1"
  },
  {
    "commonality": "Common",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7"
  },
  {
    "commonality": "Common",
    "version": "11.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15"
  },
  {
    "commonality": "Common",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/9.1.3 Safari/601.7.8"
  },
  {
    "commonality": "Common",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_3_4 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G35 Safari/601.1"
  },
  {
    "commonality": "Common",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25"
  },
  {
    "commonality": "Common",
    "version": "8",
    "ua": "Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4"
  },
  {
    "commonality": "Common",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2"
  },
  {
    "commonality": "Common",
    "version": "7",
    "ua": "Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53"
  },
  {
    "commonality": "Common",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A452 Safari/601.1"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B150 Safari/604.1"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5"
  },
  {
    "commonality": "Common",
    "version": "7.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/7.1.8 Safari/537.85.17"
  },
  {
    "commonality": "Common",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/537.86.7"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 Mobile/15C153 Safari/604.1"
  },
  {
    "commonality": "Common",
    "version": "",
    "ua": "Mozilla/5.0 (Smartsign Player) AppleWebKit/534.7 (KHTML, like Gecko) Safari/534.7"
  },
  {
    "commonality": "Common",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"
  },
  {
    "commonality": "Common",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPad; CPU OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A405 Safari/7534.48.3"
  },
  {
    "commonality": "Common",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
  },
  {
    "commonality": "Common",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17"
  },
  {
    "commonality": "Common",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.4.4 (KHTML, like Gecko) Version/9.0.3 Safari/537.86.4"
  },
  {
    "commonality": "Common",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E233 Safari/601.1"
  },
  {
    "commonality": "Common",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.5.17 (KHTML, like Gecko) Version/9.1 Safari/537.86.5"
  },
  {
    "commonality": "Common",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/8.0.2 Safari/600.2.5 (Applebot/0.1; +http://www.apple.com/go/applebot)"
  },
  {
    "commonality": "Common",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/8.0.6 Safari/600.6.3"
  },
  {
    "commonality": "Common",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B93 Safari/604.1"
  },
  {
    "commonality": "Common",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/537.16 (KHTML, like Gecko) Version/8.0 Safari/537.16"
  },
  {
    "commonality": "Common",
    "version": "7",
    "ua": "Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53"
  },
  {
    "commonality": "Common",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/537.86.6"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A432 Safari/604.1"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0 Mobile/15D100 Safari/604.1"
  },
  {
    "commonality": "Common",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/537.86.3"
  },
  {
    "commonality": "Common",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/537.86.2"
  },
  {
    "commonality": "Common",
    "version": "7",
    "ua": "Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 Mobile/15C114 Safari/604.1"
  },
  {
    "commonality": "Common",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.18"
  },
  {
    "commonality": "Common",
    "version": "4",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B367 Safari/531.21.10"
  },
  {
    "commonality": "Common",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.28.10 (KHTML, like Gecko) Version/6.0.3 Safari/536.28.10"
  },
  {
    "commonality": "Common",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B329 Safari/8536.25"
  },
  {
    "commonality": "Common",
    "version": "8",
    "ua": "Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4"
  },
  {
    "commonality": "Common",
    "version": "7",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2"
  },
  {
    "commonality": "Common",
    "version": "4",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_2_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 Mobile/15C202 Safari/604.1"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0 Mobile/15D60 Safari/604.1"
  },
  {
    "commonality": "Common",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7"
  },
  {
    "commonality": "Common",
    "version": "6",
    "ua": "Mozilla/5.0 (iPad; CPU OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A523 Safari/8536.25"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_1_2 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B202 Safari/604.1"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.0 Mobile/15E148 Safari/604.1"
  },
  {
    "commonality": "Common",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2"
  },
  {
    "commonality": "Common",
    "version": "4.1",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; en) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/4.1.3 Safari/533.19.4"
  },
  {
    "commonality": "Common",
    "version": "7",
    "ua": "Mozilla/5.0 (iPad; CPU OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53"
  },
  {
    "commonality": "Common",
    "version": "6",
    "ua": "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"
  },
  {
    "commonality": "Common",
    "version": "8",
    "ua": "Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4"
  },
  {
    "commonality": "Common",
    "version": "8",
    "ua": "Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B440 Safari/600.1.4"
  },
  {
    "commonality": "Common",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_5 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5"
  },
  {
    "commonality": "Common",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4 (Applebot/0.1; +http://www.apple.com/go/applebot)"
  },
  {
    "commonality": "Common",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
  },
  {
    "commonality": "Common",
    "version": "7",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_2 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A4449d Safari/9537.53"
  },
  {
    "commonality": "Common",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A344 Safari/601.1"
  },
  {
    "commonality": "Common",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B440 Safari/600.1.4"
  },
  {
    "commonality": "Common",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2"
  },
  {
    "commonality": "Common",
    "version": "7",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53"
  },
  {
    "commonality": "Common",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E234 Safari/601.1"
  },
  {
    "commonality": "Common",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16"
  },
  {
    "commonality": "Common",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/8.0.2 Safari/600.2.5"
  },
  {
    "commonality": "Common",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4"
  },
  {
    "commonality": "Common",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A404 Safari/601.1"
  },
  {
    "commonality": "Common",
    "version": "11.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15"
  },
  {
    "commonality": "Common",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3"
  },
  {
    "commonality": "Average",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4"
  },
  {
    "commonality": "Average",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A344 Safari/601.1"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/537.86.1"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E233 Safari/601.1"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.29.13 (KHTML, like Gecko) Version/6.0.4 Safari/536.29.13"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_0_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A404 Safari/601.1"
  },
  {
    "commonality": "Average",
    "version": "8",
    "ua": "Mozilla/5.0 (iPad; CPU OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12D508 Safari/600.1.4"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9"
  },
  {
    "commonality": "Average",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12D508 Safari/600.1.4"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X; en-us) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B176 Safari/7534.48.3"
  },
  {
    "commonality": "Average",
    "version": "4",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7"
  },
  {
    "commonality": "Average",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_7; en-us) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Safari/530.17"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.58.2 (KHTML, like Gecko) Version/5.1.8 Safari/534.58.2"
  },
  {
    "commonality": "Average",
    "version": "4",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (iPad; CPU OS 6_1_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B146 Safari/8536.25"
  },
  {
    "commonality": "Average",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_0_1 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A402 Safari/604.1"
  },
  {
    "commonality": "Average",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_0_2 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A421 Safari/604.1"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko ) Version/5.1 Mobile/9B176 Safari/7534.48.3"
  },
  {
    "commonality": "Average",
    "version": "4.1",
    "ua": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; en) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/4.1.3 Safari/533.19.4"
  },
  {
    "commonality": "Average",
    "version": "7",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53"
  },
  {
    "commonality": "Average",
    "version": "7",
    "ua": "Mozilla/5.0 (iPad; CPU OS 7_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D167 Safari/9537.53"
  },
  {
    "commonality": "Average",
    "version": "5",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"
  },
  {
    "commonality": "Average",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7) AppleWebKit/534.48.3 (KHTML, like Gecko) Version/5.1 Safari/534.48.3"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 Mobile/14B72 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.4.10 (KHTML, like Gecko) Version/8.0.4 Safari/600.4.10"
  },
  {
    "commonality": "Average",
    "version": "7.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/7.1.7 Safari/537.85.16"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.38 (KHTML, like Gecko) Version/10.0 Mobile/14A5297c Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B146 Safari/8536.25"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.59.8 (KHTML, like Gecko) Version/5.1.9 Safari/534.59.8"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.52.7 (KHTML, like Gecko) Version/5.1.2 Safari/534.52.7"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/534.57.7 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.7"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (iPad; CPU OS 6_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B141 Safari/8536.25"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A523 Safari/8536.25"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G36 Safari/601.1"
  },
  {
    "commonality": "Average",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; PPC Mac OS X 10_5_8) AppleWebKit/534.50.2 (KHTML, like Gecko) Version/5.0.6 Safari/533.22.3"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/536.28.10 (KHTML, like Gecko) Version/6.0.3 Safari/536.28.10"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.53.11 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/536.29.13 (KHTML, like Gecko) Version/6.0.4 Safari/536.29.13"
  },
  {
    "commonality": "Average",
    "version": "11.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 Mobile/14B150 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.1.46 (KHTML, like Gecko) Safari/601.1.46"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B176 Safari/7534.48.3"
  },
  {
    "commonality": "Average",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B411 Safari/600.1.4"
  },
  {
    "commonality": "Average",
    "version": "7.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/7.1.6 Safari/537.85.15"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/10.0 Safari/602.1.31"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/534.51.22 (KHTML, like Gecko) Version/5.1.1 Safari/534.51.22"
  },
  {
    "commonality": "Average",
    "version": "7",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D167 Safari/9537.53"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A403 Safari/8536.25"
  },
  {
    "commonality": "Average",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us) AppleWebKit/531.21.11 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10"
  },
  {
    "commonality": "Average",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"
  },
  {
    "commonality": "Average",
    "version": "7",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.77.4 (KHTML, like Gecko) Version/7.0.5 Safari/537.77.4"
  },
  {
    "commonality": "Average",
    "version": "6.2",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/6.2.6 Safari/537.85.15"
  },
  {
    "commonality": "Average",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A405 Safari/600.1.4"
  },
  {
    "commonality": "Average",
    "version": "8",
    "ua": "Mozilla/5.0 (iPad; CPU OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A405 Safari/600.1.4"
  },
  {
    "commonality": "Average",
    "version": "8",
    "ua": "Mozilla/5.0 (iPad; CPU OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B435 Safari/600.1.4"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/536.30.1 (KHTML, like Gecko) Version/6.0.5 Safari/536.30.1"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2"
  },
  {
    "commonality": "Average",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B150 Safari/604.1"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8) AppleWebKit/536.25 (KHTML, like Gecko) Version/6.0 Safari/536.25"
  },
  {
    "commonality": "Average",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B93 Safari/604.1"
  },
  {
    "commonality": "Average",
    "version": "7",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2"
  },
  {
    "commonality": "Average",
    "version": "7",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X; en-us) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53"
  },
  {
    "commonality": "Average",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25"
  },
  {
    "commonality": "Average",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/603.1.13 (KHTML, like Gecko) Version/10.1 Safari/603.1.13"
  },
  {
    "commonality": "Average",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3"
  },
  {
    "commonality": "Average",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.0 Mobile/15E148 Safari/604.1"
  },
  {
    "commonality": "Average",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 Mobile/15C114 Safari/604.1"
  },
  {
    "commonality": "Average",
    "version": "7",
    "ua": "Mozilla/5.0 (iPad; CPU OS 7_0_3 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B511 Safari/9537.53"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 Mobile/14B72c Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "7",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E277 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "7.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A405 Safari/601.1"
  },
  {
    "commonality": "Average",
    "version": "7",
    "ua": "Mozilla/5.0 (iPad; CPU OS 7_0_6 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B651 Safari/9537.53"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A405 Safari/7534.48.3"
  },
  {
    "commonality": "Average",
    "version": "4",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16"
  },
  {
    "commonality": "Average",
    "version": "7",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2"
  },
  {
    "commonality": "Average",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; PPC Mac OS X) AppleWebKit/534.34 (KHTML, like Gecko) PhantomJS/1.9.8 Safari/534.34"
  },
  {
    "commonality": "Average",
    "version": "4",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.102011-10-16 20:23:10"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (iPod; CPU iPhone OS 6_1_6 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B500 Safari/8536.25"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E198 Safari/601.1"
  },
  {
    "commonality": "Average",
    "version": "5",
    "ua": "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 Mobile/14F90 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13D20 Safari/601.1"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A406 Safari/8536.25"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A551 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "6.2",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/6.2.7 Safari/537.85.16"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.51.22 (KHTML, like Gecko) Version/5.1.1 Safari/534.51.22"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.14 (KHTML, like Gecko) Version/6.0.1 Safari/536.26.14"
  },
  {
    "commonality": "Average",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.4.8 (KHTML, like Gecko) Version/8.0.3 Safari/600.4.8"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko)                 Version/6.0 Mobile/10A5376e Safari/8536.25 (compatible; SMTBot/1.0; +http://www.similartech.com/smtbot)"
  },
  {
    "commonality": "Average",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A365 Safari/600.1.4"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.4 (KHTML, like Gecko) Version/10.0 Mobile/14G5047a Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.5 Safari/534.55.3"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A346 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B350 Safari/8536.25"
  },
  {
    "commonality": "Average",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/8.0.2 Safari/600.2.5"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.40 (KHTML, like Gecko) Version/10.0 Mobile/14A5309d Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "7",
    "ua": "Mozilla/5.0 (iPad; CPU OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML like Gecko) Mobile/12A405 Version/7.0 Safari/9537.53"
  },
  {
    "commonality": "Average",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/537.36 (KHTML, like Gecko) Version/8.0 Safari/537.36"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 Mobile/14B72 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E5200d Safari/601.1"
  },
  {
    "commonality": "Average",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPod; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A403 Safari/8536.25"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.5 Safari/534.55.3"
  },
  {
    "commonality": "Average",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.1.1 Safari/538.1"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E237 Safari/601.1"
  },
  {
    "commonality": "Average",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Safari/522.0"
  },
  {
    "commonality": "Average",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/603.1.30 (KHTML, like Gecko) Safari/603.1.30"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
  },
  {
    "commonality": "Average",
    "version": "8",
    "ua": "Mozilla/5.0 (iPad; CPU OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A365 Safari/600.1.4"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.25 (KHTML, like Gecko) Version/6.0 Safari/536.25"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1"
  },
  {
    "commonality": "Average",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B435 Safari/600.1.4"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E230 Safari/601.1"
  },
  {
    "commonality": "Average",
    "version": "4",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 3_2_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B500 Safari/531.21.10"
  },
  {
    "commonality": "Average",
    "version": "6.2",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/6.2 Safari/537.85.10"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E230 Safari/601.1"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_6 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B500 Safari/8536.25"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E277 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.1.1 Safari/538.1"
  },
  {
    "commonality": "Average",
    "version": "7",
    "ua": "Mozilla/5.0 (iPad; CPU OS 7_0_2 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A501 Safari/9537.53"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2"
  },
  {
    "commonality": "Average",
    "version": "6.2",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/6.2.2 Safari/537.85.11"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 5_1 like Mac OS X; en-us) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B176 Safari/7534.48.3"
  },
  {
    "commonality": "Average",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; en-us) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10"
  },
  {
    "commonality": "Average",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/538.1 (KHTML, like Gecko) webinfo4 Safari/538.1"
  },
  {
    "commonality": "Average",
    "version": "7",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.74.9 (KHTML, like Gecko) Version/7.0.2 Safari/537.74.9"
  },
  {
    "commonality": "Average",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A366 Safari/600.1.4"
  },
  {
    "commonality": "Average",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B436 Safari/600.1.4"
  },
  {
    "commonality": "Average",
    "version": "7",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9) AppleWebKit/537.71 (KHTML, like Gecko) Version/7.0 Safari/537.71"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/534.52.7 (KHTML, like Gecko) Version/5.1.2 Safari/534.52.7"
  },
  {
    "commonality": "Average",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_1 like Mac OS X) AppleWebKit/604.3.1 (KHTML, like Gecko) Version/11.0 Mobile/15B5066f Safari/604.1"
  },
  {
    "commonality": "Average",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A342 Safari/601.1"
  },
  {
    "commonality": "Average",
    "version": "7.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/7.1.5 Safari/537.85.14"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3"
  },
  {
    "commonality": "Average",
    "version": "7",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_6 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B651 Safari/9537.53"
  },
  {
    "commonality": "Average",
    "version": "6.2",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/6.2.3 Safari/537.85.12"
  },
  {
    "commonality": "Average",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/603.2.4 (KHTML, like Gecko) Safari/603.2.4"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E237 Safari/601.1"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.3 (KHTML, like Gecko) Version/10.0 Mobile/14D15 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Safari/522.0"
  },
  {
    "commonality": "Average",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; fr-fr) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/536.30.1 (KHTML, like Gecko) Version/6.0.5 Safari/536.30.1"
  },
  {
    "commonality": "Average",
    "version": "7.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/7.1.3 Safari/537.85.12"
  },
  {
    "commonality": "Average",
    "version": "7",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.71 (KHTML like Gecko) WebVideo/1.0.1.10 Version/7.0 Safari/537.71"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A551 Safari/8536.25"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.39 (KHTML, like Gecko) Version/9.0 Safari/601.1.39"
  },
  {
    "commonality": "Average",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6; en-us) AppleWebKit/531.9 (KHTML, like Gecko) Version/4.0.3 Safari/531.9"
  },
  {
    "commonality": "Average",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B143 Safari/8536.25"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2"
  },
  {
    "commonality": "Average",
    "version": "3",
    "ua": "Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (iPad; CPU OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A8426 Safari/8536.25"
  },
  {
    "commonality": "Average",
    "version": "7.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/7.1.2 Safari/537.85.11"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.54.16 (KHTML, like Gecko) Version/5.1.4 Safari/534.54.16"
  },
  {
    "commonality": "Average",
    "version": "7",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_3 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B511 Safari/9537.53"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.38 (KHTML, like Gecko) Version/10.0 Safari/602.1.38"
  },
  {
    "commonality": "Average",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5"
  },
  {
    "commonality": "Average",
    "version": "5",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 6.1; tr-TR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"
  },
  {
    "commonality": "Average",
    "version": "7.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.4.10 (KHTML, like Gecko) Version/7.1.4 Safari/537.85.13"
  },
  {
    "commonality": "Average",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/9.1 Safari/601.5.17"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F72 Safari/601.1"
  },
  {
    "commonality": "Average",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.1.1 Safari/538.1"
  },
  {
    "commonality": "Average",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-us) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B176 Safari/7534.48.3"
  },
  {
    "commonality": "Average",
    "version": "7",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14"
  },
  {
    "commonality": "Average",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.2 (KHTML, like Gecko) Version/11.0 Mobile/15D5046b Safari/604.1"
  },
  {
    "commonality": "Average",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-us) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/10.0 Mobile/14D27 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "5",
    "ua": "Mozilla/5.0(iPad; U; CPU OS 4_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8F191 Safari/6533.18.5"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A343 Safari/601.1"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.40 (KHTML, like Gecko) Version/10.0 Safari/602.1.40"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/536.30.1 (KHTML, like Gecko) Version/6.0.5 Safari/536.30.1"
  },
  {
    "commonality": "Average",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.5"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B5110e Safari/601.1"
  },
  {
    "commonality": "Average",
    "version": "4",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 5_0_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10"
  },
  {
    "commonality": "Average",
    "version": "8.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.32 (KHTML, like Gecko) Version/8.1 Safari/601.1.32"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Safari/601.1.42"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13D15 Safari/601.1"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2"
  },
  {
    "commonality": "Average",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; ko-kr) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5"
  },
  {
    "commonality": "Average",
    "version": "7",
    "ua": "mozilla/5.0 (iphone; cpu iphone os 7_0_2 like mac os x) applewebkit/537.51.1 (khtml, like gecko) version/7.0 mobile/11a501 safari/9537.53"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E269 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.32 (KHTML, like Gecko) Version/10.0 Mobile/14A5261v Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; de-at) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 Mobile/14B150 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.59.10 (KHTML, like Gecko) Version/5.1.9 Safari/534.57.2"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A5346a Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 Mobile/14G60 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.57.5 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.4"
  },
  {
    "commonality": "Average",
    "version": "7",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 7_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML like Gecko) Version/7.0 Mobile/11D167 Safari/123E71C"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/536.25 (KHTML, like Gecko) Version/6.0 Safari/536.25"
  },
  {
    "commonality": "Average",
    "version": "3",
    "ua": "Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3"
  },
  {
    "commonality": "Average",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_1 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A403 Safari/604.1"
  },
  {
    "commonality": "Average",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.54.16 (KHTML, like Gecko) Version/5.1.4 Safari/534.54.16"
  },
  {
    "commonality": "Average",
    "version": "3",
    "ua": "Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A537a Safari/419.3"
  },
  {
    "commonality": "Average",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A525 Safari/8536.25"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/9.0.3 Safari/601.4.4"
  },
  {
    "commonality": "Average",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F69 Safari/600.1.4"
  },
  {
    "commonality": "Average",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/530.19.2 (KHTML, like Gecko) Version/4.0.2 Safari/530.19"
  },
  {
    "commonality": "Average",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.20 (KHTML, like Gecko) Version/10.1 Safari/603.1.20"
  },
  {
    "commonality": "Average",
    "version": "7",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.73.11 (KHTML, like Gecko) Version/7.0.1 Safari/537.73.11"
  },
  {
    "commonality": "Average",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J3 Safari/6533.18.5"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 Mobile/14F8089 Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A5335b Safari/602.1"
  },
  {
    "commonality": "Average",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E234 Safari/601.1"
  },
  {
    "commonality": "Average",
    "version": "4.1",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; fr) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/4.1.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A345 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A356 Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B117 Safari/6531.22.7"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 Mobile/14C89 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.14 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.14"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/600.1.4 (KHTML, like Gecko) Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.10 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.10"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 Mobile/14F89 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8G4 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; ja-jp) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.21 (KHTML, like Gecko) Version/10.0 Mobile/15A5278f Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0(iPad; U; CPU OS 4_3 like Mac OS X; %lang2%) adbeat.com/policy AppleWebKit/533.17.9 (KHTML, like Gecko) Version/6.0 Mobile/10B350 Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/536.26.17 (KHTML like Gecko) Version/6.0.2 Safari/536.26.17"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 9_3_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E238 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H141 Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPod; CPU iPhone OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B329 Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "6.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.71 (KHTML, like Gecko) Version/6.1 Safari/537.71"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/WK10171 Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; it-it) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.0.0 Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPad; CPU OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B436 Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 5_0 like Mac OS X; en-us) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; es-es) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 Mobile/14C92 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A406 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B145 Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/538.1 (KHTML, like Gecko) CasperJS/1.1.0-beta3+PhantomJS/2.0.0 Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_0 like Mac OS X; %lang2%) adbeat.com/policy AppleWebKit/600.1.4 (KHTML, like Gecko) Version/9.0 Mobile/12A366 Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "7.2",
    "ua": "Mozilla/5.0 (iPad; U; CPU iPad OS 5_0_1 like Mac OS X; en-us) AppleWebKit/535.1+ (KHTML like Gecko) Version/7.2.0.0 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/604.3.1 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4.1",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; it-it) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/4.1.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.25 (KHTML, like Gecko) Version/11.0 Mobile/15A5304j Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.0.0 Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Coast/2.0.2.69230 Mobile/11B554a Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "6.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.73.11 (KHTML, like Gecko) Version/6.1.1 Safari/537.73.11"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.38 (KHTML, like Gecko) Version/10.0 Mobile/14A300 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.0.0 Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; da-dk) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.6 Safari/600.6.3"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.43 (KHTML, like Gecko) Version/10.0 Safari/602.1.43"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8F190 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B142 Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.12"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_6) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/11.0 Safari"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPod; CPU iPhone OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A405 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.3 (KHTML, like Gecko) Version/11.0 Mobile/15D5049a Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.3 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.3"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPod; U; CPU iPhone OS 421 like Mac OS X; en-CA) AppleWebKit/533.17.9 (KHTML like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.43 (KHTML, like Gecko) Version/10.0 Mobile/14A5322e Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14D15 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/602.1.25 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.10"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4.1",
    "ua": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; ko-kr) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/4.1.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.1.28 (KHTML, like Gecko) Version/11.0 Safari/604.1.28"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Coast/3.21.84640 Mobile/12B411 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPad; CPU OS 8_0 like Mac OS X) AppleWebKit/537.51.3 (KHTML, like Gecko) Version/8.0 Mobile/11A4132 Safari/9537.145"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A5372a Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B101 Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "6.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/6.1.3 Safari/537.75.14"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.54.16 (KHTML, like Gecko) Version/5.1.4 Safari/534.54.16"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/9.0 Safari/601.1.56"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.2 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.2"
  },
  {
    "commonality": "Uncommon",
    "version": "6.2",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/6.2.5 Safari/537.85.14"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/538.1 (KHTML, like Gecko) Tableau Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.3.3 (KHTML, like Gecko) Version/10.0 Mobile/14G5037b Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.4 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.4"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.1"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_9_5 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A365 Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_1 like Mac OS X) AppleWebKit/602.2.8 (KHTML, like Gecko) Version/10.0 Mobile/14B55c Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPad; CPU OS 6_0_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A8500 Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.1 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.1"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B144 Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "6.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.77.4 (KHTML, like Gecko) Version/6.1.5 Safari/537.77.4"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPad; CPU OS 6_1_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B147 Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A5368a Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/534.52.7 (KHTML, like Gecko) Version/5.1 Safari/534.50"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_1 like Mac OS X) AppleWebKit/604.3.3 (KHTML, like Gecko) Version/11.0 Mobile/15B5078e Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPod; U; CPU iPhone OS 3_1_3 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7E18 Safari/528.16"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/124 (KHTML, like Gecko) Safari/125"
  },
  {
    "commonality": "Uncommon",
    "version": "3.2",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; fr-fr) AppleWebKit/525.27.1 (KHTML, like Gecko) Version/3.2.1 Safari/525.27.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; pt-br) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; de-de) AppleWebKit/534.15  (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.20 (KHTML, like Gecko) Version/10.0 Mobile/14E5230e Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 ( Macintosh; Intel Mac OS X 10_10_1 ) AppleWebKit/600.2.5 ( KHTML, like Gecko ) Version/8.0.2 Safari/600.2.5 ( compatible; CloudServerMarketSpider/1.0; +http://cloudservermarket.com/spider.html )"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.10 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.10"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.11 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.11"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/602.3.12 (KHTML, like Gecko) Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8F191 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A5354b Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPhone Simulator; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B176 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/10.0 Safari/602.1.50"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us) AppleWebKit/531.22.7 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.50 (KHTML, like Gecko) Version/9.0 Safari/601.1.50"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B141 Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/10.0 Safari/602.1.31"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) adbeat.com/policy AppleWebKit/602.1.38 (KHTML, like Gecko) Version/10.0 Mobile/14A5297c Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.31 (KHTML, like Gecko) Version/11.0 Mobile/15A5327g Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/534.54.16 (KHTML, like Gecko) Version/5.1.4 Safari/534.54.16"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A5345a Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E188a Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPod; CPU iPhone OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A523 Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.3 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.3"
  },
  { "commonality": "Uncommon", "version": "", "ua": "Safari" },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.1.2 Safari"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E8301 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (;;; en-us; Huawei-U8651S Build/U8651SV100R001USAC85B843) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_0 like Mac OS X) AppleWebKit/602.1.38 (KHTML, like Gecko) Version/10.0 Mobile/14A5297c Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "6.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/6.1.6 Safari/537.78.2"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_5 like Mac OS X; es-es) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/10.0 Safari/602.1.31"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Safari/601.6.17"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/11.0 Safari/604.1.38"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 Mobile/15C153 Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.52.7 (KHTML, like Gecko) Version/5.1.2 Safari/534.52.7"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-de) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.5 (KHTML, like Gecko) Version/8.0.2 Safari/600.3.5"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0_1 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A306 Safari/6531.22.7"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13C75 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A340 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.1 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/5"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/10.1 Safari/603.1.30"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 421 like Mac OS X; zh-CN) AppleWebKit/533.17.9 (KHTML like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.1 Safari/603.1.23"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.11 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.11"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/602.3.10 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.10"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/602.3.7 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.7"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.5 Safari/534.55.3"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPod; U; CPU iPhone OS 433 like Mac OS X; zh-CN) AppleWebKit/533.17.9 (KHTML like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.76.4 (KHTML, like Gecko) Version/7.0.4 Safari/537.76.4"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-us) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B208 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPod; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.38 (KHTML, like Gecko) Version/10.0 Mobile/14A300 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 11_2_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 Mobile/15C202 Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/536.26.14 (KHTML, like Gecko) Version/6.0.1 Safari/536.26.14"
  },
  {
    "commonality": "Uncommon",
    "version": "9.3",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/9.3.2 Safari/537.75.14"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 Mobile/15C107 Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 Mobile/14B100 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.59.10 (KHTML, like Gecko) Version/5.1.9 Safari/534.59.8"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 3_2_2 like Mac OS X; zh-cn) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B500 Safari/531.21.10"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) WebClip/10601.7.1 Safari/10601.7.7"
  },
  {
    "commonality": "Uncommon",
    "version": "6.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.74.9 (KHTML, like Gecko) Version/6.1.2 Safari/537.74.9"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.4 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.4"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/8.0.6 Safari/600.6.3"
  },
  {
    "commonality": "Uncommon",
    "version": "4.1",
    "ua": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; ja-jp) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/4.1.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A5362a Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/601.5.10 (KHTML, like Gecko) Version/9.1 Safari/601.5.10"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E269 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0 Safari/601.3.9"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; ja-jp) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A340 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "3.1",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_5; en-us) AppleWebKit/525.18 (KHTML, like Gecko) Version/3.1.2 Safari/525.20.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; es-es) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.6 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.6"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.3 (KHTML, like Gecko) Version/10.0 Mobile/14G5037b Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A5370a Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D169 Safari/9537.53"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_1 like Mac OS X) AppleWebKit/604.2.10 (KHTML, like Gecko) Version/11.0 Mobile/15A8391 Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.7 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.7"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/10.1 Mobile/15A432 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B5110e Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2"
  },
  {
    "commonality": "Uncommon",
    "version": "4.1",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; es) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/4.1.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0(Macintosh;U;Intel Mac OS X 10_6_3;en-us;V55 Build/MASTER)AppleWebKit/534.13(KHTML,like Gecko)Version4.0 Safari/534.13"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Safari/537.36 (Windows NT 6.2; WOW64) AppleWebKit/537.36"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_5 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 Mobile/15C5110b Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13D20 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A345 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "6.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.76.4 (KHTML, like Gecko) Version/6.1.4 Safari/537.76.4"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B5086a Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B92 Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "3.1",
    "ua": "Mozilla/5.0 (iPod; U; CPU iPhone OS 2_2_1 like Mac OS X; en-us) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5H11a Safari/525.20"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B14 3 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.1 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_5 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) WebClip/13604.5.6 Safari/13604.5.6"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.10 (KHTML, like Gecko) Version/10.0 Mobile/14C5077b Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/601.5.13 (KHTML, like Gecko) Version/9.1 Safari/601.5.13"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B405 Safari/531.21.10"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_5 like Mac OS X; fr-fr) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Safari/601.6.17"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.25 (KHTML, like Gecko) Version/11.0 Mobile/15A5304i Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4.1",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; ja-jp) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/4.1.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G34 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A407 Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Superbird/56.0.2924.87 Safari/537.36"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8F190 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.6 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.6"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; ko-kr) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; en-us) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10 FBSMTWB"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_7; en-us) AppleWebKit/534.20.8 (KHTML, like Gecko) Version/5.1 Safari/534.20.8"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Safari/601.6.17"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 9_3_4 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G35 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3 like Mac OS X; en-gb) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8F190 Safari/6533.18.5 Zetakey/3.2"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.8 (KHTML, like Gecko) Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.34 (KHTML, like Gecko) PhantomJS/1.9.0 Safari/534.34 Siteimprove (Accessibility)"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.2 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.2"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.34 (KHTML, like Gecko) PhantomJS/1.9.7 Safari/534.34"
  },
  {
    "commonality": "Uncommon",
    "version": "3",
    "ua": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/523.12 (KHTML, like Gecko) Version/3.0.4 Safari/523.12"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/312.9 (KHTML, like Gecko) Safari/312.6"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/8.0.2 Safari/600.2.5 (Getter/0.1)"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.29 (KHTML, like Gecko) Version/10.1 Safari/603.1.29"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (iPad; CPU OS 7_0_2 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8F191 Safari/6533.18.5 electricmobilesimulator"
  },
  {
    "commonality": "Uncommon",
    "version": "1.0",
    "ua": "Mozilla/5.0 (webOS/1.0; U; en-US) AppleWebKit/525.27.1 (KHTML, like Gecko) Version/1.0 Safari/525.27.1 Pre/1.0"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (iPhone; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1 Mobile/14F89 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; fr-fr) AppleWebKit/530.19.2 (KHTML, like Gecko) Version/4.0.2 Safari/530.19"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10 FBSMTWB"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.3 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.3"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25 (compatible; SemrushBot-SA/0.97; +http://www.semrush.com/bot.html)"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2 like Mac OS X) AppleWebKit/604.4.5 (KHTML, like Gecko) Version/11.0 Mobile/15C5092b Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G21 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0 Mobile/15D60 Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "6.2",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/600.4.10 (KHTML, like Gecko) Version/6.2.4 Safari/537.85.13"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko; Google Page Speed Insights) Version/8.0 Mobile/12F70 Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/604.1.31 (KHTML, like Gecko) Version/11.0 Safari/604.1.31"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.6 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.6"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.4.10 (KHTML, like Gecko) Version/8.0.4 Safari/600.4.10"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 11_0_1 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A402 Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.5"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; en-us) AppleWebKit/531.9 (KHTML, like Gecko) Version/4.0.3 Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F51a Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 6.1; de-DE) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/9.0 Mobile/10A5355d Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0_1 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko; Google Page Speed Insights) Version/6.0 Mobile/10A525 Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "4.1",
    "ua": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; it-it) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/4.1.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-us) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_0 like Mac OS X) AppleWebKit/602.1.32 (KHTML, like Gecko) Version/10.0 Mobile/14A5261v Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_1_3 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7E18 Safari/528.16"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us) AppleWebKit/534.1+ (KHTML, like Gecko) Version/5.0 Safari/533.16"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.3 (KHTML, like Gecko) Version/10.0 Mobile/14C5062e Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A452 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/602.1.27 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.15"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; BOLT/2.800) AppleWebKit/534.6 (KHTML, like Gecko) Version/5.0 Safari/534.6.3"
  },
  {
    "commonality": "Uncommon",
    "version": "8.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.27 (KHTML, like Gecko) Version/8.1 Safari/601.1.27"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/604.3.4 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.4"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; %lang2%) adbeat.com/policy AppleWebKit/531.21.10 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPad; CPU OS 6_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Coast/1.0.2.62956 Mobile/10B141 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "4.1",
    "ua": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; fr) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/4.1.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) WebClip/10603.2.5 Safari/10603.2.5"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (Windows XP Pro x64) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0.6 Safari/536.26"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_0 like Mac OS X) AppleWebKit/602.1.38 (KHTML, like Gecko) Version/10.0 Mobile/14A300 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPad; CPU OS 5_0_1 like Mac OS X) qjyBrowser/77618.1.15526 AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A405 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) WebClip/10601.5.17 Safari/10601.5.17.4"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPod; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B176 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A405 Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Unknown; UNIX BSD/SYSV system) AppleWebKit/534.34 (KHTML, like Gecko) smtube/16.1.0 Safari/534.34"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (S3xyM0nk3y; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_2 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/10.1 Mobile/15A421 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us; CMP741E) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B367 Safari/531.21.10"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/602.3.3 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.3"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 5_0 like Mac OS X; en-us) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.0.2 Mobile/9A5248d Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A4325c Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0 Mobile/15D5057a Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; fi-fi) AppleWebKit/420+ (KHTML, like Gecko) Safari/419.3"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 11_1_2 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B202 Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/601.5.8 (KHTML, like Gecko) Version/9.1 Safari/601.5.8"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/602.3.12 (KHTML, like Gecko) Safari/522.0"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.5 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.5"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) WebClip/10601.6.11 Safari/10601.6.17"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2 like Mac OS X) AppleWebKit/604.4.6 (KHTML, like Gecko) Version/11.0 Mobile/15C5097d Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "6.2",
    "ua": "Mozilla/5.0 (Macintosh; PPC Mac OS X 10_5_8) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/6.2.8 Safari/537.85.17"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/601.4.2 (KHTML, like Gecko) Version/9.0.3 Safari/601.4.2"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A5354b Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0(iPad; U; CPU OS 4_3 like Mac OS X; %lang2%) adbeat.com/policy AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8F191 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 Mobile/14F91 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_2_1 like Mac OS X; es-es) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPhone Simulator; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Mobile/9A334 Sangfulli Mobile Safari"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G12 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.2 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.2"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_7; en) AppleWebKit/530.19.2 (KHTML, like Gecko) Version/4.0.2 Safari/530.19.2"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/534.34 (KHTML, like Gecko) PhantomJS/1.9.2 Safari/534.34"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X; %lang2%) adbeat.com/policy AppleWebKit/534.46 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0 Mobile/15D100 Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 6.2; es-US ) AppleWebKit/540.0 (KHTML like Gecko) Version/6.0 Safari/8900.00"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/534.50.2 (KHTML, like Gecko) Version/4.0.2 Safari/530.19"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E8301 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.2 (KHTML, like Gecko) Version/10.0 Mobile/14D10 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPad; CPU OS 6_0_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A550 Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148a Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/604.1.28 (KHTML, like Gecko) Version/11.0 Safari/604.1.28"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.28.4 (KHTML, like Gecko) Version/6.0.3 Safari/536.28.4"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.7 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.7"
  },
  {
    "commonality": "Uncommon",
    "version": "3",
    "ua": "Mozilla/5.0 (iPod; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/3A101a Safari/419.3"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A5341a Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 Mobile/14B71 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/531.22.7"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_1_2 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7D11 Safari/528.16"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 Mobile/15C5107a Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.37 (KHTML, like Gecko) Version/9.0 Safari/601.1.37"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13C5055d Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F68 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows; chromeframe/2.4.8.5746) AppleWebKit/1.0 (KHTML, like Gecko) Bromium Safari/1.0"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A4325c Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 Mobile/15C107 Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 Mobile/14C89 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.6 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.6"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25 ( compatible; CloudServerMarketSpider/1.0; +http://cloudservermarket.com/spider.html )"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.5 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.5"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_1; en-us) AppleWebKit/531.9 (KHTML, like Gecko) Version/4.0.3 Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-us) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/538.34.48 (KHTML, like Gecko) Version/8.0 Safari/538.35.8"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.59.10 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPhone Simulator; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Surf/0.4.1 (X11; U; Unix; en-US) AppleWebKit/531.2+ Compatible (Safari)"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Mobile/14D27 Safari Line/7.1.2"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.4 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.4"
  },
  {
    "commonality": "Uncommon",
    "version": "3",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; de-de) AppleWebKit/523.10.3 (KHTML, like Gecko) Version/3.0.4 Safari/523.10"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.54.16 (KHTML, like Gecko) Version/5.1.4 Safari/534.54.16"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) WebClip/10601.4.2 Safari/10601.4.4"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.5 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.5"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; HTC_PH39100/1.63.502.4; en-us) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.1 (KHTML, like Gecko) Version/11.0 Mobile/15D5037e Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_5 like Mac OS X; de-de) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) WebClip/10600.7.2 Safari/10600.7.12"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 11_0_2 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A421 Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13D14 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/534.34 (KHTML, like Gecko) PhantomJS/1.9.7 Safari/534.34"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "\"Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1\""
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H141 Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_4 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8K2 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E5260b Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) WebClip/11603.3.8 Safari/12603.3.8"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_0 like Mac OS X; en-us) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-gb) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X; %lang2%) adbeat.com/policy AppleWebKit/534.46 (KHTML, like Gecko) Version/8.0 Mobile/9A334 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/603.1.12 (KHTML, like Gecko) Version/10.1 Safari/603.1.12"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone U CPU iPhone OS 4_3_5 like Mac OS X en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.21 (KHTML, like Gecko) Version/10.0 Mobile/15A5278f Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5"
  },
  {
    "commonality": "Uncommon",
    "version": "3.2",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-us) AppleWebKit/525.27.1 (KHTML, like Gecko) Version/3.2.1 Safari/525.27.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F68 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0 EdgiOS/41.10.1.0 Mobile/15D100 Safari/604.5.6"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/601.4.4 (KHTML, like Gecko) Version/9.1.1 Safari/7046A194A"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_7; en-us) AppleWebKit/530.18 (KHTML, like Gecko) Version/4.0 Safari/528.17"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E233 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.5 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.5"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Safari/604.1.34"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; ARM Mac OS X) AppleWebKit/538.15 (KHTML, like Gecko) Safari/538.15 Version/6.0"
  },
  {
    "commonality": "Uncommon",
    "version": "10.2",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/604.1.23(KHTML, like Gecko) Version/10.2 Safari/604.1.23"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.0.0 Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.34 (KHTML, like Gecko) PhantomJS/1.7.0 Safari/534.34"
  },
  {
    "commonality": "Uncommon",
    "version": "3",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-us) AppleWebKit/523.10.3 (KHTML, like Gecko) Version/3.0.4 Safari/523.10"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A466 Safari/9537.53"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E236 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) WebClip/10602.4.8 Safari/10602.4.8.0.1"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A)"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Safari/601.6.17"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPad; CPU OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Coast/1.0.2.62956 Mobile/10B329 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "9.2",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.18 (KHTML, like Gecko) Version/9.2 Safari/602.1.18"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; %lang2%) adbeat.com/policy AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B360 Safari/531.21.10"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B411 Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G29 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X; %lang2%) adbeat.com/policy AppleWebKit/534.46 (KHTML, like Gecko) Version/10.0 Mobile/9A334 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.34 (KHTML, like Gecko) Designer Safari/534.34"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.32 (KHTML, like Gecko) Version/10.0 Safari/602.1.32"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPod; U; CPU iPhone OS 3_1_2 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7D11 Safari/528.16"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPhone Simulator; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E5181f Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.52.7 (KHTML, like Gecko) Version/5.1.2 Safari/534.52.7"
  },
  {
    "commonality": "Uncommon",
    "version": "3.1",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.18 (KHTML, like Gecko) Version/3.1.1 Safari/525.17"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 Mobile/14B71 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "3",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/523.12 (KHTML, like Gecko) Version/3.0.4 Safari/523.12"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/533.1 (KHTML, like Gecko) Version/8.0 Safari/533.1"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPad; CPU iPad OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.6 Safari/534.57.2"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F69 Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13BC75 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10.2",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/604.1.5 (KHTML, like Gecko) Version/10.2 Safari/604.1.5"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_5 like Mac OS X; nl-nl) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.6 (KHTML, like Gecko) Version/10.0 Mobile/14G57 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5.2",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8) AppleWebKit/535.18.5 (KHTML, like Gecko) Version/5.2 Safari/535.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_2 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 EdgiOS/41.41.4.0 Mobile/15B202 Safari/604.3.5"
  },
  {
    "commonality": "Uncommon",
    "version": "1.0",
    "ua": "Mozilla/5.0 (webOS/1.4.5.1; U; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Version/1.0 Safari/532.2 Pixi/1.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; da-dk) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Windows NT 5.1; en-US) AppleWebKit/535.12 (KHTML, like Gecko) Version/5.0.1 Safari/535.12"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Coast/2.0.0.67915 Mobile/11B554a Safari/7534.48.3"
  },
  { "commonality": "Uncommon", "version": "", "ua": "Ipad Iphone Safari" },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A ACHEETAHI/1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/11.0 Safari/604.1.38"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/603.3.8 (KHTML, like Gecko) Safari/603.3.8"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.41 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A456 Safari/602.1 AlohaBrowser/2.0"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; PPC Mac OS X 10_5_8) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/5.0.6 Safari/533.22.3"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Phone; U; CPU like Mac OS X; en-gb) AppleWebKit/532+ (KHTML, like Gecko) Version/10.1 Mobile/1A538b Safari/419.3"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPod; CPU iPhone OS 6_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B144 Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/10.0 Safari/602.1.50"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.3 (KHTML, like Gecko) Version/10.0 Mobile/14F5080a Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4 (compatible; SBooksNet/1.0; +http://s-books.net/crawl_policy)"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E5214d Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/538.44 (KHTML, like Gecko) Version/8.0 Safari/538.44"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_10_5 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B411 Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_0 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B500 Safari/531.21.10"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A432 Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/604.1.25 (KHTML, like Gecko) Version/11.0 Safari/604.1.25"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.3 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.3"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G33 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7 electricmobilesimulator"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A344 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_0 like Mac OS X) AppleWebKit/602.1.40 (KHTML, like Gecko) Version/10.0 Mobile/14A5309d Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.1 (KHTML, like Gecko) Version/10.0 Mobile/14F5065b Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; en-us) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/10.0 Mobile/14D27 Safari/602.1\t"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) WebClip/10601.2.3 Safari/10601.2.7.2"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.5"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.28 (KHTML, like Gecko) Version/11.0 Mobile/15A5318g Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "6.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9) AppleWebKit/537.35.1 (KHTML, like Gecko) Version/6.1 Safari/537.35.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.29 (KHTML, like Gecko) Version/10.0 Mobile/14E5249d Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; BOLT/2.340) AppleWebKit/530+ (KHTML, like Gecko) Version/4.0 Safari/530.17 UNTRUSTED/1.0 3gpp-gba UNTRUSTED/1.0"
  },
  {
    "commonality": "Uncommon",
    "version": "4.1",
    "ua": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; es) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/4.1.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B87 Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; zh-tw) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPod; CPU iPhone OS 6_1_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B146 Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/10.0 Safari/602.1.31"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/538.15 (KHTML, like Gecko) Safari/538.15 Version/6.0 dwb/2014.04.23"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"
  },
  {
    "commonality": "Uncommon",
    "version": "3.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/534.50.2 (KHTML, like Gecko) Version/3.1.2 Safari/525.20.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/0600.1.25 (KHTML, like Gecko) FluidApp Version/1955 Safari/0600.1.25"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A366 Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; CPU OS 4_3_5 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 Safari/602.1.31"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/534.50.2 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10"
  },
  {
    "commonality": "Uncommon",
    "version": "6.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/6.1.3 Safari/537.75.14"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_6 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8E200 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "3",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en_US) AppleWebKit/522.7 (KHTML, like Gecko) Dreamweaver/10.0.0.4117 Version/3.0 Safari/522.7"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A456 Safari/602.1 AlohaBrowser/1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (compatible; Odyssey Web Browser; AROS; rv:1.16) AppleWebKit/535.14 (KHTML, like Gecko) OWB/1.16 Safari/535.14"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 10_0_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A456 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.71 (KHTML like Gecko) Version/7.0 Safari/537.71"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.31 (KHTML, like Gecko) Version/11.0 Mobile/15A5327g Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12D508 Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.34 (KHTML, like Gecko) demobrowser/0.1 Safari/534.34"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/9.1.3 Safari/601.7.8"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 Mobile/14F5089a Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; en_US) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B117 Safari/6531.22.7"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; en-us) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (X11; U; CrOS i686 0.13.507) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.7 (KHTML, like Gecko) Version/10.0 Mobile/14C5069c Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; fr-fr) AppleWebKit/531.21.11 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/531.22.7 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-us) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "3",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-us) AppleWebKit/523.15.1 (KHTML, like Gecko) Version/3.0.4 Safari/523.15"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.1 Safari/601.3.9"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (iPhone; CPU OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Mobile/14E304 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A5362a Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0 EdgiOS/41.9.0.0 Mobile/15D60 Safari/604.5.6"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; es-es) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPad; CPU OS_5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version 5.1 Mobile/9A334 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 Safari/602.1.31"
  },
  {
    "commonality": "Uncommon",
    "version": "11.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.111.15 (KHTML, like Gecko) Safari Version/11.1.3"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3 like Mac OS X; en-us) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E5191d Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; nl-nl) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11.2",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.2 Safari/605.1.15"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A342 Safari/601.1)"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPod; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A403 Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/1533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/61533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 5_0_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B367 Safari/531.21.10"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/11.0.1 Safari/601.3.9"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.100 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.100"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPad; CPU OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A405 Safari/7534.48.3 Newsan/2.0 (Hisense/1.1; TV)"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7"
  },
  {
    "commonality": "Uncommon",
    "version": "10.3",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.3 Mobile/14E277 Safari/603.1.30"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPad;U;CPU OS 6_0 like Mac OS X;en-us)AppleWebKit/536.26(KHTML,like Gecko)Version/6.0 Mobile/10A5355d Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.59.10 (KHTML, like Gecko) WebClip/6534.51.13 Safari/6534.59.10"
  },
  {
    "commonality": "Uncommon",
    "version": "3.1",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_5; fr-fr) AppleWebKit/525.18 (KHTML, like Gecko) Version/3.1.2 Safari/525.20.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/10.0 Mobile/14D23 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; PPC Mac OS X 10_5_8) AppleWebKit/536.28.8+ (KHTML, like Gecko) Version/5.0.6 Safari/533.22.3"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/531.9 (KHTML, like Gecko) Version/4.0.3 Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_5 like Mac OS X; it-it) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.34 (KHTML, like Gecko) RelIdApp/3.1.6 Safari/534.34"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/10.1 Safari/602.1 EdgiOS/41.10.1.0"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.43 (KHTML, like Gecko) Version/9.0 Safari/601.1.43"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B411 Safari/600.1.4 (compatible; YandexMobileBot/3.0; +http://yandex.com/bots)"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/546.10 (KHTML, like Gecko) Version/6.0 Mobile/7E18WD Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/604.1.27 (KHTML, like Gecko) Version/11.0 Safari/604.1.27"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "\"Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5\""
  },
  {
    "commonality": "Uncommon",
    "version": "6.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.71 (KHTML, like Gecko) Version/6.1 Safari/537.71"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.78.2 (KHTML, like Gecko, Safari/9537.85.12.18) ADM/784"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_1; fr-fr) AppleWebKit/531.9 (KHTML, like Gecko) Version/4.0.3 Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/538.1 (KHTML, like Gecko) Tableau Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) WebClip/13604.4.7.1.3 Safari/13604.4.7.1.3"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/534.34 (KHTML, like Gecko) python Safari/534.34"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0 EdgiOS/41.11.0.0 Mobile/15D100 Safari/604.5.6"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_8_0; nl-nl) AppleWebKit/537.75.14 (KHTML, like Gecko) Fluid/1.7.1 Safari/537.75.14"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) WebClip/10603.1.30.0.34 Safari/10603.1.30.0.34"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B411 Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Safari/522.0"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; de-de) AppleWebKit/531.21.11 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3,gzip(gfe)"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPhone; CPU OS 7.1.2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) 1Password/4.5.3 (like Version/11D257 Mobile/7.1.2 Safari/8536.25)"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/604.5.6 (KHTML, like Gecko) Safari/604.5.6"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/538.1 (KHTML, like Gecko) PokerClient Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_1) AppleWebKit/536.25 (KHTML, like Gecko) Version/6.0 Safari/536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS (null) like Mac OS X) AppleWebKit/(null) (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/534.34 (KHTML, like Gecko) CasperJS/1.1.3+PhantomJS/1.9.8 Safari/534.34"
  },
  {
    "commonality": "Uncommon",
    "version": "1.0",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/1.0 Safari/1"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_7;en-us) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Safari/530.17"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; en-us) AppleWebKit/530.19.2 (KHTML, like Gecko) Version/4.0.2 Safari/530.19"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E227 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; it-it) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "3.1",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_4; en-us) AppleWebKit/525.18 (KHTML, like Gecko) Version/3.1.2 Safari/525.20.1"
  },
  {
    "commonality": "Uncommon",
    "version": "7.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.1.7 Safari/7046A194A"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A5346a Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.5 Safari/534.55.3"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 EdgiOS/41.9.0.0 Mobile/15C202 Safari/604.4.7"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; PPC Mac OS X 10_10_5) AppleWebKit/603.2.5 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.5"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.34 (KHTML, like Gecko) CasperJS/1.1.0-beta3+PhantomJS/1.9.2 Safari/534.34"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; PowerPC AmigaOS 4.1; Odyssey Web Browser; rv:1.23) AppleWebKit/538.1 (KHTML, like Gecko) OWB/1.23 Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 11_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B93 Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/6.0.2 Safari/534.57.2"
  },
  {
    "commonality": "Uncommon",
    "version": "6.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/6.1 Safari/537.71"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT based; en-US) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Safari/528.17"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/601.5.17 (KHTML, like Gecko) Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.31"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_8 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8E401 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_9_5 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B411 Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E5200d Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) WebClip/10602.2.14.0.5 Safari/10602.2.14.0.7"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_5 like Mac OS X; th-th) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/602.3.10 (KHTML, like Gecko) Version/10.0 Mobile/14C5077b Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "3",
    "ua": "Mozilla/5.0\u00a0(iPhone\u00a0U\u00a0CPU like\u00a0Mac\u00a0OS X\u00a0en)\u00a0AppleWebKit/420+\u00a0(KHTML,\u00a0like\u00a0Gecko)Version/3.0\u00a0Mobile/1A543\u00a0Safari/419.3"
  },
  {
    "commonality": "Uncommon",
    "version": "12.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_12_0) AppleWebKit/604.1.30 (KHTML, like Gecko) Version/12.1 Safari/604.1.30"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_1) AppleWebKit/534.48.3 (KHTML, like Gecko) Version/5.1 Safari/534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; CPU OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_1 like Mac OS X) AppleWebKit/604.2.10 (KHTML, like Gecko) Version/11.0 Mobile/15A8401 Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3         (KHTML, like Gecko) Version/5.1.5 Safari/534.55.3"
  },
  {
    "commonality": "Uncommon",
    "version": "6.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.73.11 (KHTML, like Gecko) Version/6.1.1 Safari/537.73.11"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0  like Mac OS X) AppleWebKit/602.1.32 (KHTML, like Gecko) Version/10.0 Mobile/14A5261v Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46.60.1 (KHTML, like Gecko) Version/6.0 Mobile/10A523 Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.1 (KHTML, like Gecko) Version/10.0 Mobile/14G5028a Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/5.1 Mobile/11B554a Safari/9537.53"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPhone; OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14.1.1 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 5_0 like Mac OS X; en-us) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.0.2 Mobile/9A5248d Safari/6533.18.5#2.0#TCL/TCL-ME-MS68-S1/22/tclwebkit1.0.2/1920*1080(444178386,null;221158002,f58ad39ee4cb4fc185e3154bc762e607)"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS X 10_9_5 like Mac OS X) AppleWebKit/357.51.2 (KHTML, like Gecko) Version 7.0 Mobile/11D257Safari/9537.53"
  },
  {
    "commonality": "Uncommon",
    "version": "6.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.77.4 (KHTML, like Gecko) Version/6.1.5 Safari/537.77.4"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-us) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/531.9 (KHTML, like Gecko) Version/4.0.3 Safari/531.9 FBSMTWB"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; ja-jp) AppleWebKit/531.21.11 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13D11 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.38 (KHTML, like Gecko) Version/10.0 Safari/602.1.38"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 Mobile/14B67 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) WebClip/13604.4.7.1.6 Safari/13604.4.7.1.6"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/538.1 (KHTML, like Gecko) CustomBrowser Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 Mobile/14C82 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4.1",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; de-de) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/4.1.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 Mobile/15C5111a Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X; %lang2%) adbeat.com/policy AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B176 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.43 (KHTML, like Gecko) Version/10.1.2 Safari/602.1.43"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/10.0.1 Safari/601.3.9"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A5370a Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_3 like Mac OS X) AppleWebKit/603.1.29 (KHTML, like Gecko) Version/10.0 Mobile/14E5249d Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0 Mobile/15D60 Safari/604.5.6"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/546.10 (KHTML, like Gecko) Version/6.0 Mobile/7E18WD Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/538.15 (KHTML, like Gecko) Safari/538.15 Version/6.0 dwb/2014.03.16"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; vi-vn) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B117 Safari/6531.22.7"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) WebClip/12604.1.38.1.7 Safari/12604.1.38.1.7"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/534.34 (KHTML, like Gecko) wkhtmltopdf Safari/534.34"
  },
  {
    "commonality": "Uncommon",
    "version": "3.1",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 2_2 like Mac OS X; en-us) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5G77 Safari/525.20"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 5_0 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J3 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; es-es) AppleWebKit/531.21.11 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10"
  },
  {
    "commonality": "Uncommon",
    "version": "7.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/7.1 Safari/537.85.10"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_1 like Mac OS X) AppleWebKit/604.3.3 (KHTML, like Gecko) Version/11.0 Mobile/15B5078e Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/11.0.3 Safari"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.1 Safari/601.2.7"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/602.1.37 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.4"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.25 (KHTML, like Gecko) Version/11.0 Mobile/15A5304j Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.6 (KHTML, like Gecko) Version/10.0 Mobile/14G5053a Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.2 (KHTML, like Gecko) Safari/125.8"
  },
  {
    "commonality": "Uncommon",
    "version": "3.1",
    "ua": "Mozilla/5.0 (iPod; U; CPU iPhone OS 2_2_1 like Mac OS X; en-us) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5H11 Safari/525.20"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/11.0 Safari/603.1.50"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2"
  },
  {
    "commonality": "Uncommon",
    "version": "3.1",
    "ua": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; en) AppleWebKit/525.18 (KHTML, like Gecko) Version/3.1.2 Safari/525.22"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0 Safari/537.78.2"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B150 Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.3 (KHTML, like Gecko) Safari/535.3 EAWebKit/13.4.2.0.0 APB/2.0"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0_1 like Mac OS X) AppleWebKit/537.4 (KHTML, like Gecko; Google Page Speed Insights) Version/6.0 Mobile/10A525 Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 9_0_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A404 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 6.1; de-AT) AppleWebKit/533.3 (KHTML, like Gecko) Qt/4.7.4 Safari/533.3"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_5 like Mac OS X; en-gb) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 3_2_2 like Mac OS X; it-it) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B500 Safari/531.21.10"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/538.1 (KHTML, like Gecko) demobrowser/0.1 Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4.1",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; pt-pt) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/4.1.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.54.16 (KHTML, like Gecko) Version/5.1.2 Safari/534.52.7"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0(iPad; U; CPU iPhone OS 11_0 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/11.0.0 Mobile/7B314 Safari/531.21.10"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/10.1 Safari/603.1.30"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 Mobile/14C90 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Version/11.0.2 Safari/602.4.8"
  },
  {
    "commonality": "Uncommon",
    "version": "3.2",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5; en-US) AppleWebKit/525.27.1 (KHTML, like Gecko) Version/3.2.1 Safari/525.27.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.5 (KHTML, like Gecko) Version/11.0 Mobile/15D5054a Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.1 Safari/602.4.8"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Safari/601.6.17"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13C5055d Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/534.50.2 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 1063; tr-DE) AppleWebKit/533.16 (KHTML like Gecko) Version/5.0 Safari/533.16"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; fr-fr) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "4.1",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; nl-nl) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/4.1.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9.2.1 like Mac OS X; en_US) AppleWebKit/1 (KHTML, like Gecko) Mobile/1 Safari/1 iPhone/1 EtsyInc/4.31 rv:43100.64.0"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/602.4.6 (KHTML, like Gecko) Safari/602.4.6"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.73.11 (KHTML like Gecko) Version/7.0.1 Safari/537.73.11"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_1; nl-nl) AppleWebKit/532.3+ (KHTML, like Gecko) Fluid/0.9.6 Safari/532.3+"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B144 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 Mobile/14C82 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/11.0 Safari/601.2.7"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_7) AppleWebKit/534.16+ (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU OS 4_2_1 like Mac OS X) AppleWebKit/532.9 (KHTML, like Gecko) Version/5.0.3 Mobile/8B5097d Safari/6531.22.7"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E5233a Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/418.8 (KHTML, like Gecko) Safari/419.3"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; xx-xx) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/10.0.1 Safari/601.2.7"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/534.34 (KHTML, like Gecko) PhantomJS/1.9.8 Safari/534.34"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/8.0.4 Safari/600.4.10"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.1.32 (KHTML, like Gecko) Version/11.0 Safari/604.1.32"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 Safari/602.1.31"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/9.1.3 Safari/601.7.8"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 5.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 10_3_3 like Mac OS X; en-ph) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B141 Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/538.1 (KHTML, like Gecko) TestQt Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "1.0",
    "ua": "Mozilla/5.0 (webOS/1.4.5; U; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Version/1.0 Safari/532.2 Pixi/1.1"
  },
  {
    "commonality": "Uncommon",
    "version": "6.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.76.4 (KHTML, like Gecko) Version/6.1.4 Safari/537.76.4"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; fi-fi) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46.140 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A456 Safari/602.1 AlohaBrowser/1.5"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0 Mobile/15D5057a Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 11_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 Mobile/15C114 Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/9.0 Mobile Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 EdgiOS/41.41.4.0 Mobile/15C114 Safari/604.4.7"
  },
  {
    "commonality": "Uncommon",
    "version": "3.1",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 2_0 like Mac OS X; en-us) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5A347 Safari/525.200"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.34 (KHTML, like Gecko) Arena Safari/534.34"
  },
  {
    "commonality": "Uncommon",
    "version": "4.1",
    "ua": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; en-us) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/4.1.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; fr-fr) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B117 Safari/6531.22.7"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 3_2_2 like Mac OS X; es-es) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B500 Safari/531.21.10"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Coast/2.0.1.68788 Mobile/11B554a Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6; fr-fr) AppleWebKit/531.9 (KHTML, like Gecko) Version/4.0.3 Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; ko-kr) AppleWebKit/531.21.11 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/604.3.5 (KHTML, like Gecko) WebClip/13604.3.5 Safari/13604.3.5"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.6 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.6"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Safari/522.0"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_0 like Mac OS X) AppleWebKit/601.1.39 (KHTML, like Gecko) Version/9.0 Mobile/13A4305g Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/534.50.2 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/538.1 (KHTML, like Gecko) Tableau/10.2 Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.4.4 (KHTML, like Gecko) Version/9.1.1 Safari/601.4.4"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPad; CPU OS 7_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Coast/2.0.5.71150 Mobile/11D167 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_2 like Mac OS X) Mac OS X/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A501 Safari/9537.53"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.30"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/538.1 (KHTML, like Gecko) fancybrowser Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; ko-kr) AppleWebKit/531.9 (KHTML, like Gecko) Version/4.0.3 Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.5 Safari/534.55.3"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13G36 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "3.2",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_7; en-us) AppleWebKit/525.28.3 (KHTML, like Gecko) Version/3.2.3 Safari/525.28.3"
  },
  {
    "commonality": "Uncommon",
    "version": "4.1",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; sv-se) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/4.1.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPod; U; CPU iPhone OS 41 like Mac OS X; fr-CA) AppleWebKit/532.9 (KHTML like Gecko) Version/4.0.5 Mobile/8B118 Safari/6531.22.7"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/538.1 (KHTML, like Gecko) Tableau Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) 63.0.3239 Safari/537.36"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A5372a Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-us) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27 FBSMTWB"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B440 Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "3.2",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; hu-hu) AppleWebKit/525.27.1 (KHTML, like Gecko) Version/3.2.1 Safari/525.27.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 6.0; hu-HU) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "6.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.74.9 (KHTML, like Gecko) Version/6.1.2 Safari/537.74.9"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.78.2 (KHTML, like Gecko) WebClip/9537.85.14.10 Safari/9537.85.14.17"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 6_1 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/6.0.5 Mobile/8B117 Safari/6531.22.7"
  },
  {
    "commonality": "Uncommon",
    "version": "3.1",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 2_0_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5B108 Safari/525.20"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; PPC Mac OS X 10_10_5) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; fr-fr) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/603.1.10 (KHTML, like Gecko) Version/10.1 Safari/603.1.10"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_1 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B117 Safari/6531.22.7"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; ru; CPU iPhone OS 4_2_1 like Mac OS X; ru) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148a Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "3.2",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.27.1 (KHTML, like Gecko) Version/3.2.1 Safari/525.27.1"
  },
  {
    "commonality": "Uncommon",
    "version": "3.2",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/525.27.1 (KHTML, like Gecko) Version/3.2.1 Safari/525.27.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Mobile/14B150 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; it-it) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0(iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26(KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/603.1.11 (KHTML, like Gecko) Version/10.1 Safari/603.1.11"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A406 Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69 Safari/601.1.46"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20 (KHTML, like Gecko) Version/5.0.4 Safari/533.20"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/604.1.38 (KHTML, like Gecko) Safari/604.1.38"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_9_5 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12D508 Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.29 (KHTML, like Gecko) Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/600.3.10 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.10"
  },
  {
    "commonality": "Uncommon",
    "version": "4.1",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-en) AppleWebKit/533.16 (KHTML, like Gecko) Version/4.1 Safari/533.16"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.34 (KHTML, like Gecko) PhantomJS/1.9.8 Safari/534.34"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H8 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_1 like Mac OS X) AppleWebKit/604.3.1 (KHTML, like Gecko) Version/11.0 Mobile/15B5066f Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "3",
    "ua": "Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A102 Safari/419 (United States)"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 6_0 like Mac OS X; en-us) AppleWebKit/530.18 (KHTML, like Gecko) Version/5.0 Mobile/7A341 Safari/530.16"
  },
  {
    "commonality": "Uncommon",
    "version": "4.1",
    "ua": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; de-de) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/4.1.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en_US) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_5 like Mac OS X; pt-br) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "3.1",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_5; en-us) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.2 Safari/525.20.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version 10.1.1 Safari/603.2.4"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13C71 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10.3",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.3 Mobile/14E277 Safari/603.1.30"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; nb-no) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 108) AppleWebKit/536.15 (KHTML like Gecko) Version/6.0 Safari/536.16"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_2_1 like Mac OS X) AppleWebKit/602.4.3 (KHTML, like Gecko) Version/10.0 Mobile/14D15 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 EdgiOS/41.6.0.0 Mobile/15C153 Safari/604.4.7"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0(iPad; U; CPU OS 5_0 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8F191 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; es-es) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10102) AppleWebKit/640.3.18 (KHTML like Gecko) Version/10.0.2 Safari/640.3.18"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B143 Safari/8536.25,gzip(gfe)"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/604.1.21 (KHTML, like Gecko) Version/11.0 Safari/604.1.21"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_5 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B601 Safari/9537.53"
  },
  {
    "commonality": "Uncommon",
    "version": "3.1",
    "ua": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_4; en-us) AppleWebKit/525.18 (KHTML, like Gecko) Version/3.1.2 Safari/525.20.1"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.76.4 (KHTML like Gecko) Version/7.0.4 Safari/537.76.4"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A346 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B5130b Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/538.1 (KHTML, like Gecko) CasperJS/1.1.4+PhantomJS/2.1.1 Safari/538.1"
  },
  { "commonality": "Uncommon", "version": "", "ua": "safari-mac" },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_5 like Mac OS X; tr-tr) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F61 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.34 (KHTML, like Gecko) Designer Safari/534.34"
  },
  { "commonality": "Uncommon", "version": "", "ua": "Safari Mac" },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/601.1.17 (KHTML, like Gecko) Version/8.0 Mobile/13A175 Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1 MXiOS/4.8.7.60"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/521.25 (KHTML, like Gecko) Safari/521.24"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/10.1 Mobile/15B93 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10.2",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/604.1.19 (KHTML, like Gecko) Version/10.2 Safari/604.1.19"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML like Gecko) Version/7.0.6 Safari/537.78.2"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E5231a Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.2.7"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A5345a Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; de-de) AppleWebKit/534.15+ (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Version/11.0.1 Safari/602.4.8"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/538.1 (KHTML, like Gecko) Otter/0.1.01 Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/534.52.7 (KHTML, like Gecko) Version/5.1.2 Safari/534.52.7"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.27+ (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/602.1.39 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.5"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.77.4 (KHTML like Gecko) Version/7.0.5 Safari/537.77.4"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; PPC Mac OS X 10_5_8) AppleWebKit/534.50.2 (KHTML, like Gecko) Stainless/0.8 like Version/5.1 Safari/534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; ja-jp) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0 Mobile/15D100 Safari/604.5.6"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/534.52.7 (KHTML, like Gecko) Version/5.1.2 Safari/534.52.7"
  },
  { "commonality": "Uncommon", "version": "", "ua": "Safari/537.36" },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_2 like Mac OS X) AppleWebKit/604.4.5 (KHTML, like Gecko) Version/11.0 Mobile/15C5092b Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Windows; U; en_US) AppleWebKit/533.19.4 (KHTML, like Gecko) Dreamweaver/12.0.0.5808 Version/5.0.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.1.2 Mobile/14C92 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B5097d Safari/6531.22.7"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.54.16 (KHTML, like Gecko) Version/5.1.4 Safari/534.54.16"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.40 (KHTML, like Gecko) Version/10.0 Safari/602.1.40"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/602.1.31 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.52.7 (KHTML, like Gecko) Version/5.1.2 Safari/534.52.7"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/603.1.6 (KHTML, like Gecko) Version/10.1 Safari/603.1.6"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/534.57.7 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0; managedpc) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1 Safari/601.6.17"
  },
  {
    "commonality": "Uncommon",
    "version": "4.1",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; en) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/4.1.2 Safari/533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; zh-cn) AppleWebKit/531.9 (KHTML, like Gecko) Version/4.0.3 Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "1.0",
    "ua": "Mozilla/5.0 (webOS/1.4.5; U; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Version/1.0 Safari/532.2 Pre/1.1"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "\"Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25\""
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_3 like Mac OS X; en-US) AppleWebKit/535.16.10 (KHTML, like Gecko) Version/5.0.2 Mobile/8C28a Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64; chromeframe/24.0.1312.57) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; de-de) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.3.6 (KHTML, like Gecko) Version/10.0 Mobile/14G57 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; ru-ru) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B5119e Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E5277a Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/9.0 Safari/600.7.12"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Phone; U; CPU like Mac OS X; en-gb) AppleWebKit/532+ (KHTML, like Gecko) Version/11.0 Mobile/1A538b Safari/419.3"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/534.30 (KHTML, like Gecko) Version/8.0 Safari/534.30"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_7_3; en_US) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.3.2 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.2"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/538.1 (KHTML, like Gecko) fancybrowser Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/602.1.33 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/9.1.3 Safari/601.7.8"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; tr-tr) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.59.10 (KHTML, like Gecko, Safari/6534.59.10) ADM/763"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46.60.1 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "11.2",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.2 Safari/605.1.15"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_4 like Mac OS X; ja-jp) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8K2 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "3",
    "ua": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/523.10.3 (KHTML, like Gecko) Version/3.0.4 Safari/523.10"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B87 Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.0.3 Safari/601.4.4"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E5225a Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; es-es) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17,gzip(gfe)"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/538.1 (KHTML, like Gecko) demobrowser/0.1 Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B367 Safari/531.21.10"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.28 (KHTML, like Gecko) Version/11.0 Mobile/15A5318g Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Safari/601.6.17"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/536.30.1 (KHTML, like Gecko, Safari/8536.30.1) ADM/763"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.78.2 (KHTML, like Gecko) Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/602.1.35 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.4"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13G36 Safari/601.1.46"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E5214d Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E5269a Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPhone) AppleWebKit (KHTML, like Gecko) Mobile Safari/jtrip-app-1.0"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/603.1.20 (KHTML, like Gecko) Safari/603.1.20"
  },
  {
    "commonality": "Uncommon",
    "version": "11.2",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/11.2.2 Safari/601.3.9"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.6 (KHTML, like Gecko) Version/10.0 Mobile/14G5057a Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/10.0.2 Safari/601.3.9"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 EdgiOS/41.8.0.0 Mobile/15C202 Safari/604.4.7"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/538.1 (KHTML, like Gecko) python Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; it-it) AppleWebKit/531.22.7 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_9 rv:5.0; ar-ae)  AppleWebKit/537.2.1 (KHTML, like Gecko) Version/6.0.4 Safari/537.2.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/538.1 (KHTML, like Gecko) CasperJS/1.1.4+PhantomJS/2.1.1 Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10.2",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/604.1.6 (KHTML, like Gecko) Version/10.2 Safari/604.1.6"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_12_6 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B411 Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPhone; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/603.1.3 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 Mobile/14C92 Safari/602.3.12"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/534.50.2 (KHTML, like Gecko) Version/4.0.3 Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A5335b Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_0_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A456 Safari/602.1 AlohaBrowser/2.0"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.1.39 (KHTML, like Gecko) Version/9.0 Safari/601.1.39"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_0 like Mac OS X) AppleWebKit/602.1.43 (KHTML, like Gecko) Version/10.0 Mobile/14A5322e Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPad; CPU 0S 5_0_1 like Mac OS X) AppleWebkit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A405 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/538.1 (KHTML, like Gecko)  Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/534.54.16 (KHTML, like Gecko) Version/5.1.4 Safari/534.54.16"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.3 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.3"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; it-it) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_5 like Mac OS X; ar) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "7.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.1.7 Safari/537.75.14"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13C75 Safari/601.1     this is fake UA, get mad to the dev @EmojiDesu"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F65 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Safari/522.0"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/11.00 Safari/601.7.7"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.25 (KHTML, like Gecko) Version/11.0 Mobile/15A5304i Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.34 (KHTML, like Gecko) PhantomJS/1.9.2 Safari/534.34"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Coast/2.0.5.71150 Mobile/11B554a Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/538.1 (KHTML, like Gecko) webinfo7 Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.2 (KHTML, like Gecko) Safari/535.2 wke/1.0"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E5191d Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; fr-fr) AppleWebKit/531.22.7 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16"
  },
  {
    "commonality": "Uncommon",
    "version": "3.2",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/534.50.2 (KHTML, like Gecko) Version/3.2.3 Safari/525.28.3"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0(iPad; U; CPU OS 3_2 like Mac OS X; en-us)AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4Mobile/7B334b Safari/531.21.10"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.52 (KHTML, like Gecko) Version/9.0 Safari/601.1.52"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; zh-cn) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/535.3 (KHTML, like Gecko) Version/5.0.1 Safari/535.3"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.3.4 (KHTML, like Gecko) Version/10.0 Mobile/14G5047a Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/602.1.50 (KHTML, like Gecko) Safari/602.1.50"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows; chromeframe/2.0.0.0) AppleWebKit/1.0 (KHTML, like Gecko) Bromium Safari/1.0"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E5234a Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.1.50 (KHTML, like Gecko) Version/9.0 Safari/601.1.50"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.5.17 (KHTML, like Gecko) Version/9.1 Safari/601.5.17"
  },
  {
    "commonality": "Uncommon",
    "version": "6.2",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/6.2.8 Safari/537.85.17"
  },
  {
    "commonality": "Uncommon",
    "version": "3",
    "ua": "Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420  (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 Safari/602.1.31"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPad; CPU iPhone OS 9.3.2 like Mac OS X; en_US) AppleWebKit/1 (KHTML, like Gecko) Mobile/1 Safari/1 iPhone/1 SellOnEtsy/2.38 rv:23800.40.0"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPhone; CPU OS_5 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version 5.1 Mobile/9A334 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/534.54.16 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; pl-pl) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "3.1",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 2_0 like Mac OS X; en-us) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5A347 Safari/525.20"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/535.3 (KHTML, like Gecko) Version/5.1.7 Safari/535.3"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; nl-nl) AppleWebKit/534.52.7 (KHTML, like Gecko) Fluid/0.9.6 Safari/534.52.7"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; fr-fr) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_11_6 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B411 Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; pt-br) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; es-es) AppleWebKit/530.19.2 (KHTML, like Gecko) Version/4.0.2 Safari/530.19"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/11.0.1 Safari/601.2.7"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/10.1.2 Mobile/10A5376e Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) WebClip/10602.3.12.0.1 Safari/10602.3.12.0.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/10.0 Safari/602.1.31"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6; en-us) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10 FOH:R017"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; en-gb) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "10.2",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/604.1.17 (KHTML, like Gecko) Version/10.2 Safari/604.1.17"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPhone; iPhone OS 5_0) AppleWebKit/535.7 (KHTML, like Gecko) Version/5.1 Mobile Safari/7354.48"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.59.10 (KHTML, like Gecko) Version/4.0.3 Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "3.1",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 2_0 like Mac OS X; en-us) AppleWebKit/528.4.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5A347 Safari/525.20"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8G4 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPad; CPU OS 7_0_3 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Coast/1.1.2.64598 Mobile/11B511 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/538.1 (KHTML, like Gecko) Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_9_5) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12"
  },
  {
    "commonality": "Uncommon",
    "version": "1.0",
    "ua": "Mozilla/5.0 (webOS/1.4.5; U; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Version/1.0 Safari/532.2 Pre/1.0"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 Mobile/15C5110b Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla / 5.0(Macintosh; U; Intel Mac OS X 10_5_5; en - us) AppleWebKit / 525.25(KHTML, like Gecko) Version / 3.2 Safari / 525.25"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows; chromeframe/2.4.8.5729) AppleWebKit/1.0 (KHTML, like Gecko) Bromium Safari/1.0"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.21 (KHTML, like Gecko) PokerGameClient Safari/537.21"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; pt-br) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; es_ES) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B117 Safari/6531.22.7"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6; es-es) AppleWebKit/531.9 (KHTML, like Gecko) Version/4.0.3 Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_5 like Mac OS X; fi-fi) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.32 (KHTML, like Gecko) Version/10.0 Mobile/14A5261v Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (X11; OpenBSD amd64) AppleWebKit/605.1 (KHTML, like Gecko) Version/11.0 Safari/605.1 Surf/2.0"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.22 (KHTML, like Gecko) Version/8.0 Safari/600.1.22"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/604.3.5 (KHTML, like Gecko) Safari/601.6.17"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mobile: Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.38 (KHTML, like Gecko) Version/10.0 Mobile/14A300 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4.11.10 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPhone; CPU OS 7.0.4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) 1Password/4.3.2 (like Version/11B554a Mobile/7.0.4 Safari/8536.25)"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9.2.1 like Mac OS X; en_US) AppleWebKit/1 (KHTML, like Gecko) Mobile/1 Safari/1 iPhone/1 EtsyInc/4.34 rv:43400.94.0"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Superbird/28.0.1500.71 Safari/537.36"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Safari/522.0"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/10.1.2 Safari/537.75.14"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5 bdbrowser/6.4.0.4"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPad; CPU iPad OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "3.2",
    "ua": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5; en-US) AppleWebKit/525.27.1 (KHTML, like Gecko) Version/3.2.1 Safari/525.27.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/10.1 EdgiOS/41.1.0.35 Mobile/15A432 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/10.0 Mobile/12A366 Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "3",
    "ua": "Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3 3gpp-gba"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13D15 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/534.34 (KHTML, like Gecko) Safari/534.34 PhantomJS/2.0.0 (PhantomJsCloud.com/2.0.1)"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_5 like Mac OS X; en) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/4.0.2 Mobile/8C148 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; ko-kr) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/(null) (KHTML, like Gecko) Version/(null) Mobile/(null) Safari/(null)"
  },
  { "commonality": "Uncommon", "version": "", "ua": "Safari/9.1.3" },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/601.1.16 (KHTML, like Gecko) Version/8.0 Mobile/13A171a Safari/600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; es-es) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "3.2",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/534.50.2 (KHTML, like Gecko) Version/3.2.1 Safari/525.27.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/534.50.2 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; de-de) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; fr-fr) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J3 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; fi-fi) AppleWebKit/531.9 (KHTML, like Gecko) Version/4.0.3 Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; ja-jp) AppleWebKit/531.22.7 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) MxNitro/1.0.0.300 Safari/537.36"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 6.1; cs-CZ) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.1.1 Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; zh-cn) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B367 Safari/531.21.10"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.34 (KHTML, like Gecko) RelIdApp/3.1.9 Safari/534.34"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/602.3.12 (KHTML, like Gecko) Safari/602.3.12"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/11.0.1 Safari/601.2.7"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/534.54.16 (KHTML, like Gecko) Version/5.1.4 Safari/534.54.16"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/534.57.7 (KHTML, like Gecko) Version/5.1.1 Safari/534.51.22"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Safari/522.0"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/538.1 (KHTML, like Gecko) fancybrowser Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9.3",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/9.3 Mobile/9B176 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.34 (KHTML, like Gecko) pythonw Safari/534.34"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/538.1 (KHTML, like Gecko) demobrowser/0.1 Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Safari/522.0"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16"
  },
  {
    "commonality": "Uncommon",
    "version": "1.0",
    "ua": "Mozilla/5.0 (webOS/1.3; U; en-US) AppleWebKit/525.27.1 (KHTML, like Gecko) Version/1.0 Safari/525.27.1 Desktop/1.0"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPad; CPU OS 7.0.4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) 1Password/4.3.2 (like Version/11B554a Mobile/7.0.4 Safari/8536.25)"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (iPad; CPU OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53 MxBrowser/4.3.5.2000"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Microsoft Windows NT 6.1.7600.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Version/5.0.4 Safari/537.36"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Coast/2.0.3.70182 Mobile/11B554a Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.59.10 (KHTML, like Gecko) Version 6.0.2 Safari/534.59.10"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/534.34 (KHTML, like Gecko) PhantomJS/1.9.7 Safari/534.34"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9.3.2 like Mac OS X; en_US) AppleWebKit/1 (KHTML, like Gecko) Mobile/1 Safari/1 iPhone/1 EtsyInc/4.39 rv:43900.60.0"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) adbeat.com/policy AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8"
  },
  {
    "commonality": "Uncommon",
    "version": "3.1",
    "ua": "Mozilla/5.0 (Mozilla/5.0 (iPhone; U; CPU iPhone OS 2_0_1 like Mac OS X; haw-US) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5G77 Safari/525.20"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5 companydatatrees"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/534.34 (KHTML, like Gecko) PhantomJS/1.9.1 Safari/534.34"
  },
  {
    "commonality": "Uncommon",
    "version": "11.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.2 (KHTML, like Gecko) Version/11.1 Safari/605.1.2"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/538.1 (KHTML, like Gecko)  Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_2 like Mac OS X) AppleWebKit/604.1.38.0.7 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-gb) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "7.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/7.1.3 Safari/537.85.12"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.12"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.5 Safari/534.55.3"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/531.1 (KHTML, like Gecko) FlyFlow/3.1 Version/5.0 Safari/531.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPod; U; CPU iPhone OS 3_1_3 like Mac OS X; es-es) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7E18 Safari/528.16"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/538.1 (KHTML, like Gecko) janusvr Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "MMozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_1 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B118 Safari/6531.22.7"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_1 like Mac OS X) AppleWebKit/602.2.8 (KHTML, like Gecko) Version/10.0 Mobile/14B55c Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E5277a Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; PowerPC AmigaOS4; Odyssey Web Browser; rv:1.16) AppleWebKit/535.14 (KHTML, like Gecko) OWB/1.16 Safari/535.14"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Phone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/10.0 Mobile/14D27 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Microsoft Windows NT 6.1.7601 Service Pack 1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Version/ 5.0.2Safari/ 5.0.2"
  },
  {
    "commonality": "Uncommon",
    "version": "3",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; fr) AppleWebKit/523.12 (KHTML, like Gecko) Version/3.0.4 Safari/523.12"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla / 5.0(Macintosh; U; PPC Mac OS X; de - de) AppleWebKit / 412(KHTML, like Gecko) Safari / 412"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/602.3.3 (KHTML, like Gecko) Version/10.0 Mobile/14C5062e Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/534.34 (KHTML, like Gecko) pythonw Safari/534.34"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; cs-cz) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "10.3",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/10.3.2 Safari/601.3.9"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.78.2 (KHTML, like Gecko) WebClip/9537.85.15.2 Safari/9537.85.15.3"
  },
  {
    "commonality": "Uncommon",
    "version": "7.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/7.1.8 Safari/537.85.17"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/538.1 (KHTML, like Gecko) ugraf Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/0600.3.18 (KHTML, like Gecko) FluidApp Version/1955 Safari/0600.3.18"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_2_1 like Mac OS X; de-de) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (iPad; CPU OS 11_0_1 like Mac OS X) AppleWebKit/604.2.10 (KHTML, like Gecko) Version/11.0 Mobile/15A8401 Safari/604.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.1.2 Safari/601.3.9"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPad; CPU iPhone OS 9.3.1 like Mac OS X; en_US) AppleWebKit/1 (KHTML, like Gecko) Mobile/1 Safari/1 iPhone/1 SellOnEtsy/2.33 rv:23300.43.0"
  },
  {
    "commonality": "Uncommon",
    "version": "11",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en) AppleWebKit/526.9 (KHTML, like Gecko) Version/11.0 Safari/526.8"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (iPod touch; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_15) AppleWebKit/537.86.6 (KHTML, like Gecko) Version/9.1.1 Safari/537.86.6"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/418.9 (KHTML, like Gecko) Safari/419.3"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/534.34 (KHTML, like Gecko) PhantomJS/1.9.2 Safari/534.34"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/538.1 (KHTML, like Gecko) WebOZ Browser Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (iPhone; CPU OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, Like Gecko) Version/10.1 Mobile/11A465 Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B5130b Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "10.2",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/604.1.6 (KHTML, like Gecko) Version/10.2 Safari/604.1.6"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Amiga; PowerPC AmigaOS 4.1; Odyssey Web Browser; rv:1.23) AppleWebKit/538.1 (KHTML, like Gecko) OWB/1.23 Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/603.1.1 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/5.1 Mobile/12H321 Safari/7600.1.4"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPhone; U CPU iPhone OS 5_1_1 like Mac OS X; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/535.1 (KHTML, like Gecko) iPhone/7.4.1.8 Mobile Safari/535.1 3gpp-gba"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.37 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.4"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPad; CPU iPhone OS 9.3 like Mac OS X; en_US) AppleWebKit/1 (KHTML, like Gecko) Mobile/1 Safari/1 iPhone/1 SellOnEtsy/2.31 rv:23100.39.0"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; es-es) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J3 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-us) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.32 (KHTML, like Gecko) Version/10.0 Safari/602.1.32"
  },
  {
    "commonality": "Uncommon",
    "version": "7",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B511 Safari/9537.53"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; en-gb) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "10.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3_1 like Mac OS X; en-gb) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8G4 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 6.1; sv-SE) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 4_3 like Mac OS X; th-th) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8F190 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "3.1",
    "ua": "Mozilla/5.0 (en-us) AppleWebKit/525.13 (KHTML, like Gecko; Google Web Preview) Version/3.1 Safari/525.13"
  },
  {
    "commonality": "Uncommon",
    "version": "6",
    "ua": "Mozilla/5.0 (iPad; U; CPU OS 9_3_5 like Mac OS X; en-gb) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B141 Safari/8536.25"
  },
  {
    "commonality": "Uncommon",
    "version": "8",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/8.0 Safari/600.1.25"
  },
  {
    "commonality": "Uncommon",
    "version": "3",
    "ua": "Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1C25 Safari/419.3"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.2 (KHTML, like Gecko) Version/10.0 Mobile/14F5075a Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_8_0; nl-nl) AppleWebKit/601.4.4 (KHTML, like Gecko) Fluid/1.7.1 Safari/532.3+"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/10.0.1 Safari/7046A194A"
  },
  {
    "commonality": "Uncommon",
    "version": "10",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.10 (KHTML, like Gecko) Version/10.0 Mobile/15A230 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "5.1",
    "ua": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_1_1 like Mac OS X; en-us) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Macintosh; U; Intel Mac OS X; es-mx AppleWebKit/537+ (KHTML, like Gecko) Version/5.0 Safari/537.6"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en - us) AppleWebKit / 531.21.10(KHTML, like Gecko) Version / 4.0.4 Mobile / 7B314 Safari/ 531.21.10"
  },
  {
    "commonality": "Uncommon",
    "version": "5",
    "ua": "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_2_1 like Mac OS X; fr-fr) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/538.1 (KHTML, like Gecko) PokerClient Safari/538.1"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (iPad; CPU OS 7_0_3 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Coast/2.0.2.69230 Mobile/11B511 Safari/7534.48.3"
  },
  {
    "commonality": "Uncommon",
    "version": "",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Safari/531.9"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/531.9 (KHTML, like Gecko) Version/4.0.3 Safari/531.9.1"
  },
  {
    "commonality": "Uncommon",
    "version": "15",
    "ua": "Mozilla/5.0 (iPad; CPU OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/15.0 Mobile/14D27 Safari/602.1"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/601.4.4 (KHTML, like Gecko) Version/9.1.1 Safari/601.4.4"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Windows; U; Windows NT 5.1 ; en-us; ThinkPad Tablet Build/ThinkPadTablet_A310_02) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13"
  },
  {
    "commonality": "Uncommon",
    "version": "9.1",
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/601.4.4 (KHTML, like Gecko) Version/9.1.1 Safari/601.4.4"
  },
  {
    "commonality": "Uncommon",
    "version": "3.1",
    "ua": "Mozilla/5.0 (iPod; U; CPU iPhone OS 221 like Mac OS X; zh-TW) AppleWebKit/525.18.1 (KHTML like Gecko) Version/3.1.1 Mobile/5H11a Safari/525.20"
  },
  {
    "commonality": "Uncommon",
    "version": "9",
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13C5060d Safari/601.1"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7"
  },
  {
    "commonality": "Uncommon",
    "version": "4",
    "ua": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6; nl-nl) AppleWebKit/531.9 (KHTML, like Gecko) Version/4.0.3 Safari/531.9"
  }
]
