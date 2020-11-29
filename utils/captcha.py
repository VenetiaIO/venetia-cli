import requests
import time
import json
from utils.logger import logger
import random
import json
import threading
from urllib3.exceptions import HTTPError

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

class captcha:
    @staticmethod
    def v2(sitekey, url, proxy, SITE,taskID):
        logger.info(SITE,taskID,'Solving Captcha...')
        twoCap = loadSettings()["2Captcha"]
        captchaURL = 'https://2captcha.com/in.php?key={}&method=userrecaptcha&version=v2&action=verify&min_score=0.3&googlekey={}&pageurl={}&json=1'.format(twoCap,sitekey,url)
        try:
            first = requests.get(captchaURL)
        except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
            v2(sitekey,url,proxy,SITE,taskID)

        time.sleep(8)
        if proxy == None:
            url = 'https://2captcha.com/res.php?key={}&action=get&taskinfo=1&id={}&json=1'.format(twoCap,first.json()["request"])
        else:
            try:
                url = 'https://2captcha.com/res.php?key={}&action=get&taskinfo=1&id={}&json=1&proxy={}&proxytype=HTTPS'.format(twoCap,first.json()["request"],proxy["https"])
            except:
                url = 'https://2captcha.com/res.php?key={}&action=get&taskinfo=1&id={}&json=1'.format(twoCap,first.json()["request"])
        try:
            r = requests.get(url)
        except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
            v2(sitekey,url,proxy,SITE,taskID)
        while r.json()["request"] == "CAPCHA_NOT_READY":
            try:
                r = requests.get(url)
            except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
                v2(sitekey,url,proxy,SITE,taskID)
            time.sleep(1)
        return r.json()["request"]

    @staticmethod
    def Hiddenv2(sitekey, url, proxy, SITE,taskID):
        logger.info(SITE,taskID,'Solving Captcha...')
        twoCap = loadSettings()["2Captcha"]
        captchaURL = 'https://2captcha.com/in.php?key={}&method=userrecaptcha&version=v2&action=verify&min_score=0.3&googlekey={}&pageurl={}&json=1'.format(twoCap,sitekey,url)
        try:
            first = requests.get(captchaURL)
        except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            Hiddenv2(sitekey,url,proxy,SITE,taskID)
        time.sleep(8)
        if proxy == None:
            url = 'https://2captcha.com/res.php?key={}&action=get&taskinfo=1&id={}&json=1'.format(twoCap,first.json()["request"])
        else:
            try:
                url = 'https://2captcha.com/res.php?key={}&action=get&taskinfo=1&id={}&json=1&proxy={}&proxytype=HTTPS'.format(twoCap,first.json()["request"],proxy["https"])
            except:
                url = 'https://2captcha.com/res.php?key={}&action=get&taskinfo=1&id={}&json=1'.format(twoCap,first.json()["request"])
        try:
            r = requests.get(url)
        except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            Hiddenv2(sitekey,url,proxy,SITE,taskID)
        while r.json()["request"] == "CAPCHA_NOT_READY":
            try:
                r = requests.get(url)
            except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
                Hiddenv2(sitekey,url,proxy,SITE,taskID)
            time.sleep(1)
        return r.json()["request"]


    @staticmethod
    def v3(sitekey, url, proxy, SITE,taskID):
        logger.info(SITE,taskID,'Solving Captcha...')
        twoCap = loadSettings()["2Captcha"]
        captchaURL = 'https://2captcha.com/in.php?key={}&method=userrecaptcha&version=v3&action=verify&min_score=0.3&googlekey={}&pageurl={}&json=1'.format(twoCap,sitekey,url)
        try:
            first = requests.get(captchaURL)
        except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
            v3(sitekey,url,proxy,SITE,taskID)
        time.sleep(8)
        if proxy == None:
            url = 'https://2captcha.com/res.php?key={}&action=get&taskinfo=1&id={}&json=1'.format(twoCap,first.json()["request"])
        else:
            try:
                url = 'https://2captcha.com/res.php?key={}&action=get&taskinfo=1&id={}&json=1&proxy={}&proxytype=HTTPS'.format(twoCap,first.json()["request"],proxy["https"])
            except:
                url = 'https://2captcha.com/res.php?key={}&action=get&taskinfo=1&id={}&json=1'.format(twoCap,first.json()["request"])
        try:
            r = requests.get(url)
        except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
            v3(sitekey,url,proxy,SITE,taskID)
        while r.json()["request"] == "CAPCHA_NOT_READY":
            try:
                r = requests.get(url)
            except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
                v3(sitekey,url,proxy,SITE,taskID)
            logger.warning(SITE,taskID,r.json()["request"])
            time.sleep(1)
        return r.json()["request"]

    @staticmethod
    def hcaptcha(sitekey, url, proxy, SITE,taskID):
        logger.info(SITE,taskID,'Solving Captcha...')
        twoCap = loadSettings()["2Captcha"]
        captchaURL = 'https://2captcha.com/in.php?key={}&method=hcaptcha&action=verify&googlekey={}&pageurl={}&json=1'.format(twoCap,sitekey,url)
        try:
            first = requests.get(captchaURL)
        except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
            hcaptcha(sitekey,url,proxy,SITE,taskID)
        time.sleep(8)
        if proxy == None:
            url = 'https://2captcha.com/res.php?key={}&action=get&taskinfo=1&id={}&json=1'.format(twoCap,first.json()["request"])
        else:
            try:
                url = 'https://2captcha.com/res.php?key={}&action=get&taskinfo=1&id={}&json=1&proxy={}&proxytype=HTTPS'.format(twoCap,first.json()["request"],proxy["https"])
            except:
                url = 'https://2captcha.com/res.php?key={}&action=get&taskinfo=1&id={}&json=1'.format(twoCap,first.json()["request"])
        try:
            r = requests.get(url)
        except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
            hcaptcha(sitekey,url,proxy,SITE,taskID)
        while r.json()["request"] == "CAPCHA_NOT_READY":
            try:
                r = requests.get(url)
            except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
                hcaptcha(sitekey,url,proxy,SITE,taskID)
            logger.warning(SITE,taskID,r.json()["request"])
            time.sleep(1)
        return r.json()["request"]

    @staticmethod
    def geetest(gt, challenge, apiServer, pageurl, proxy, SITE, taskID):
        logger.info(SITE,taskID,'Solving Captcha...')
        twoCap = loadSettings()["2Captcha"]

        url = f'https://2captcha.com/in.php?key={twoCap}&method=geetest&gt={gt}&challenge={challenge}&api_server={apiServer}&pageurl={pageurl}&json=1'
        try:
            r = requests.get(url)
        except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
            geetest(gt,challenge,apiServer,pageurl,proxy,SITE,taskID)
        if r.status_code == 200 and r.json()["status"] == 1:
            time.sleep(15)
            if proxy == None:
                url = 'https://2captcha.com/res.php?key={}&action={}&id={}&json=1'.format(twoCap,'get',r.json()["request"])
            else:
                try:
                    proxy = loadProxy(proxy,'')
                    url = 'https://2captcha.com/res.php?key={}&action={}&id={}&json=1&proxy={}&proxytype=HTTPS'.format(twoCap,'get',r.json()["request"],proxy["https"])
                except:
                    url = 'https://2captcha.com/res.php?key={}&action={}&id={}&json=1'.format(twoCap,'get',r.json()["request"])
            try:
                res = requests.get(url)
            except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
                geetest(gt,challenge,apiServer,pageurl,proxy,SITE,taskID)
            while res.json()["request"] in ['CAPCHA_NOT_READY']:
                try:
                    res = requests.get(url)
                except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
                    geetest(gt,challenge,apiServer,pageurl,proxy,SITE,taskID)
                time.sleep(2)
    
            return res.json()

    
    @staticmethod
    def menuV2(sitekey, url, proxy, taskID, SITE):
        logger.alert(SITE,taskID,'Solving Captcha...')
        twoCap = loadSettings()["2Captcha"]
        captchaURL = 'https://2captcha.com/in.php?key={}&method=userrecaptcha&version=v2&action=verify&min_score=0.3&googlekey={}&pageurl={}&json=1'.format(twoCap,sitekey,url)
        try:
            first = requests.get(captchaURL)
        except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
            menuV2(sitekey,url,proxy,SITE,taskID)
        time.sleep(8)
        if proxy == None:
            url = 'https://2captcha.com/res.php?key={}&action=get&taskinfo=1&id={}&json=1'.format(twoCap,first.json()["request"])
        else:
            try:
                proxy = loadProxy(proxy,taskID)
                url = 'https://2captcha.com/res.php?key={}&action=get&taskinfo=1&id={}&json=1&proxy={}&proxytype=HTTPS'.format(twoCap,first.json()["request"],proxy["https"])
            except:
                url = 'https://2captcha.com/res.php?key={}&action=get&taskinfo=1&id={}&json=1'.format(twoCap,first.json()["request"])
        try:
            r = requests.get(url)
        except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
            menuV2(sitekey,url,proxy,SITE,taskID)
        while r.json()["request"] == "CAPCHA_NOT_READY":
            try:
                r = requests.get(url)
            except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
                menuV2(sitekey,url,proxy,SITE,taskID)
            time.sleep(1)
        if r.json()["request"] == "ERROR_CAPTCHA_UNSOLVABLE":
            return 'failed'
        else:
            with open('./data/captcha/tokens.json') as config:
                tokens = json.loads(config.read())
                
    
            tokens[SITE].append({"token":r.json()["request"]})
    
            with open('./data/captcha/tokens.json','w') as output:
                json.dump(tokens,output)
    
            logger.success(SITE,taskID,'CAPCHA_SOLVED')
            threading.currentThread().handled = True
            return 'complete'