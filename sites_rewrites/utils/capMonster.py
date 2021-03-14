import requests
import time
import json
from utils.logger import logger
import random
import json
import threading
from urllib3.exceptions import HTTPError
import asyncio

async def loadSettings():
    with open(f'./data/config.json') as settings:
        settings = json.loads(settings.read())
        return settings

async def loadProxy(proxies,taskID, SITE):
    if proxies == "":
        return None
    elif proxies != "":
        with open(f'./proxies/{proxies}.txt', 'r') as proxyIn:
            proxyInput = proxyIn.read().splitlines()
    
        proxyList = [i for i in proxyInput]
        p = random.choice(proxyList)
        p = p.split(':')
        try:
            proxies = {
                "address":p[0],
                "port":p[1],
                "login":p[2],
                "passw":p[3]
            }
        except:
            proxies = {
                "address":p[0],
                "port":p[1],
                "login":'',
                "passw":''
            }
        return proxies


class capMonster:
    @staticmethod 
    async def v2(sitekey, url, proxy, SITE,taskID):
        await logger.info(SITE,taskID,'Solving Captcha...')
        settings = await loadSettings()
        apiKey = settings["capMonster"]

        proxy_http = await loadProxy(proxy, taskID, SITE)
        
        address = proxy_http["address"]
        port = proxy_http["port"]
        login = proxy_http["login"]
        passw = proxy_http["passw"]

        

        task = {
            "clientKey":apiKey,
            "task":
            {
                "type":"NoCaptchaTaskProxyless",
                "websiteURL":url,
                "websiteKey":sitekey,
                "proxyType":"http",
                "proxyAddress":address,
                "proxyPort":port,
                "proxyLogin":login,
                "proxyPassword":passw,
                "userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.132 Safari/537.36"
            }
        }

        try:
            r = requests.post('https://api.capmonster.cloud/createTask', json=task)
        except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            await logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
            await v2(sitekey, url, proxy, SITE,taskID)


        if r.status_code == 200 and r.json()['errorId'] == 0:
            data = {
                "clientKey":apiKey,
                "taskId": r.json()['taskId']
            }
            try:
                response = requests.post('https://api.capmonster.cloud/getTaskResult', json=data)
            except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                await logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
                await v2(sitekey, url, proxy, SITE,taskID)

            while response.json()["status"] != 'ready':
                try:
                    response = requests.post('https://api.capmonster.cloud/getTaskResult', json=data)
                except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    await logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
                    await v2(sitekey, url, proxy, SITE,taskID)
                await asyncio.sleep(1)

            return response.json()['solution']['gRecaptchaResponse']
        
        else:
            return None


    @staticmethod 
    async def v3(sitekey, url, proxy, SITE,taskID):
        await logger.info(SITE,taskID,'Solving Captcha...')
        settings = await loadSettings()
        apiKey = settings["capMonster"]
   

        task = {
            "clientKey":apiKey,
            "task":
            {
                "type":"RecaptchaV3TaskProxyless",
                "websiteURL":url,
                "websiteKey":sitekey,
                "minScore": 0.3,
                "pageAction": "myverify"
            }
        }

        try:
            r = requests.post('https://api.capmonster.cloud/createTask', json=task)
        except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            await logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
            await v3(sitekey, url, proxy, SITE,taskID)

        if r.status_code == 200 and r.json()['errorId'] == 0:
            data = {
                "clientKey":apiKey,
                "taskId": r.json()['taskId']
            }
            try:
                response = requests.post('https://api.capmonster.cloud/getTaskResult', json=data)
            except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                await logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
                await v3(sitekey, url, proxy, SITE,taskID)

            while response.json()["status"] != 'ready':
                try:
                    response = requests.post('https://api.capmonster.cloud/getTaskResult', json=data)
                except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    await logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
                    await v3(sitekey, url, proxy, SITE,taskID)
                await asyncio.sleep(1)

    
            return response.json()['solution']['gRecaptchaResponse']
    

    @staticmethod 
    async def hcaptcha(sitekey, url, proxy, SITE,taskID):
        await logger.info(SITE,taskID,'Solving Captcha...')
        settings = await loadSettings()
        apiKey = settings["capMonster"]   

        proxy_http = await loadProxy(proxy, taskID, SITE)['http'].split('http://')[1].split(':')
        if len(proxy_http) == 4:
            address = proxy_http[2]
            port = proxy_http[3]
            login = proxy_http[0]
            passw = proxy_http[1]
        else:
            address = proxy_http[0]
            port = proxy_http[1]
            login = ''
            passw = ''

        task = {
            "clientKey":apiKey,
            "task":
            {
                "type":"HCaptchaTask",
                "websiteURL":url,
                "websiteKey":sitekey,
                "proxyType":"http",
                "proxyAddress":address,
                "proxyPort":port,
                "proxyLogin":login,
                "proxyPassword":passw,
                "userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.132 Safari/537.36"
            }
        }

        try:
            r = requests.post('https://api.capmonster.cloud/createTask', json=task)
        except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            await logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
            await hcaptcha(sitekey, url, proxy, SITE,taskID)

        if r.status_code == 200 and r.json()['errorId'] == 0:
            data = {
                "clientKey":apiKey,
                "taskId": r.json()['taskId']
            }
            try:
                response = requests.post('https://api.capmonster.cloud/getTaskResult', json=data)
            except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                await logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
                await hcaptcha(sitekey, url, proxy, SITE,taskID)

            while response.json()["status"] != 'ready':
                try:
                    response = requests.post('https://api.capmonster.cloud/getTaskResult', json=data)
                except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    await logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
                    await hcaptcha(sitekey, url, proxy, SITE,taskID)
                await asyncio.sleep(1)

    
            return response.json()['solution']['gRecaptchaResponse']



    @staticmethod 
    async def menuV2(sitekey, url, proxy, SITE,taskID):
        await logger.info(SITE,taskID,'Solving Captcha...')
        settings = await loadSettings()
        apiKey = settings["capMonster"]

        proxy_http = await loadProxy(proxy, taskID, SITE)['https'].split('http://')[1].split(':')
        if len(proxy_http) == 4:
            address = proxy_http[2]
            port = proxy_http[3]
            login = proxy_http[0]
            passw = proxy_http[1]
        else:
            address = proxy_http[0]
            port = proxy_http[1]
            login = ''
            passw = ''

        

        task = {
            "clientKey":apiKey,
            "task":
            {
                "type":"NoCaptchaTaskProxyless",
                "websiteURL":url,
                "websiteKey":sitekey,
                "proxyType":"http",
                "proxyAddress":address,
                "proxyPort":port,
                "proxyLogin":login,
                "proxyPassword":passw,
                "userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.132 Safari/537.36"
            }
        }

        try:
            r = requests.post('https://api.capmonster.cloud/createTask', json=task)
        except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            await logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
            await menuV2(sitekey, url, proxy, SITE,taskID)

        if r.status_code == 200 and r.json()['errorId'] == 0:
            data = {
                "clientKey":apiKey,
                "taskId": r.json()['taskId']
            }
            try:
                response = requests.post('https://api.capmonster.cloud/getTaskResult', json=data)
            except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                await logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
                await menuV2(sitekey, url, proxy, SITE,taskID)

            while response.json()["status"] != 'ready':
                try:
                    response = requests.post('https://api.capmonster.cloud/getTaskResult', json=data)
                except(Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    await logger.error(SITE,taskID,'Failed to get captcha. Retrying...')
                    await menuV2(sitekey, url, proxy, SITE,taskID)
                    
                await asyncio.sleep(1)

            with open('./data/captcha/tokens.json') as config:
                tokens = json.loads(config.read())
                
    
            tokens[SITE].append({"token":response.json()['solution']['gRecaptchaResponse']})
    
            with open('./data/captcha/tokens.json','w') as output:
                json.dump(tokens,output)
    
            await logger.success(SITE,taskID,'Captcha Solved')
            # threading.currentThread().handled = True
            return 'complete'
            